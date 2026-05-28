import sqlite3
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
# Импортируем нашу функцию из ocr_analyzer.py
from ocr_analyzer import analyze_handwriting

app = Flask(__name__)
# Добавь эту строчку сразу после app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

# Имя нашей базы данных
DB_NAME = "notes_archive.db"

# Твой список предметов для нормализации
SUBJECT_MAP = {
    "геометрия": "Геометрия", "физика": "Физика", "химия": "Химия",
    "английский язык": "Английский язык", "алгебра": "Алгебра",
    "история": "История", "русский язык": "Русский язык",
    "география": "География", "обществознание": "Обществознание",
    "биология": "Биология", "информатика": "Информатика", "литература": "Литература"
}

def normalize_subject(ai_subject):
    # Приводим к нижнему регистру и ищем в списке, если нет - "Разное"
    return SUBJECT_MAP.get(ai_subject.lower().strip(), "Разное")

def init_db():
    # Создаем базу данных и таблицу, если их еще нет
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS notes 
                      (id INTEGER PRIMARY KEY, subject TEXT, topic TEXT, content TEXT)''')
    conn.commit()
    conn.close()

# Инициализируем базу при запуске
init_db()

@app.route('/upload', methods=['POST'])
def upload_file():
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    if 'file' not in request.files:
        return jsonify({"error": "Файл не найден"}), 400
        
    file = request.files['file']
    # Сохраняем фото во временную папку uploads
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)
    
    # Обрабатываем через наш AI
    data = analyze_handwriting(file_path)
    
    # Нормализуем предмет
    subj = normalize_subject(data['subject'])
    topic = data['topic']
    text = data['text']
    
    # Сохраняем в БД (или обновляем существующую тему)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Проверяем, есть ли уже такая тема в этом предмете
    cursor.execute("SELECT id, content FROM notes WHERE subject = ? AND topic = ?", (subj, topic))
    row = cursor.fetchone()
    
    if row:
        # Дописываем текст, если тема есть
        new_content = row[1] + "\n\n--- Дополнение ---\n" + text
        cursor.execute("UPDATE notes SET content = ? WHERE id = ?", (new_content, row[0]))
    else:
        # Создаем новую запись
        cursor.execute("INSERT INTO notes (subject, topic, content) VALUES (?, ?, ?)", (subj, topic, text))
    
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success", "subject": subj, "topic": topic})
# 1. Получить список всех предметов, по которым есть записи
@app.route('/subjects', methods=['GET'])
def get_subjects():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT subject FROM notes")
    subjects = [row[0] for row in cursor.fetchall()]
    conn.close()
    return jsonify(subjects)

# 2. Получить список всех тем внутри конкретного предмета
@app.route('/topics', methods=['GET'])
def get_topics():
    subj = request.args.get('subject')
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT topic FROM notes WHERE subject = ?", (subj,))
    topics = [row[0] for row in cursor.fetchall()]
    conn.close()
    return jsonify(topics)

# 3. Получить конкретный конспект
@app.route('/note', methods=['GET'])
def get_note():
    subj = request.args.get('subject')
    topic = request.args.get('topic')
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM notes WHERE subject = ? AND topic = ?", (subj, topic))
    row = cursor.fetchone()
    conn.close()
    if row:
        return jsonify({"content": row[0]})
    return jsonify({"error": "Конспект не найден"}), 404
if __name__ == '__main__':
    # Render автоматически назначает порт через переменную окружения PORT
    port = int(os.environ.get("PORT", 5000))
    # host='0.0.0.0' делает сервер доступным для внешних подключений
    app.run(host='0.0.0.0', port=port)