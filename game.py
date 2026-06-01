import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from deep_translator import GoogleTranslator
import random

words_db = {
    "easy": {
        "кот": "cat", 
        "собака": "dog", 
        "дом": "house", 
        "вода": "water",
        "книга": "book", 
        "стол": "table", 
        "цветок": "flower", 
        "молоко": "milk",
        "хлеб": "bread", 
        "солнце": "sun",
    },
    
    "medium": {
        "путешествие": "journey", 
        "зеркало": "mirror", 
        "одеяло": "blanket",
        "голодный": "hungry", 
        "красивый": "beautiful", 
        "опасность": "danger",
        "лестница": "stairs", 
        "погода": "weather", 
        "счастье": "happiness",
        "приключение": "adventure"
    },
    "hard": {
        "произношение": "pronunciation", 
        "возможность": "opportunity",
        "окружающая среда": "environment", 
        "любопытный": "curious",
        "необходимость": "necessity", 
        "изобретение": "invention",
        "правительство": "government", 
        "значительный": "significant",
        "одновременно": "simultaneously", 
        "достопримечательность": "sightseeing"
    },
    "numbers": {
        "один": "one",
        "пять": "five",
        "десять": "ten",
        "тринадцать": "thirteen",
        "двенадцать": "twelve",
        "двадцать": "twenty",
        "пятьдесят": "fifty",
        "семьдесят": "seventy",
        "одна сотня": "onehundred",
        "одна тысяча семьдесят": "onethousandseventy"
    }
    
}   

def listen_and_recognize():
    duration = 5 
    sample_rate = 44100
    print("Говорите...")
    recording = sd.rec(
    int(duration * sample_rate), # длительность записи в сэмплах
    samplerate=sample_rate,      # частота дискретизации
    channels=1,                  # 1 — это моно
    dtype="int16")               # формат аудиоданных
    sd.wait()  # ждём завершения записи

    wav.write("output.wav", sample_rate, recording)
    print("Запись завершена, распознаём текст...")

    recognizer = sr.Recognizer()
    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language="en-EN")
        print(f'Ты сказал: {text}')
        return text.lower()
    except sr.UnknownValueError:             # - если Google не понял речь (шум, молчание)
        print("")
    except sr.RequestError as e:             # - если нет интернета или API недоступен
        print(f"Ошибка сервиса: {e}")

def compare_words(spoken, correct):
    if not spoken:
        return False
    return spoken == correct

def calculate_points(level, streak=0):
    base = {"easy": 10, "medium": 20, "hard": 30, "numbers": 15}
    bonus = streak * 5  
    return base.get(level, 10) + bonus

def game():
    print('''
••••••••••  ••      ••    ••••••          ••••••••••    ••••••      ••••••    
••••••••••  ••      ••    ••••••          ••••••••••    ••••••      ••••••    
••          ••••    ••  ••                ••          ••          ••          
••          ••••    ••  ••                ••          ••          ••          
••••••••    ••  ••  ••  ••    ••••        ••••••••    ••    ••••  ••    ••••  
••••••••    ••  ••  ••  ••    ••••        ••••••••    ••    ••••  ••    ••••  
••          ••    ••••  ••      ••        ••          ••      ••  ••      ••  
••          ••    ••••  ••      ••        ••          ••      ••  ••      ••  
••••••••••  ••      ••    ••••••          ••••••••••    ••••••      ••••••    
••••••••••  ••      ••    ••••••          ••••••••••    ••••••      ••••••    

    ''')
    print("Добро пожаловать в игру 'EngEgg'🥚\n")
    print("📜 Правила:")
    print("• Ты увидишь слово на русском.\n• Произнеси его перевод на английский.\n• У тебя есть 5 секунд на ответ\n• Если правильно — получаешь баллы.\n• Ошибки отнимают жизни.\n• Чем сложнее уровень, тем больше баллов за слово.")
    print("<-- - - - - - - - - - - -->")
    print("Выбери уровень сложности:")
    print("1 — Лёгкий 😁\n2 — Средний 😮\n3 — Сложны 😳\n4 — Числа 🤓")
    dif = input("Введи номер уровня (1/2/3/4): ").strip()

    if dif == "4":
        level = "numbers"  
        lives = 3
    elif dif == "3":
        level = "hard"  
        lives = 2
    elif dif == "2":
        level = "medium"  
        lives = 3
    else:
        level = "easy" 
        lives = 4
    
    score = 0
    streak = 0
    rounds = 10  
    

    words = list(words_db[level].items())
    random.shuffle(words)
    words = words[:rounds]
    
    level_names = {"easy": "Лёгкий", "medium": "Средний", "hard": "Сложный", "numbers": "Числа"}
    print(f"🦾 Уровень: {level_names[level].upper()} | 💘 Жизни: {lives} | 🎯 Раундов: {rounds}")
    
    input("Нажми ENTER, чтобы начать...")
    
    for round_num, (russian, correct_english) in enumerate(words, 1):
        if lives <= 0:
            print(f"\n💔 Жизни кончились! GAME OVER.")
            break
        
        print(f"\n{'='*40}")
        print(f"🎯 Раунд {round_num}/{rounds}")
        print(f"📖 Переведи слово: {russian.upper()}")
        print(f"💘 Жизней: {lives} | ⭐ Счёт: {score}")
        
        spoken_english = listen_and_recognize()
        
        if spoken_english is None:
            print(f"Пропуск хода. Правильный ответ: {correct_english}")
            lives -= 1
            streak = 0
            continue
        
        elif compare_words(spoken_english, correct_english):
            streak += 1
            points = calculate_points(level, streak)
            score += points
            print(f"ОТЛИЧНО! +{points} баллов")
            if streak >= 3:
                print(f"Серия из {streak} правильных ответов!")
        else:
            lives -= 1
            streak = 0
            print(f"Неправильно. Ты сказал: '{spoken_english}'")
            print(f"Правильно: {correct_english}")
            print(f"Осталось жизней: {lives}")


    print(f"\n{'='*40}")
    print("🏁 ИГРА ЗАВЕРШЕНА")
    print(f"Итоговый счёт: {score} баллов")
    
    # Рейтинг
    if score >= 200:
        print(f"💂 Ты — Мастер произношения!")
    elif score >= 100:
        print(f"🏆 Отличный результат! Так держать!")
    elif score >= 50:
        print(f"🎤 Неплохо! Продолжай тренироваться.")
    else:
        print(f"📚 Нужно больше практики. Не сдавайся!")
    
    # Играть снова
    again = input("\n🔄 Сыграть ещё раз? ").lower().strip()
    if again in ["да", "yes", "y", "д"]:
        game()
    else:
        print("""Спасибо за игру! Пока-пока! 👋
█████ █   █  ███     █████  ███   ███  
█     ██  █ █        █     █     █     
████  █ █ █ █  ██    ████  █  ██ █  ██ 
█     █  ██ █   █    █     █   █ █   █ 
█████ █   █  ███     █████  ███   ███  
              """)


if __name__ == '__main__':
    game()
