import sqlite3
from database import init_db, save_note, DB_NAME

def run_test():
    print("🤖 Запуск теста базы данных...")
    init_db()
    
    user_id = 777
    
    # Запись 1 (История)
    save_note(user_id, "История", "Екатерина 1", "Конспект номер один про Екатерину.")
    
    # Запись 2 (Физика)
    save_note(user_id, "физика", "оптика", "Конспект про линзы и свет.")
    
    # Запись 3 (Снова История — проверяем, склеится ли!)
    save_note(user_id, "История", "екатерина 1", "Конспект номер два про Екатерину.")
    
    # Смотрим, что получилось в базе
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM topics")
    topics = cursor.fetchall()
    print(f"\nСоздано уникальных тем: {len(topics)} (Должно быть 2)")
    
    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()
    print(f"Всего сохраненных записей: {len(notes)} (Должно быть 3)")
    
    conn.close()
    print("\n🏁 Тест завершен!")

if __name__ == "__main__":
    run_test()