import requests

# Адрес нашего сервера, который сейчас запущен
url = 'http://127.0.0.1:5000/upload'

# Укажи путь к любому изображению, которое хочешь распознать
# (напиши здесь название файла, который лежит в папке kons)
file_path = 'test.jpg' 

try:
    with open(file_path, 'rb') as f:
        files = {'file': (file_path, f, 'image/png')}
        print("Отправляю файл на сервер...")
        response = requests.post(url, files=files)
        
        if response.status_code == 200:
            print("Успешно! Ответ сервера:")
            print(response.json())
        else:
            print(f"Ошибка: {response.status_code}")
            print(response.text)
except FileNotFoundError:
    print(f"Файл {file_path} не найден. Проверь имя файла!")