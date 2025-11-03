import streamlit as st
import json
from datetime import datetime
import random

# Инициализация состояния игры
if 'game_state' not in st.session_state:
    st.session_state.game_state = {
        'score': 0,
        'level': 1,
        'missions_completed': [],
        'player_name': '',
        'hints_used': 0,
        'start_time': datetime.now()
    }

class CryptoGame:
    def __init__(self):
        self.russian_alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        self.english_alphabet = 'abcdefghijklmnopqrstuvwxyz'
    
    def caesar_encrypt(self, text, shift, alphabet):
        result = []
        for char in text.lower():
            if char in alphabet:
                idx = (alphabet.index(char) + shift) % len(alphabet)
                result.append(alphabet[idx])
            else:
                result.append(char)
        return ''.join(result)
    
    def vigenere_encrypt(self, text, key, alphabet):
        result = []
        key = key.lower()
        key_length = len(key)
        
        for i, char in enumerate(text.lower()):
            if char in alphabet:
                text_idx = alphabet.index(char)
                key_idx = alphabet.index(key[i % key_length])
                new_idx = (text_idx + key_idx) % len(alphabet)
                result.append(alphabet[new_idx])
            else:
                result.append(char)
        return ''.join(result)

def main():
    st.set_page_config(
        page_title="Крипто-Детектив", 
        page_icon="🕵️", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # CSS для красивого оформления
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .mission-card {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #1f77b4;
    }
    .success-message {
        color: #28a745;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    game = CryptoGame()
    
    # Заголовок приложения
    st.markdown('<h1 class="main-header">🕵️ Крипто-Детектив</h1>', unsafe_allow_html=True)
    
    # Боковая панель для настроек и статистики
    with st.sidebar:
        st.header("🎮 Управление игрой")
        
        # Инициализация игрока
        if not st.session_state.game_state['player_name']:
            player_name = st.text_input("Введите ваше имя детектива:")
            if player_name:
                st.session_state.game_state['player_name'] = player_name
                st.rerun()
        else:
            st.success(f"Детектив: {st.session_state.game_state['player_name']}")
        
        # Выбор алфавита
        alphabet_choice = st.radio("Алфавит:", ["Русский", "Английский"], key="alphabet")
        current_alphabet = game.russian_alphabet if alphabet_choice == "Русский" else game.english_alphabet
        
        # Статистика
        st.markdown("---")
        st.header("📊 Статистика")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🏆 Очки", st.session_state.game_state['score'])
        with col2:
            st.metric("🎯 Уровень", st.session_state.game_state['level'])
        
        st.metric("✅ Миссий", len(st.session_state.game_state['missions_completed']))
        
        # Сброс игры
        if st.button("🔄 Новая игра"):
            for key in st.session_state.game_state:
                if key != 'start_time':
                    st.session_state.game_state[key] = 0 if isinstance(st.session_state.game_state[key], (int, float)) else []
            st.session_state.game_state['start_time'] = datetime.now()
            st.rerun()
    
    # Основное содержимое - вкладки
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Миссии", "📚 Обучение", "🏆 Достижения", "⚙️ Тренировка"])
    
    with tab1:
        show_missions_tab(game, current_alphabet)
    
    with tab2:
        show_learning_tab(game, current_alphabet)
    
    with tab3:
        show_achievements_tab()
    
    with tab4:
        show_practice_tab(game, current_alphabet)

def show_missions_tab(game, alphabet):
    st.header("🎯 Сюжетные миссии")
    
    missions = [
        {
            "id": 1,
            "title": "Обучение у мастера",
            "description": "Старый криптограф передает вам первое задание...",
            "type": "caesar",
            "difficulty": "🟢 Начальный",
            "points": 100
        },
        {
            "id": 2, 
            "title": "Перехваченные документы",
            "description": "Расшифруйте сообщения вражеских агентов!",
            "type": "vigenere", 
            "difficulty": "🟡 Средний",
            "points": 150
        },
        {
            "id": 3,
            "title": "Финальная схватка",
            "description": "Битва с главным крипто-злодеем!",
            "type": "mixed",
            "difficulty": "🔴 Сложный", 
            "points": 200
        }
    ]
    
    for mission in missions:
        with st.container():
            st.markdown(f'<div class="mission-card">', unsafe_allow_html=True)
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(f"Миссия {mission['id']}: {mission['title']}")
                st.write(mission['description'])
                st.write(f"**Сложность:** {mission['difficulty']} | **Награда:** {mission['points']} очков")
            
            with col2:
                mission_completed = mission['id'] in st.session_state.game_state['missions_completed']
                if mission_completed:
                    st.success("✅ Завершено")
                else:
                    if st.button(f"Начать", key=f"mission_{mission['id']}"):
                        start_mission(game, mission, alphabet)
            
            st.markdown('</div>', unsafe_allow_html=True)

def start_mission(game, mission, alphabet):
    st.session_state.current_mission = mission
    
    if mission['type'] == 'caesar':
        # Генерация задания Цезаря
        texts_ru = ["пройди обучение", "стань детективом", "разгадай тайну"]
        texts_en = ["start your journey", "become a detective", "solve the mystery"]
        text = random.choice(texts_ru if alphabet == game.russian_alphabet else texts_en)
        shift = random.randint(1, 5)
        
        encrypted = game.caesar_encrypt(text, shift, alphabet)
        
        st.info(f"🔐 **Зашифрованное сообщение:** `{encrypted}`")
        st.info(f"💡 **Подсказка:** Шифр Цезаря со сдвигом {shift}")
        
        answer = st.text_input("Введите расшифрованный текст:")
        
        if answer:
            if answer.lower() == text:
                st.success("🎉 Верно! Миссия выполнена!")
                complete_mission(mission['id'], mission['points'])
            else:
                st.error("❌ Неверно! Попробуйте еще раз.")

def complete_mission(mission_id, points):
    if mission_id not in st.session_state.game_state['missions_completed']:
        st.session_state.game_state['missions_completed'].append(mission_id)
        st.session_state.game_state['score'] += points
        st.session_state.game_state['level'] = len(st.session_state.game_state['missions_completed']) + 1
        st.rerun()

def show_learning_tab(game, alphabet):
    st.header("📚 Теория криптографии")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔐 Шифр Цезаря")
        st.image("https://via.placeholder.com/300x200?text=Caesar+Cipher", use_column_width=True)
        st.markdown("""
        **Принцип работы:**
        - Каждая буква сдвигается на фиксированное число позиций
        - Пример: сдвиг 3, 'А' → 'Г', 'Б' → 'Д'
        - Простой в использовании, но ненадежный
        """)
        
        # Интерактивный пример
        st.subheader("🧪 Попробуйте сами:")
        text_caesar = st.text_input("Текст для шифра Цезаря:", "привет")
        shift = st.slider("Сдвиг:", 1, 10, 3)
        if text_caesar:
            encrypted = game.caesar_encrypt(text_caesar, shift, alphabet)
            st.code(f"Зашифровано: {encrypted}")

def show_achievements_tab():
    st.header("🏆 Ваши достижения")
    
    achievements = [
        {"name": "Первый шаг", "description": "Завершите первую миссию", "completed": len(st.session_state.game_state['missions_completed']) > 0},
        {"name": "Мастер Цезаря", "description": "Решите 5 задач с шифром Цезаря", "completed": st.session_state.game_state['score'] > 200},
        {"name": "Криптограф", "description": "Наберите 500 очков", "completed": st.session_state.game_state['score'] >= 500},
    ]
    
    for achievement in achievements:
        col1, col2 = st.columns([3, 1])
        with col1:
            if achievement['completed']:
                st.success(f"✅ **{achievement['name']}** - {achievement['description']}")
            else:
                st.info(f"🔒 **{achievement['name']}** - {achievement['description']}")

def show_practice_tab(game, alphabet):
    st.header("⚙️ Свободная тренировка")
    
    practice_type = st.selectbox("Выберите тип шифра:", ["Шифр Цезаря", "Шифр Виженера"])
    
    if practice_type == "Шифр Цезаря":
        col1, col2 = st.columns(2)
        with col1:
            text = st.text_area("Текст для шифрования:")
            shift = st.number_input("Сдвиг:", min_value=1, max_value=33, value=3)
            if text:
                encrypted = game.caesar_encrypt(text, shift, alphabet)
                st.text_area("Зашифрованный текст:", encrypted, height=100)
        
        with col2:
            encrypted_input = st.text_area("Текст для расшифровки:")
            shift_decrypt = st.number_input("Сдвиг для расшифровки:", min_value=1, max_value=33, value=3)
            if encrypted_input:
                decrypted = game.caesar_encrypt(encrypted_input, -shift_decrypt, alphabet)
                st.text_area("Расшифрованный текст:", decrypted, height=100)

if __name__ == "__main__":
    main()
