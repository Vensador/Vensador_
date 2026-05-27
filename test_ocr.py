from ocr_analyzer import analyze_handwriting

def run_ocr_test():
    print("📸 Отправляем картинку 'test.jpg' в Gemini...")
    
    # Запускаем распознавание
    result = analyze_handwriting("test.jpg")
    
    print("\n🤖 Ответ от нейросети:")
    print(f"📚 Предмет: {result.get('subject')}")
    print(f"📑 Тема: {result.get('topic')}")
    print(f"📝 Текст конспекта:\n{result.get('text')}")

if __name__ == "__main__":
    run_ocr_test()