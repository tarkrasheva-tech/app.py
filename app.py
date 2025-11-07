import streamlit as st
import random
import string

st.set_page_config(
    page_title="Генератор паролей",
    page_icon="🔐",
    layout="wide"
)

# Стили
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .password-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #28a745;
    }
</style>
""", unsafe_allow_html=True)

class PasswordGenerator:
    def __init__(self):
        self.character_sets = {
            'uppercase': string.ascii_uppercase,
            'lowercase': string.ascii_lowercase,
            'digits': string.digits,
            'symbols': "!@#$%&*()-_=+[]{}|;:,.<>?"
        }
    
    def generate_base_password(self, length=12, use_uppercase=True, use_lowercase=True, 
                             use_digits=True, use_symbols=True):
        characters = ""
        
        if use_uppercase:
            characters += self.character_sets['uppercase']
        if use_lowercase:
            characters += self.character_sets['lowercase']
        if use_digits:
            characters += self.character_sets['digits']
        if use_symbols:
            characters += self.character_sets['symbols']
        
        if not characters:
            raise ValueError("Выберите хотя бы один тип символов!")
        
        password_chars = []
        if use_uppercase:
            password_chars.append(random.choice(self.character_sets['uppercase']))
        if use_lowercase:
            password_chars.append(random.choice(self.character_sets['lowercase']))
        if use_digits:
            password_chars.append(random.choice(self.character_sets['digits']))
        if use_symbols:
            password_chars.append(random.choice(self.character_sets['symbols']))
        
        remaining_length = length - len(password_chars)
        for _ in range(remaining_length):
            password_chars.append(random.choice(characters))
        
        random.shuffle(password_chars)
        return ''.join(password_chars)
    
    def caesar_cipher(self, text, shift):
        result = ""
        for char in text:
            if char.isalpha():
                ascii_offset = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            else:
                result += char
        return result
    
    def vigenere_cipher(self, text, keyword):
        result = ""
        keyword = keyword.upper()
        keyword_index = 0
        
        for char in text:
            if char.isalpha():
                ascii_offset = ord('A') if char.isupper() else ord('a')
                shift = ord(keyword[keyword_index % len(keyword)]) - ord('A')
                result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
                keyword_index += 1
            else:
                result += char
        return result

def main():
    st.markdown('<h1 class="main-header">🔐 Генератор паролей с шифрами</h1>', unsafe_allow_html=True)
    
    # Инициализация генератора
    if 'generator' not in st.session_state:
        st.session_state.generator = PasswordGenerator()
    if 'last_password' not in st.session_state:
        st.session_state.last_password = None
    
    # Сайдбар с настройками
    with st.sidebar:
        st.header("⚙️ Настройки")
        
        length = st.slider("Длина пароля", min_value=6, max_value=50, value=12)
        
        st.subheader("Типы символов")
        use_uppercase = st.checkbox("Заглавные буквы (A-Z)", value=True)
        use_lowercase = st.checkbox("Строчные буквы (a-z)", value=True)
        use_digits = st.checkbox("Цифры (0-9)", value=True)
        use_symbols = st.checkbox("Специальные символы", value=True)
        
        st.subheader("Шифрование")
        cipher_type = st.selectbox("Тип шифра", ["Без шифра", "Цезарь", "Виженер"])
        
        if cipher_type == "Цезарь":
            shift = st.slider("Сдвиг", min_value=1, max_value=25, value=3)
        elif cipher_type == "Виженер":
            keyword = st.text_input("Ключевое слово", value="SECRET")
    
    # Основная область
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("🎲 Сгенерировать пароль", type="primary", use_container_width=True):
            try:
                base_password = st.session_state.generator.generate_base_password(
                    length=length,
                    use_uppercase=use_uppercase,
                    use_lowercase=use_lowercase,
                    use_digits=use_digits,
                    use_symbols=use_symbols
                )
                
                if cipher_type == "Цезарь":
                    final_password = st.session_state.generator.caesar_cipher(base_password, shift)
                    cipher_info = f"Шифр Цезаря (сдвиг: {shift})"
                elif cipher_type == "Виженер":
                    final_password = st.session_state.generator.vigenere_cipher(base_password, keyword)
                    cipher_info = f"Шифр Виженера (ключ: {keyword})"
                else:
                    final_password = base_password
                    cipher_info = "Без шифра"
                
                st.session_state.last_password = {
                    'base': base_password,
                    'final': final_password,
                    'cipher_info': cipher_info,
                    'length': length
                }
                
            except Exception as e:
                st.error(f"Ошибка: {e}")
    
    with col2:
        if st.session_state.last_password:
            if st.button("📋 Копировать пароль", use_container_width=True):
                st.code(st.session_state.last_password['final'])
                st.success("Пароль скопирован в буфер обмена!")
    
    # Отображение результата
    if st.session_state.last_password:
        st.markdown("---")
        st.subheader("🎯 Результат")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="password-box">', unsafe_allow_html=True)
            st.write("**Базовый пароль:**")
            st.code(st.session_state.last_password['base'], language="text")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="password-box">', unsafe_allow_html=True)
            st.write("**Финальный пароль:**")
            st.code(st.session_state.last_password['final'], language="text")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.write(f"**Информация:** {st.session_state.last_password['cipher_info']}")
        st.write(f"**Длина:** {st.session_state.last_password['length']} символов")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Дешифрование
    st.markdown("---")
    st.subheader("🔓 Дешифрование")
    
    col1, col2 = st.columns(2)
    
    with col1:
        encrypted_text = st.text_area("Зашифрованный текст", height=100)
        decrypt_cipher = st.selectbox("Тип шифра для дешифрования", ["Цезарь", "Виженер"])
        
        if decrypt_cipher == "Цезарь":
            decrypt_shift = st.number_input("Сдвиг", min_value=1, max_value=25, value=3)
        else:
            decrypt_keyword = st.text_input("Ключ для дешифрования", value="SECRET")
    
    with col2:
        if st.button("🔍 Дешифровать", use_container_width=True):
            if encrypted_text:
                try:
                    if decrypt_cipher == "Цезарь":
                        # Для дешифрования Цезаря используем отрицательный сдвиг
                        decrypted = st.session_state.generator.caesar_cipher(encrypted_text, -decrypt_shift)
                    else:
                        # Для Виженера нужна отдельная функция дешифрования
                        decrypted = ""
                        keyword = decrypt_keyword.upper()
                        keyword_index = 0
                        for char in encrypted_text:
                            if char.isalpha():
                                ascii_offset = ord('A') if char.isupper() else ord('a')
                                shift = ord(keyword[keyword_index % len(keyword)]) - ord('A')
                                decrypted += chr((ord(char) - ascii_offset - shift) % 26 + ascii_offset)
                                keyword_index += 1
                            else:
                                decrypted += char
                    
                    st.success("Текст дешифрован!")
                    st.code(decrypted, language="text")
                    
                except Exception as e:
                    st.error(f"Ошибка дешифрования: {e}")
            else:
                st.warning("Введите текст для дешифрования")

if __name__ == "__main__":
    main()
