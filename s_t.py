import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
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
# ESTILOS VISUALES: SUPRESIÓN DEL RECUADRO BLANCO DE BOKEH
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(168, 85, 247, 0.12), transparent 30%),
        radial-gradient(circle at 90% 20%, rgba(236, 72, 153, 0.12), transparent 28%),
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
    margin-bottom: 4px;
}

h1 {
    font-size: 2.3rem !important;
    font-weight: 700 !important;
    text-align: center;
    color: #ffffff !important;
    margin-bottom: 0.2rem !important;
}

/* Supresión absoluta del fondo blanco de Bokeh y estilización moderna */
iframe[title="streamlit_bokeh_events.streamlit_bokeh_events"] {
    background: transparent !important;
    border: none !important;
    display: block !important;
    margin: 0 auto !important;
}

.bk-root {
    background: transparent !important;
}

.bk-root .bk-btn, .bk-root .bk-btn-default {
    background: linear-gradient(135deg, #7c3aed, #db2777) !important;
    color: #ffffff !important;
    border: 1px solid rgba(168, 85, 247, 0.5) !important;
    border-radius: 28px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    letter-spacing: 0.05em !important;
    box-shadow: 0 0 25px rgba(168, 85, 247, 0.4) !important;
    transition: all 0.25s ease !important;
}

.bk-root .bk-btn:hover {
    transform: translateY(-2px) scale(1.02) !important;
    box-shadow: 0 0 35px rgba(236, 72, 153, 0.6) !important;
}

.recording-status-box {
    text-align: center;
    margin: 10px auto 16px auto;
    padding: 10px;
    background: rgba(124, 58, 237, 0.1);
    border: 1px solid rgba(168, 85, 247, 0.25);
    border-radius: 8px;
    max-width: 500px;
}

.wave-pulse {
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #ec4899;
    box-shadow: 0 0 12px #ec4899;
    margin-right: 8px;
    animation: wavePulse 1.2s infinite ease-in-out;
}

@keyframes wavePulse {
    0%, 100% { transform: scale(0.8); opacity: 0.5; }
    50% { transform: scale(1.3); opacity: 1; }
}

.trans-result-card {
    background: #0f0a28;
    border: 1px solid rgba(168, 85, 247, 0.25);
    border-left: 4px solid #a855f7;
    border-radius: 8px;
    padding: 1.2rem;
    margin: 1rem 0;
    font-size: 1.05rem;
    color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# ENCABEZADO
# ============================================================
st.markdown('<div class="brand-signature">Krov Industries · Procesamiento Acústico</div>', unsafe_allow_html=True)
st.title("Traductor de Voz a Audio")
st.markdown("<p style='text-align:center; color:#c4b5fd; font-size:0.95rem; margin-bottom:1.5rem;'>Reconocimiento oral continuo, traducción multilingüe y síntesis vocal</p>", unsafe_allow_html=True)

with st.sidebar:
    st.subheader("Instrucciones")
    st.write(
        "1. Haz clic en el botón de escucha y permite el acceso al micrófono en el navegador.\n"
        "2. Habla con claridad.\n"
        "3. Elige los idiomas de entrada y salida.\n"
        "4. Presiona «Convertir y reproducir audio» para generar la voz traducida."
    )

st.markdown(
    """
    <div class="recording-status-box">
        <span class="wave-pulse"></span>
        <span style="font-family:'JetBrains Mono'; font-size:0.8rem; color:#e9d5ff;">MICRÓFONO LISTO // PULSA EL BOTÓN INFERIOR</span>
    </div>
    """,
    unsafe_allow_html=True
)

stt_button = Button(
    label="Escuchar voz 🎤",
    width=340,
    height=52
)

stt_button.js_on_event(
    "button_click",
    CustomJS(code="""
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            alert('El reconocimiento de voz no está soportado en este navegador. Utiliza Google Chrome o Edge.');
            return;
        }
        var SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
        var recognition = new SpeechRec();
        recognition.continuous = false;
        recognition.interimResults = true;
        recognition.lang = 'es-ES';

        recognition.onstart = function() {
            console.log('Captura de voz iniciada');
        };

        recognition.onresult = function (e) {
            var value = "";
            for (var i = e.resultIndex; i < e.results.length; ++i) {
                if (e.results[i].isFinal) {
                    value += e.results[i][0].transcript;
                }
            }
            if (value != "") {
                document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
            }
        };

        recognition.onerror = function(event) {
            console.error('Error de micrófono:', event.error);
        };

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

if result and "GET_TEXT" in result:
    st.session_state["recognized_voice_text"] = str(result.get("GET_TEXT"))

current_text = st.session_state.get("recognized_voice_text", "")

if current_text:
    st.markdown(f'<div class="trans-result-card"><b>Texto transcrito:</b> {current_text}</div>', unsafe_allow_html=True)
    os.makedirs("temp", exist_ok=True)
    translator = Translator()

    col_l1, col_l2, col_l3 = st.columns(3)
    with col_l1:
        in_lang = st.selectbox(
            "Idioma de entrada:",
            ("Español", "Inglés", "Bengali", "Coreano", "Mandarín", "Japonés", "Ruso", "Alemán"),
            index=0
        )
    with col_l2:
        out_lang = st.selectbox(
            "Idioma de destino:",
            ("Inglés", "Español", "Bengali", "Coreano", "Mandarín", "Japonés", "Ruso", "Alemán"),
            index=0
        )
    with col_l3:
        english_accent = st.selectbox(
            "Acento del sintetizador:",
            ("Defecto", "Español", "Reino Unido", "Estados Unidos", "Canada", "Australia", "Irlanda", "Sudáfrica")
        )

    lang_map = {
        "Inglés": "en", "Español": "es", "Bengali": "bn", "Coreano": "ko",
        "Mandarín": "zh-cn", "Japonés": "ja", "Ruso": "ru", "Alemán": "de"
    }
    accent_map = {
        "Defecto": "com", "Español": "com.mx", "Reino Unido": "co.uk",
        "Estados Unidos": "com", "Canada": "ca", "Australia": "com.au",
        "Irlanda": "ie", "Sudáfrica": "co.za"
    }

    input_language = lang_map.get(in_lang, "es")
    output_language = lang_map.get(out_lang, "en")
    tld = accent_map.get(english_accent, "com")

    display_output_text = st.checkbox("Mostrar texto traducido", value=True)

    if st.button("Convertir y reproducir audio", use_container_width=True):
        with st.spinner("Traduciendo y sintetizando audio..."):
            try:
                translation = translator.translate(current_text, src=input_language, dest=output_language)
                trans_text = translation.text
                tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
                
                safe_name = "".join(c for c in current_text[:20] if c.isalnum() or c in (" ", "_")).strip() or "audio"
                file_path = f"temp/{safe_name}.mp3"
                tts.save(file_path)

                with open(file_path, "rb") as af:
                    audio_bytes = af.read()

                st.markdown("### Audio traducido:")
                st.audio(audio_bytes, format="audio/mp3", start_time=0)

                if display_output_text:
                    st.markdown(f'<div class="trans-result-card"><b>Traducción:</b> {trans_text}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error durante la traducción o síntesis: {e}")

def remove_files(days):
    for f in glob.glob("temp/*.mp3"):
        if os.stat(f).st_mtime < time.time() - (days * 86400):
            try:
                os.remove(f)
            except Exception:
                pass

remove_files(7)
