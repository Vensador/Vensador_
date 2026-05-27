import os
import json
import base64
import requests
import urllib3

# Отключаем предупреждения об SSL в консоли
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Твой рабочий API-ключ
API_KEY = "AIzaSyCN4w3iNtHO5fk8GX_TF89oZnNo5ux-pUs"

def analyze_handwriting(image_path: str) -> dict:
    """
    Распознает текст конспекта через актуальную модель Gemini 2.5 Flash.
    """
    try:
        # Авто-подмена имени файла, если на диске лежит text.jpg
        if not os.path.exists(image_path):
            if image_path == "test.jpg" and os.path.exists("text.jpg"):
                image_path = "text.jpg"
            else:
                return {
                    "text": f"Файл {image_path} не найден!",
                    "subject": "Ошибка",
                    "topic": "Нет файла"
                }

        # 1. Читаем картинку в чистый Base64
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode("utf-8")
            
        # 2. АКТУАЛЬНЫЙ URL С МОДЕЛЬЮ GEMINI 2.5 FLASH (из твоего лога!)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
        
        # 3. Инструкция для ИИ
        prompt = """
        You are an assistant for recognizing school notebooks.
        1. Read the handwritten Russian text in the image. Ignore crossed-out text.
        2. Determine the school subject in Russian (e.g., История, Физика, Биология).
        3. Determine the main topic in Russian (e.g., Екатерина I, Оптика, Анатомия).
        
        Return the result strictly in JSON format with these exact keys:
        {
          "text": "all recognized text from the notebook",
          "subject": "subject name in Russian",
          "topic": "topic name in Russian"
        }
        """
        
        # 4. Структура Payload для моделей 2.5 (тут camelCase для ответа в JSON)
        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {
                        "inlineData": {
                            "mimeType": "image/jpeg", 
                            "data": image_data
                        }
                    }
                ]
            }],
            "generationConfig": {
                "responseMimeType": "application/json"
            }
        }
        
        headers = {"Content-Type": "application/json"}
        
        # 5. Отправляем запрос через твой VPN
        response = requests.post(url, json=payload, headers=headers, verify=False, timeout=30)
        
        if response.status_code != 200:
            print(f"Ошибка сервера Google: Status {response.status_code}")
            print(f"Детали: {response.text}")
            return {"text": "Ошибка API", "subject": "Разное", "topic": "Неизвестно"}
            
        # 6. Парсим ответ
        response_json = response.json()
        text_content = response_json['candidates'][0]['content']['parts'][0]['text']
        
        # Очищаем от markdown-обертки, если она появится
        text_content = text_content.replace("```json", "").replace("```", "").strip()
        
        return json.loads(text_content)

    except Exception as e:
        print(f"Ошибка при распознавании: {e}")
        return {
            "text": "Не удалось распознать текст.",
            "subject": "Разное",
            "topic": "Неизвестно"
        }