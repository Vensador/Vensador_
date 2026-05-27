import sqlite3
from datetime import datetime

DB_NAME = "study_notes.db"

def init_db():
    """Создает таблицы в базе данных, если их еще нет"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Таблица для хранения предметов и тем
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            topic_name TEXT NOT NULL,
            UNIQUE(user_id, subject, topic_name)
        )
    ''')
    
    # Таблица для хранения текстов конспектов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_id INTEGER NOT NULL,
            note_text TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (topic_id) REFERENCES topics (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def save_note(user_id: int, subject: str, topic_name: str, text: str):
    """Сохраняет конспект. Если тема уже есть, использует старую."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Делаем красивые названия с заглавной буквы
    subject = subject.strip().capitalize()
    topic_name = topic_name.strip().capitalize()
    
    try:
        # Пробуем создать новую тему
        cursor.execute(
            "INSERT INTO topics (user_id, subject, topic_name) VALUES (?, ?, ?)",
            (user_id, subject, topic_name)
        )
        topic_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        # Если тема уже существует, находим её ID
        cursor.execute(
            "SELECT id FROM topics WHERE user_id = ? AND subject = ? AND topic_name = ?",
            (user_id, subject, topic_name)
        )
        topic_id = cursor.fetchone()[0]
        
    # Записываем сам текст
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO notes (topic_id, note_text, created_at) VALUES (?, ?, ?)",
        (topic_id, text, current_time)
    )
    
    conn.commit()
    conn.close()
    return subject, topic_name