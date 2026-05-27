import sqlite3

conn = sqlite3.connect('notes_archive.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM notes")
rows = cursor.fetchall()

print("Твой архив:")
for row in rows:
    print(f"ID: {row[0]}, Предмет: {row[1]}, Тема: {row[2]}, Контент: {row[3][:50]}...") # Выведет первые 50 символов конспекта
conn.close()