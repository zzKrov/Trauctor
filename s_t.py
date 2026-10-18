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
# CONFIGURACIÓN GENERAL (SIN BARRA LATERAL)
# ============================================================
st.set_page_config(
    page_title="Traductor de Voz // Krov Industries",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# ATMÓSFERA VISUAL: GRADIENTES VIOLETA Y BOTÓN DE VOZ SATINADO
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"], [data-testid="stAppViewContainer"], .stApp, section.main {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background: transparent !important;
    background-color: transparent !important;
    color: #f5f5ff !important;
    overflow-x: hidden;
}

[data-testid="stHeader"] { background: transparent !important; }

/* Eliminación total de cualquier sidebar remanente */
[data-testid="stSidebar"], section[data-testid="stSidebar"] {
    display: none !important;
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

.main-title {
    font-size: 2.2rem;
    font-weight: 700;
    text-align: center;
    color: #ffffff;
    margin-bottom: 0.2rem;
    text-shadow: 0 0 25px rgba(168, 85, 247, 0.45);
}

.sub-lead {
    text-align: center;
    color: #c4b5fd;
    font-size: 0.95rem;
    margin-bottom: 1.8rem;
}

/* SUPRESIÓN DEL RECUADRO BLANCO DE BOKEH */
iframe[title="streamlit_bokeh_events.streamlit_bokeh_events"] {
    background: transparent !important;
    border: none !important;
    display: block !important;
    margin: 0 auto !important;
}

.recording-badge-box {
    text-align: center;
    margin: 10px auto 16px auto;
    padding: 12px 24px;
    background: rgba(124, 58, 237, 0.12);
    border: 1px solid rgba(168, 85, 247, 0.35);
    border-radius: 30px;
    width: fit-content;
    backdrop-filter: blur(14px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
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

.trans-card {
    background: rgba(15, 10, 40, 0.85);
    border: 1px solid rgba(168, 85, 247, 0.3);
    border-left: 4px solid #a855f7;
    border-radius: 8px;
    padding: 1.2rem;
    margin: 1rem 0;
    font-size: 1.05rem;
    color: #ffffff;
    backdrop-filter: blur(14px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6);
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# LÁMPARA DE LAVA FLUIDA AMATISTA EN CANVAS
# ---------------------------------------------------------
components.html(
    """
    <script>
    (function() {
        const doc = window.parent.document;
        let canvas = doc.getElementById('voice-lava-canvas');
        if (!canvas) {
            canvas = doc.createElement('canvas');
            canvas.id = 'voice-lava-canvas';
            canvas.style.cssText = 'position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:0;background:#080414;';
            doc.body.prepend(canvas);
        }

        const ctx = canvas.getContext('2d');
        let w = canvas.width = window.parent.innerWidth;
        let h = canvas.height = window.parent.innerHeight;

        window.parent.addEventListener('resize', () => {
            w = canvas.width = window.parent.innerWidth;
            h = canvas.height = window.parent.innerHeight;
        });

        // Fluidos orgánicos violeta y magenta
        const blobs = [
            { x: w * 0.2, y: h * 0.25, r: 260, vx: 0.5, vy: 0.4, color: 'rgba(168, 85, 247, 0.16)' },
            { x: w * 0.75, y: h * 0.35, r: 290, vx: -0.4, vy: 0.5, color: 'rgba(236, 72, 153, 0.15)' },
            { x: w * 0.35, y: h * 0.75, r: 270, vx: 0.4, vy: -0.5, color: 'rgba(124, 58, 237, 0.14)' },
            { x: w * 0.8, y: h * 0.8, r: 240, vx: -0.5, vy: -0.4, color: 'rgba(219, 39, 119, 0.12)' }
        ];

        let mouse = { x: -1000, y: -1000 };
        const sparkles = [];

        window.parent.addEventListener('mousemove', (e) => {
            mouse.x = e.clientX;
            mouse.y = e.clientY;
            for (let i = 0; i < 2; i++) {
                sparkles.push({
                    x: e.clientX,
                    y: e.clientY,
                    r: Math.random() * 2 + 0.8,
                    vx: (Math.random() - 0.5) * 1.5,
                    vy: (Math.random() - 0.5) * 1.5,
                    alpha: 1.0
                });
            }
        });

        function animate() {
            ctx.clearRect(0, 0, w, h);
            ctx.fillStyle = '#080414';
            ctx.fillRect(0, 0, w, h);
            ctx.globalCompositeOperation = 'screen';

            for (let b of blobs) {
                b.x += b.vx;
                b.y += b.vy;

                if (b.x < -100 || b.x > w + 100) b.vx *= -1;
                if (b.y < -100 || b.y > h + 100) b.vy *= -1;

                const dm = Math.hypot(b.x - mouse.x, b.y - mouse.y);
                if (dm < 280) {
                    b.x += (mouse.x - b.x) * 0.008;
                    b.y += (mouse.y - b.y) * 0.008;
                }

                const grad = ctx.createRadialGradient(b.x, b.y, b.r * 0.05, b.x, b.y, b.r);
                grad.addColorStop(0, b.color);
                grad.addColorStop(1, 'transparent');

                ctx.beginPath();
                ctx.arc(b.x, b.y, b.r, 0, Math.PI * 2);
                ctx.fillStyle = grad;
                ctx.fill();
            }

            for (let i = sparkles.length - 1; i >= 0; i--) {
                const s = sparkles[i];
                s.x += s.vx;
                s.y += s.vy;
                s.alpha -= 0.025;
                if (s.alpha <= 0) {
                    sparkles.splice(i, 1);
                    continue;
                }
                ctx.beginPath();
                ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(236, 72, 153, ${s.alpha})`;
                ctx.shadowBlur = 8;
                ctx.shadowColor = '#ec4899';
                ctx.fill();
            }

            ctx.globalCompositeOperation = 'source-over';
            requestAnimationFrame(animate);
        }
        animate();
    })();
    </script>
    """,
    height=0,
    width=0
)

# ============================================================
# ENCABEZADO
# ============================================================
st.markdown('<div class="brand-signature">Krov Industries · Procesamiento Acústico</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">Traductor de Voz a Audio</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-lead">Reconocimiento oral continuo, traducción multilingüe y síntesis vocal en tiempo real</div>', unsafe_allow_html=True)

# ------------------------------------------------------------
# BOTÓN REDONDEADO INTERACTIVO CON MUTACIÓN DE ESTADOS
# ------------------------------------------------------------
st.markdown(
    """
    <div class="recording-badge-box">
        <div style="display:flex; justify-content:center; align-items:center; gap:8px;">
            <div class="soundwave-bar"></div>
            <div class="soundwave-bar"></div>
            <div class="soundwave-bar"></div>
            <div class="soundwave-bar"></div>
            <div class="soundwave-bar"></div>
            <span style="font-family:'JetBrains Mono'; font-size:0.82rem; color:#e9d5ff; margin-left:8px;">
                CANAL DE AUDIO LISTO // PULSA EL BOTÓN INFERIOR
            </span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

stt_button = Button(
    label="Iniciar grabación de voz 🎤",
    width=340,
    height=54
)

stt_button.js_on_event(
    "button_click",
    CustomJS(code="""
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            alert('El reconocimiento de voz no está soportado en este navegador. Utiliza Google Chrome o Microsoft Edge.');
            return;
        }

        var btnEl = document.querySelector('.bk-btn');
        if (btnEl) {
            btnEl.innerText = "🔴 Escuchando... Habla ahora";
            btnEl.style.background = "linear-gradient(135deg, #f43f5e 0%, #be123c 100%)";
            btnEl.style.boxShadow = "0 0 35px rgba(244, 63, 94, 0.9)";
            btnEl.style.borderColor = "#f43f5e";
        }

        var SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
        var recognition = new SpeechRec();
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
                if (btnEl) {
                    btnEl.innerText = "✨ Transcripción completada";
                    btnEl.style.background = "linear-gradient(135deg, #059669 0%, #10b981 100%)";
                    btnEl.style.boxShadow = "0 0 30px rgba(16, 185, 129, 0.7)";
                    btnEl.style.borderColor = "#10b981";
                }
                document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
            }
        };

        recognition.onerror = function(event) {
            console.error('Error de micrófono:', event.error);
            if (btnEl) {
                btnEl.innerText = "⚠️ Error de micrófono - Reintentar";
                btnEl.style.background = "linear-gradient(135deg, #d97706 0%, #b45309 100%)";
                btnEl.style.boxShadow = "0 0 25px rgba(217, 119, 6, 0.7)";
                btnEl.style.borderColor = "#d97706";
            }
        };

        recognition.start();
    """)
)

# Inyección permanente que erradica el fondo blanco dentro del iframe de Bokeh
components.html(
    """
    <script>
    setInterval(() => {
        const iframes = window.parent.document.querySelectorAll('iframe');
        iframes.forEach(f => {
            try {
                const doc = f.contentDocument || f.contentWindow.document;
                if (doc && doc.querySelector('.bk-btn') && !doc.getElementById('krov-bokeh-fix-final')) {
                    doc.body.style.background = 'transparent';
                    doc.documentElement.style.background = 'transparent';
                    const style = doc.createElement('style');
                    style.id = 'krov-bokeh-fix-final';
                    style.innerHTML = `
                        html, body { background: transparent !important; margin: 0 !important; overflow: hidden !important; }
                        .bk-root { background: transparent !important; display: flex !important; justify-content: center !important; }
                        .bk-btn, .bk-btn-default {
                            background: linear-gradient(135deg, #7c3aed 0%, #a855f7 50%, #ec4899 100%) !important;
                            color: #ffffff !important;
                            border: 2px solid rgba(236, 72, 153, 0.7) !important;
                            border-radius: 9999px !important;
                            font-family: 'Plus Jakarta Sans', sans-serif !important;
                            font-weight: 700 !important;
                            font-size: 1rem !important;
                            letter-spacing: 0.04em !important;
                            padding: 12px 32px !important;
                            box-shadow: 0 0 30px rgba(168, 85, 247, 0.5) !important;
                            cursor: pointer !important;
                            transition: all 0.3s ease !important;
                            outline: none !important;
                        }
                        .bk-btn:hover {
                            transform: translateY(-2px) scale(1.02) !important;
                            box-shadow: 0 0 45px rgba(236, 72, 153, 0.8) !important;
                        }
                    `;
                    doc.head.appendChild(style);
                }
            } catch(e) {}
        });
    }, 150);
    </script>
    """,
    height=0,
    width=0
)

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen_final",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0
)

if result and "GET_TEXT" in result:
    st.session_state["captured_text"] = str(result.get("GET_TEXT"))

# ------------------------------------------------------------
# PANEL INTEGRADO EN PANTALLA PANORÁMICA (SIN SIDEBAR)
# ------------------------------------------------------------
c_left, c_right = st.columns([1.1, 1], gap="large")

with c_left:
    st.markdown("### 1. Texto detectado")
    texto_actual = st.text_area(
        "Transcripción editable:",
        value=st.session_state.get("captured_text", ""),
        placeholder="Presiona 'Iniciar grabación de voz' o escribe directamente aquí el texto...",
        height=140
    )

with c_right:
    st.markdown("### 2. Configuración de destino")
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        in_lang = st.selectbox(
            "Idioma de origen:",
            ("Español", "Inglés", "Bengali", "Coreano", "Mandarín", "Japonés", "Ruso", "Alemán"),
            index=0
        )
    with col_l2:
        out_lang = st.selectbox(
            "Idioma a traducir:",
            ("Inglés", "Español", "Bengali", "Coreano", "Mandarín", "Japonés", "Ruso", "Alemán"),
            index=0
        )

    english_accent = st.selectbox(
        "Acento del sintetizador de voz:",
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

    traducir_btn = st.button("Convertir y reproducir audio traducido", use_container_width=True)

if traducir_btn:
    if not texto_actual.strip():
        st.warning("Primero debes capturar voz o ingresar texto en el panel izquierdo.")
    else:
        with st.spinner("Traduciendo y generando audio..."):
            try:
                os.makedirs("temp", exist_ok=True)
                translator = Translator()
                translation = translator.translate(texto_actual, src=input_language, dest=output_language)
                trans_text = translation.text

                tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
                safe_name = "".join(c for c in texto_actual[:20] if c.isalnum() or c in (" ", "_")).strip() or "audio"
                file_path = f"temp/{safe_name}_{int(time.time())}.mp3"
                tts.save(file_path)

                st.markdown(f'<div class="trans-card"><b>Traducción ({out_lang}):</b> {trans_text}</div>', unsafe_allow_html=True)

                with open(file_path, "rb") as af:
                    st.audio(af.read(), format="audio/mp3", start_time=0)

            except Exception as e:
                st.error(f"Error durante el proceso de traducción o síntesis: {e}")

def limpiar_archivos_antiguos(days=7):
    for f in glob.glob("temp/*.mp3"):
        if os.stat(f).st_mtime < time.time() - (days * 86400):
            try:
                os.remove(f)
            except Exception:
                pass

limpiar_archivos_antiguos()
