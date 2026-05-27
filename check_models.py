import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_KEY = "AIzaSyCN4w3iNtHO5fk8GX_TF89oZnNo5ux-pUs"
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"

try:
    print("Проверяем реальный ответ от Google...")
    response = requests.get(url, verify=False, timeout=15)
    print(f"Статус ответа: {response.status_code}")
    
    if response.status_code == 200:
        models = response.json().get('models', [])
        print("\nСписок доступных моделей:")
        for m in models[:5]: # Выведем первые 5 для проверки
            print(f" - {m['name']}")
    else:
        print(f"Ответ сервера: {response.text}")
except Exception as e:
    print(f"Ошибка сети: {e}")