import streamlit as st
from googletrans import Translator, LANGUAGES
import pyperclip
from gtts import gTTS
import tempfile
import os
import pyttsx3
import socket

# -------------------------------
# Page setup
# -------------------------------
st.set_page_config(page_title="Language Translation Tool", page_icon="🌐", layout="centered")

st.title("🌐 Language Translation Tool")
st.markdown("Translate text between languages using Google Translate API")

translator = Translator()

# -------------------------------
# Input section
# -------------------------------
text = st.text_area("Enter text to translate", height=150)

col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("Select Source Language", options=list(LANGUAGES.values()), index=21)
with col2:
    target_lang = st.selectbox("Select Target Language", options=list(LANGUAGES.values()), index=38)

# -------------------------------
# Translate Button
# -------------------------------
if st.button("🔁 Translate"):
    if text.strip():
        try:
            src_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(source_lang)]
            tgt_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(target_lang)]

            result = translator.translate(text, src=src_code, dest=tgt_code)
            translated_text = result.text

            # Save translation in session state
            st.session_state['translated_text'] = translated_text
            st.session_state['tgt_code'] = tgt_code

        except Exception as e:
            st.error(f"Translation Error: {str(e)}")
    else:
        st.warning("Please enter text to translate.")


# -------------------------------
# Display stored translation (always visible)
# -------------------------------
if 'translated_text' in st.session_state:
    translated_text = st.session_state['translated_text']
    tgt_code = st.session_state.get('tgt_code', 'en')
    target_lang = list(LANGUAGES.values())[list(LANGUAGES.keys()).index(tgt_code)]

    st.success(f"**Translated Text ({target_lang}):**")
    st.write(translated_text)

    # Buttons side by side
    col1, col2 = st.columns(2)

    # Copy Button
    with col1:
        if st.button("📋 Copy Translation"):
            pyperclip.copy(translated_text)
            st.info("Translation copied to clipboard!")

    # Listen Button
    with col1:
        def check_internet():
            try:
                socket.create_connection(("www.google.com", 80), timeout=3)
                return True
            except OSError:
                return False

        if st.button("🔊 Listen"):
            try:
                if check_internet():
                    # --- Online mode (gTTS) ---
                    lang_code = tgt_code if tgt_code in [
                        'en', 'fr', 'de', 'es', 'ta', 'hi', 'ar', 'zh-cn', 'ja', 'ko'
                    ] else 'en'
                    tts = gTTS(text=translated_text, lang=lang_code)
                    temp_path = os.path.join(tempfile.gettempdir(), "speech.mp3")
                    tts.save(temp_path)

                    with open(temp_path, "rb") as audio_file:
                        st.audio(audio_file.read(), format="audio/mp3")
                    st.success("🔊 Audio generated using Google TTS")
                else:
                    # --- Offline mode (pyttsx3) ---
                    engine = pyttsx3.init()
                    engine.say(translated_text)
                    engine.runAndWait()
                    st.success("🗣️ Spoken using Offline TTS (pyttsx3)")
            except Exception as e:
                st.error(f"Text-to-Speech Error: {str(e)}")
                
      
# -------------------------------
# Footer (Always at the Bottom)
# -------------------------------
st.markdown("---")
st.markdown(
    """
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: transparent;
            text-align: left; /* Aligns content to the beginning of the line */
            padding: 10px 40px; /* Adds a bit of spacing from the left edge */
            font-size: 22px;
            color: #d1d1d1;
            line-height: 1.5;
        }
    </style>
    <div class="footer">
        <p>👨‍💻 Developed by: <b>Hamjathali I</b></p>
        <p>💡 Idea: <i>Language Translation Tool
        <p>🛠️ Tech Stack: Python, Streamlit, Googletrans API, gTTS, pyttsx3, Pyperclip <p>
    </div>
    """,
    unsafe_allow_html=True
)




