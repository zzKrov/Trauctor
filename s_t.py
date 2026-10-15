import os
import streamlit as st
import streamlit.components.v1 as components
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
# LÍNEA BASE VISUAL: GRADIENTES VIOLETA, FLUIDOS Y BOKEH MODERNO
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* 1. Fondo de gradiente multicolor animado */
.stApp {
    background: linear-gradient(135deg, #080414 0%, #150826 30%, #20072b 60%, #0a0416 100%) !important;
    background-size: 300% 300% !important;
    animation: purpleGradient 18s ease infinite alternate !important;
    color: #f5f5ff;
}

@keyframes purpleGradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* 2. Esferas orgánicas de plasma ultravioleta */
.fluid-violet-1 {
    position: fixed;
    top: 15%;
    left: -120px;
    width: 520px;
    height: 520px;
    background: radial-gradient(circle, rgba(168, 85, 247, 0.16) 0%, rgba(236, 72, 153, 0.04) 55%, transparent 75%);
    border-radius: 40% 60% 70% 30% / 50% 60% 40% 50%;
    filter: blur(85px);
    animation: violetDrift1 20s infinite alternate ease-in-out;
    pointer-events: none;
    z-index: 0;
}

.fluid-violet-2 {
    position: fixed;
    bottom: 5%;
    right: -100px;
    width: 560px;
    height: 560px;
    background: radial-gradient(circle, rgba(236, 72, 153, 0.14) 0%, rgba(168, 85, 247, 0.03) 55%, transparent 75%);
    border-radius: 60% 40% 50% 50% / 40% 50% 60% 50%;
    filter: blur(90px);
    animation: violetDrift2 24s infinite alternate ease-in-out;
    pointer-events: none;
    z-index: 0;
}

@keyframes violetDrift1 {
    0% { transform: translate(0, 0) scale(1); }
    50% { transform: translate(120px, 70px) scale(1.15); }
    100% { transform: translate(40px, 150px) scale(0.95); }
}

@keyframes violetDrift2 {
    0% { transform: translate(0, 0) scale(1); }
    50% { transform: translate(-110px, -80px) scale(1.2); }
    100% { transform: translate(-30px, -130px) scale(0.9); }
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
    text-shadow: 0 0 25px rgba(168, 85, 247, 0.4);
}

/* Supresión total del recuadro blanco de Bokeh */
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
    background: linear-gradient(135deg, #7c3aed, #ec4899) !important;
    color: #ffffff !important;
    border: 1px solid rgba(236, 72, 153, 0.6) !important;
    border-radius: 28px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    letter-spacing: 0.05em !important;
    box-shadow: 0 0 25px rgba(168, 85, 247, 0.45) !important;
    transition: all 0.25s ease !important;
}

.bk-root .bk-btn:hover {
    transform: translateY(-2px) scale(1.02) !important;
    box-shadow: 0 0 35px rgba(236, 72, 153, 0.65) !important;
}

.recording-status-box {
    text-align: center;
    margin: 10px auto 16px auto;
    padding: 12px;
    background: rgba(124, 58, 237, 0.12);
    border: 1px solid rgba(168, 85, 247, 0.3);
    border-radius: 8px;
    max-width: 520px;
    backdrop-filter: blur(10px);
}

.soundwave-bar {
    display: inline-block;
    width: 4px;
    background: #ec4899;
    border-radius: 2px;
    margin: 0 2px;
    animation: waveBounce 0.8s infinite ease-in-out alternate;
}
.soundwave-bar:nth-child(1) { height: 12px; animation-delay: 0.1s; }
.soundwave-bar:nth-child(2) { height: 22px; animation-delay: 0.3s; }
.soundwave-bar:nth-child(3) { height: 16px; animation-delay: 0.2s; }
.soundwave-bar:nth-child(4) { height: 26px; animation-delay: 0.4s; }
.soundwave-bar:nth-child(5) { height: 14px; animation-delay: 0.15s; }

@keyframes waveBounce {
    0% { transform: scaleY(0.4); }
    100% { transform: scaleY(1.2); }
}

.trans-result-card {
    background: rgba(15, 10, 40, 0.85);
    border: 1px solid rgba(168, 85, 247, 0.3);
    border-left: 4px solid #a855f7;
    border-radius: 8px;
    padding: 1.2rem;
    margin: 1rem 0;
    font-size: 1.05rem;
    color: #ffffff;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6);
}
</style>

<div class="fluid-violet-1"></div>
<div class="fluid-violet-2"></div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# PARTÍCULAS ACÚSTICAS Y ESTELA DE MOUSE
# ---------------------------------------------------------
components.html(
    """
    <script>
    const pDoc = window.parent.document;
    if (!pDoc.getElementById('sound-particles-canvas')) {
        const canvas = pDoc.createElement('canvas');
        canvas.id = 'sound-particles-canvas';
        canvas.style.cssText = 'position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:1;opacity:0.6;';
        pDoc.body.prepend(canvas);

        const ctx = canvas.getContext('2d');
        let w = canvas.width = window.parent.innerWidth;
        let h = canvas.height = window.parent.innerHeight;

        window.parent.addEventListener('resize', () => {
            w = canvas.width = window.parent.innerWidth;
            h = canvas.height = window.parent.innerHeight;
        });

        const particles = [];
        for (let i = 0; i < 40; i++) {
            particles.push({
                x: Math.random() * w,
                y: Math.random() * h,
                r: Math.random() * 2.2 + 0.8,
                vx: (Math.random() - 0.5) * 0.4,
                vy: (Math.random() - 0.5) * 0.4 - 0.3,
                alpha: Math.random() * 0.7 + 0.3
            });
        }

        let mouse = { x: -1000, y: -1000 };
        window.parent.addEventListener('mousemove', (e) => {
            mouse.x = e.clientX;
            mouse.y = e.clientY;
        });

        function render() {
            ctx.clearRect(0, 0, w, h);
            for (let i = 0; i < particles.length; i++) {
                const p = particles[i];
                p.x += p.vx; p.y += p.vy;
                if (p.x < 0) p.x = w; if (p.x > w) p.x = 0;
                if (p.y < 0) p.y = h; if (p.y > h) p.y = 0;

                ctx.beginPath();
                ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(168, 85, 247, ${p.alpha})`;
                ctx.shadowBlur = 8;
                ctx.shadowColor = '#ec4899';
                ctx.fill();

                const d = Math.hypot(p.x - mouse.x, p.y - mouse.y);
                if (d < 110) {
                    ctx.beginPath();
                    ctx.moveTo(p.x, p.y);
                    ctx.lineTo(mouse.x, mouse.y);
                    ctx.strokeStyle = `rgba(236, 72, 153, ${0.45 * (1 - d / 110)})`;
                    ctx.lineWidth = 0.8;
                    ctx.stroke();
                }
            }
            requestAnimationFrame(render);
        }
        render();
    }
    </script>
    """,
    height=0,
    width=0
)

# ============================================================
# ENCABEZADO
# ============================================================
st.markdown('<div class="brand-signature">Krov Industries · Procesamiento Acústico</div>', unsafe_allow_html=True)
st.title("Traductor de Voz a Audio")
st.markdown("<p style='text-align:center; color:#c4b5fd; font-size:0.95rem; margin-bottom:1.5rem;'>Reconocimiento oral continuo, traducción multilingüe y síntesis vocal</p>", unsafe_allow_html=True)

with st.sidebar:
    st.subheader("Instrucciones")
    st.write(
        "1. Haz clic en el botón de escucha y autoriza el micrófono en el navegador.\n"
        "2. Pronuncia con claridad la frase deseada.\n"
        "3. Elige los idiomas de entrada y salida.\n"
        "4. Presiona «Convertir y reproducir audio» para generar la voz traducida."
    )

st.markdown(
    """
    <div class="recording-status-box">
        <div style="display:flex; justify-content:center; align-items:center; gap:8px;">
            <div class="soundwave-bar"></div>
            <div class="soundwave-bar"></div>
            <div class="soundwave-bar"></div>
            <div class="soundwave-bar"></div>
            <div class="soundwave-bar"></div>
            <span style="font-family:'JetBrains Mono'; font-size:0.82rem; color:#e9d5ff; margin-left:8px;">MICRÓFONO LISTO // PULSA EL BOTÓN INFERIOR</span>
        </div>
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
