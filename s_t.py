import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob

from gtts import gTTS
from googletrans import Translator

# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================
st.set_page_config(
    page_title="Traductor de Voz // Krov Industries",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# ESTILOS VISUALES
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(168, 85, 247, 0.12), transparent 30%),
        radial-gradient(circle at 90% 20%, rgba(236, 72, 153, 0.14), transparent 28%),
        radial-gradient(circle at 50% 100%, rgba(99, 102, 241, 0.12), transparent 35%),
        #080414;
    color: #f5f5ff;
}

.brand-signature {
    text-align: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    color: #a855f7;
    text-transform: uppercase;
    margin-bottom: 6px;
}

h1 {
    font-size: 2.6rem !important;
    font-weight: 700 !important;
    text-align: center;
    color: #ffffff !important;
    margin-bottom: 0.3rem !important;
}

.sub-header-text {
    text-align: center;
    color: #d1d5db;
    font-size: 1.05rem;
    margin-bottom: 1.8rem;
}

section[data-testid="stSidebar"] {
    background: #0d0722;
    border-right: 1px solid rgba(168, 85, 247, 0.2);
}

.stButton > button {
    width: 100%;
    min-height: 50px;
    border-radius: 8px;
    background: linear-gradient(135deg, #7c3aed, #db2777);
    border: none;
    color: white;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    transition: all 0.25s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 25px rgba(168, 85, 247, 0.5);
}

.trans-result-card {
    background: #0f0a28;
    border: 1px solid rgba(168, 85, 247, 0.25);
    border-left: 4px solid #a855f7;
    border-radius: 8px;
    padding: 1.25rem;
    margin: 1.2rem 0;
    font-size: 1.1rem;
    color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# ENCABEZADO
# ============================================================
st.markdown('<div class="brand-signature">Krov Industries · Procesamiento Acústico</div>', unsafe_allow_html=True)
st.title("Traductor de Voz a Audio")
st.markdown('<div class="sub-header-text">Reconocimiento de voz continuo, traducción y síntesis de audio</div>', unsafe_allow_html=True)

with st.sidebar:
    st.subheader("Instrucciones")
    st.write(
        "1. Presiona el botón de escuchar y concede permisos de micrófono.\n"
        "2. Pronuncia con claridad la frase que deseas traducir.\n"
        "3. Elige los idiomas y la modulación de acento deseada.\n"
        "4. Presiona Convertir para generar el audio traducido."
    )

st.write("Presiona el botón para activar el reconocimiento de voz:")

stt_button = Button(
    label="Escuchar voz 🎤",
    width=320,
    height=50
)

stt_button.js_on_event(
    "button_click",
    CustomJS(code="""
        var recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = true;
        recognition.lang = 'es-ES';

        recognition.onresult = function (e) {
            var value = "";
            for (var i = e.resultIndex; i < e.results.length; ++i) {
                if (e.results[i].isFinal) {
                    value += e.results[i][0].transcript;
                }
            }
            if (value != "") {
                document.dispatchEvent(
                    new CustomEvent(
                        "GET_TEXT",
                        {detail: value}
                    )
                );
            }
        }
        recognition.onend = function() {
            console.log("Reconocimiento de voz finalizado");
        }
        recognition.start();
    """)
)

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0
)

if result:
    if "GET_TEXT" in result:
        st.markdown(f'<div class="trans-result-card"><b>Texto detectado:</b> {result.get("GET_TEXT")}</div>', unsafe_allow_html=True)

    try:
        os.makedirs("temp", exist_ok=True)
    except Exception:
        pass

    translator = Translator()
    text = str(result.get("GET_TEXT"))

    col_l1, col_l2, col_l3 = st.columns(3)

    with col_l1:
        in_lang = st.selectbox(
            "Idioma de entrada:",
            ("Español", "Inglés", "Bengali", "Coreano", "Mandarín", "Japonés", "Ruso", "Alemán"),
            index=0
        )

    lang_map = {
        "Inglés": "en", "Español": "es", "Bengali": "bn", "Coreano": "ko",
        "Mandarín": "zh-cn", "Japonés": "ja", "Ruso": "ru", "Alemán": "de"
    }
    input_language = lang_map.get(in_lang, "es")

    with col_l2:
        out_lang = st.selectbox(
            "Idioma de destino:",
            ("Inglés", "Español", "Bengali", "Coreano", "Mandarín", "Japonés", "Ruso", "Alemán"),
            index=0
        )
    output_language = lang_map.get(out_lang, "en")

    with col_l3:
        english_accent = st.selectbox(
            "Acento de modulación:",
            ("Defecto", "Español", "Reino Unido", "Estados Unidos", "Canada", "Australia", "Irlanda", "Sudáfrica")
        )

    accent_map = {
        "Defecto": "com", "Español": "com.mx", "Reino Unido": "co.uk",
        "Estados Unidos": "com", "Canada": "ca", "Australia": "com.au",
        "Irlanda": "ie", "Sudáfrica": "co.za"
    }
    tld = accent_map.get(english_accent, "com")

    def text_to_speech(input_language, output_language, text, tld):
        translation = translator.translate(text, src=input_language, dest=output_language)
        trans_text = translation.text
        tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
        try:
            my_file_name = "".join(c for c in text[:20] if c.isalnum() or c in (" ", "_")).strip()
            if not my_file_name:
                my_file_name = "audio"
        except Exception:
            my_file_name = "audio"

        tts.save(f"temp/{my_file_name}.mp3")
        return my_file_name, trans_text

    display_output_text = st.checkbox("Mostrar texto traducido en pantalla", value=True)

    if st.button("Convertir y reproducir audio", use_container_width=True):
        try:
            result_file, output_text = text_to_speech(input_language, output_language, text, tld)
            audio_path = f"temp/{result_file}.mp3"

            with open(audio_path, "rb") as audio_file:
                audio_bytes = audio_file.read()

            st.markdown("### Audio traducido:")
            st.audio(audio_bytes, format="audio/mp3", start_time=0)

            if display_output_text:
                st.markdown("### Texto traducido:")
                st.markdown(f'<div class="trans-result-card">{output_text}</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error al traducir o generar el archivo de audio: {e}")

    def remove_files(n):
        mp3_files = glob.glob("temp/*.mp3")
        if len(mp3_files) != 0:
            now = time.time()
            n_days = n * 86400
            for f in mp3_files:
                if os.stat(f).st_mtime < now - n_days:
                    try:
                        os.remove(f)
                    except Exception:
                        pass

    remove_files(7)
