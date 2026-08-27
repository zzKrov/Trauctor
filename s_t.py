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
# VISUAL OVERHAUL
# ============================================================

st.set_page_config(
    page_title="TRADUCTOR.",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

/* -----------------------------------------------------------
   GLOBAL
----------------------------------------------------------- */

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(0, 255, 255, 0.12), transparent 25%),
        radial-gradient(circle at 90% 20%, rgba(160, 0, 255, 0.14), transparent 28%),
        radial-gradient(circle at 50% 100%, rgba(0, 100, 255, 0.12), transparent 30%),
        #050509;
    color: #f5f5ff;
    overflow-x: hidden;
}

/* Animated background bloom */

.stApp::before {
    content: "";
    position: fixed;
    width: 650px;
    height: 650px;
    left: -300px;
    top: 20%;
    border-radius: 50%;
    background: rgba(0, 255, 255, 0.08);
    filter: blur(100px);
    animation: floatBloom1 12s ease-in-out infinite alternate;
    pointer-events: none;
    z-index: 0;
}

.stApp::after {
    content: "";
    position: fixed;
    width: 600px;
    height: 600px;
    right: -250px;
    bottom: 5%;
    border-radius: 50%;
    background: rgba(170, 0, 255, 0.08);
    filter: blur(110px);
    animation: floatBloom2 15s ease-in-out infinite alternate;
    pointer-events: none;
    z-index: 0;
}

@keyframes floatBloom1 {
    from {
        transform: translate(0, -30px) scale(0.9);
    }
    to {
        transform: translate(160px, 100px) scale(1.2);
    }
}

@keyframes floatBloom2 {
    from {
        transform: translate(0, 40px) scale(1);
    }
    to {
        transform: translate(-140px, -100px) scale(1.25);
    }
}

/* -----------------------------------------------------------
   MAIN CONTAINER
----------------------------------------------------------- */

.block-container {
    max-width: 1250px;
    padding-top: 3rem;
    padding-bottom: 5rem;
    position: relative;
    z-index: 2;
}

/* -----------------------------------------------------------
   TITLES
----------------------------------------------------------- */

h1 {
    font-family: 'Orbitron', sans-serif !important;
    font-size: clamp(3rem, 8vw, 7rem) !important;
    font-weight: 800 !important;
    letter-spacing: 0.08em !important;
    text-align: center;
    color: #ffffff !important;

    text-shadow:
        0 0 5px rgba(255,255,255,0.8),
        0 0 15px rgba(0,255,255,0.8),
        0 0 35px rgba(0,200,255,0.5);

    animation: titlePulse 4s ease-in-out infinite;
}

@keyframes titlePulse {
    0%, 100% {
        text-shadow:
            0 0 5px rgba(255,255,255,0.8),
            0 0 15px rgba(0,255,255,0.8),
            0 0 35px rgba(0,200,255,0.5);
    }

    50% {
        text-shadow:
            0 0 10px rgba(255,255,255,1),
            0 0 25px rgba(180,0,255,0.9),
            0 0 55px rgba(180,0,255,0.6);
    }
}

h2, h3 {
    font-family: 'Orbitron', sans-serif !important;
    color: #ffffff !important;
    letter-spacing: 0.04em;
}

.stSubheader {
    text-align: center;
}

/* -----------------------------------------------------------
   SIDEBAR
----------------------------------------------------------- */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            rgba(5, 5, 15, 0.97),
            rgba(10, 5, 20, 0.94)
        );
    border-right: 1px solid rgba(0,255,255,0.18);
    box-shadow:
        10px 0 50px rgba(0,0,0,0.4),
        inset -1px 0 20px rgba(0,255,255,0.04);
}

section[data-testid="stSidebar"] h3 {
    color: #00ffff !important;
    text-shadow: 0 0 15px rgba(0,255,255,0.7);
}

section[data-testid="stSidebar"] p {
    color: rgba(255,255,255,0.72);
    line-height: 1.7;
}

/* -----------------------------------------------------------
   IMAGE
----------------------------------------------------------- */

[data-testid="stImage"] {
    display: flex;
    justify-content: center;
    margin: 2rem auto;
}

[data-testid="stImage"] img {
    border-radius: 25px;
    border: 1px solid rgba(0,255,255,0.35);

    box-shadow:
        0 0 15px rgba(0,255,255,0.25),
        0 0 50px rgba(0,150,255,0.15);

    transition:
        transform 0.5s cubic-bezier(.2,.8,.2,1),
        box-shadow 0.5s ease,
        filter 0.5s ease;
}

[data-testid="stImage"] img:hover {
    transform: scale(1.05) rotate(-1deg);
    filter: brightness(1.12);

    box-shadow:
        0 0 20px rgba(0,255,255,0.7),
        0 0 60px rgba(120,0,255,0.45);
}

/* -----------------------------------------------------------
   TEXT
----------------------------------------------------------- */

.stApp p {
    color: rgba(255,255,255,0.82);
}

.stApp > div {
    position: relative;
}

/* -----------------------------------------------------------
   GLASS PANELS
----------------------------------------------------------- */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 25px;
}

/* -----------------------------------------------------------
   SELECTBOXES
----------------------------------------------------------- */

div[data-baseweb="select"] > div {
    background:
        linear-gradient(
            135deg,
            rgba(20,20,35,0.95),
            rgba(10,10,20,0.95)
        ) !important;

    border: 1px solid rgba(0,255,255,0.22) !important;
    border-radius: 14px !important;

    color: white !important;

    box-shadow:
        inset 0 0 15px rgba(0,255,255,0.03),
        0 0 0 rgba(0,255,255,0);

    transition:
        border 0.25s ease,
        box-shadow 0.25s ease,
        transform 0.25s ease;
}

div[data-baseweb="select"] > div:hover {
    border-color: rgba(0,255,255,0.7) !important;
    box-shadow:
        0 0 20px rgba(0,255,255,0.15);
    transform: translateY(-2px);
}

div[data-baseweb="popover"] {
    background: #090912 !important;
}

div[role="option"] {
    background: #090912 !important;
    color: white !important;
}

div[role="option"]:hover {
    background: rgba(0,255,255,0.12) !important;
}

/* -----------------------------------------------------------
   CHECKBOX
----------------------------------------------------------- */

div[data-testid="stCheckbox"] label {
    color: white !important;
    transition: color 0.2s ease;
}

div[data-testid="stCheckbox"] label:hover {
    color: #00ffff !important;
}

/* -----------------------------------------------------------
   BUTTONS
----------------------------------------------------------- */

.stButton > button {
    width: 100%;
    min-height: 55px;

    border-radius: 16px;

    background:
        linear-gradient(
            135deg,
            rgba(0,255,255,0.12),
            rgba(130,0,255,0.16)
        );

    border: 1px solid rgba(0,255,255,0.55);

    color: white;

    font-family: 'Orbitron', sans-serif;
    font-size: 0.9rem;
    font-weight: 600;
    letter-spacing: 0.08em;

    box-shadow:
        0 0 10px rgba(0,255,255,0.12),
        inset 0 0 20px rgba(0,255,255,0.025);

    transition:
        transform 0.18s cubic-bezier(.2,.8,.2,1),
        box-shadow 0.25s ease,
        background 0.25s ease,
        border-color 0.25s ease;
}

.stButton > button:hover {
    transform:
        translateY(-4px)
        scale(1.015);

    border-color: #00ffff;

    background:
        linear-gradient(
            135deg,
            rgba(0,255,255,0.23),
            rgba(150,0,255,0.25)
        );

    box-shadow:
        0 0 15px rgba(0,255,255,0.45),
        0 0 45px rgba(120,0,255,0.25);
}

.stButton > button:active {
    transform: scale(0.96);
    box-shadow:
        0 0 10px rgba(0,255,255,0.8),
        inset 0 0 20px rgba(0,255,255,0.2);
}

/* -----------------------------------------------------------
   AUDIO
----------------------------------------------------------- */

audio {
    width: 100%;
    border-radius: 15px;

    filter:
        drop-shadow(0 0 10px rgba(0,255,255,0.2));
}

/* -----------------------------------------------------------
   STREAMLIT BOKEH BUTTON
----------------------------------------------------------- */

.bk-btn {
    background:
        linear-gradient(
            135deg,
            rgba(0,255,255,0.12),
            rgba(150,0,255,0.15)
        ) !important;

    border: 1px solid rgba(0,255,255,0.65) !important;
    border-radius: 18px !important;

    color: white !important;

    font-family: 'Orbitron', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;

    box-shadow:
        0 0 15px rgba(0,255,255,0.15) !important;

    transition:
        transform 0.2s ease,
        box-shadow 0.25s ease !important;
}

.bk-btn:hover {
    transform: translateY(-4px) scale(1.02) !important;

    box-shadow:
        0 0 20px rgba(0,255,255,0.55),
        0 0 50px rgba(150,0,255,0.25) !important;
}

/* -----------------------------------------------------------
   FLOATING PARTICLES
----------------------------------------------------------- */

.particle {
    position: fixed;
    width: 3px;
    height: 3px;

    background: #00ffff;
    border-radius: 50%;

    pointer-events: none;
    z-index: 1;

    box-shadow:
        0 0 8px #00ffff,
        0 0 18px rgba(0,255,255,0.5);

    animation: particleFloat linear infinite;
}

@keyframes particleFloat {

    0% {
        transform:
            translateY(110vh)
            translateX(0)
            scale(0);
        opacity: 0;
    }

    10% {
        opacity: 0.8;
        transform: scale(1);
    }

    50% {
        transform:
            translateY(50vh)
            translateX(40px)
            scale(1);
    }

    90% {
        opacity: 0.5;
    }

    100% {
        transform:
            translateY(-10vh)
            translateX(-50px)
            scale(0);
        opacity: 0;
    }
}

/* -----------------------------------------------------------
   MOUSE GLOW
----------------------------------------------------------- */

.mouse-glow {
    position: fixed;

    width: 180px;
    height: 180px;

    border-radius: 50%;

    pointer-events: none;

    transform: translate(-50%, -50%);

    background:
        radial-gradient(
            circle,
            rgba(0,255,255,0.12) 0%,
            rgba(100,0,255,0.07) 30%,
            transparent 70%
        );

    filter: blur(5px);

    z-index: 999999;

    mix-blend-mode: screen;
}

/* -----------------------------------------------------------
   RESPONSIVE
----------------------------------------------------------- */

@media (max-width: 768px) {

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
        padding-top: 2rem;
    }

    h1 {
        font-size: 3rem !important;
    }

    [data-testid="stImage"] img {
        max-width: 85%;
    }

    .stButton > button {
        min-height: 60px;
    }
}

</style>


<!-- PARTICLES -->

<div class="particle" style="left:4%; animation-duration:12s; animation-delay:-4s;"></div>
<div class="particle" style="left:11%; animation-duration:18s; animation-delay:-9s;"></div>
<div class="particle" style="left:19%; animation-duration:14s; animation-delay:-2s;"></div>
<div class="particle" style="left:27%; animation-duration:20s; animation-delay:-14s;"></div>
<div class="particle" style="left:36%; animation-duration:16s; animation-delay:-7s;"></div>
<div class="particle" style="left:45%; animation-duration:22s; animation-delay:-18s;"></div>
<div class="particle" style="left:53%; animation-duration:13s; animation-delay:-3s;"></div>
<div class="particle" style="left:61%; animation-duration:19s; animation-delay:-11s;"></div>
<div class="particle" style="left:70%; animation-duration:15s; animation-delay:-6s;"></div>
<div class="particle" style="left:78%; animation-duration:21s; animation-delay:-16s;"></div>
<div class="particle" style="left:87%; animation-duration:17s; animation-delay:-8s;"></div>
<div class="particle" style="left:94%; animation-duration:23s; animation-delay:-20s;"></div>

<div class="mouse-glow" id="mouseGlow"></div>

<script>

const glow = document.getElementById("mouseGlow");

document.addEventListener("mousemove", function(e) {

    if (glow) {
        glow.style.left = e.clientX + "px";
        glow.style.top = e.clientY + "px";
    }

});

</script>

""", unsafe_allow_html=True)


# ============================================================
# ORIGINAL APPLICATION
# ============================================================

st.title("TRADUCTOR.")
st.subheader("Escucho lo que quieres traducir.")


image = Image.open('OIG7.jpg')

st.image(image, width=300)


with st.sidebar:
    st.subheader("Traductor.")
    st.write(
        "Presiona el botón, cuando escuches la señal "
        "habla lo que quieres traducir, luego selecciona"
        " la configuración de lenguaje que necesites."
    )


st.write("Toca el Botón y habla lo que quieres traducir")


stt_button = Button(
    label=" Escuchar  🎤",
    width=300,
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

            for (
                var i = e.resultIndex;
                i < e.results.length;
                ++i
            ) {

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
            console.log("Reconocimiento detenido");
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
        st.write(result.get("GET_TEXT"))


    try:
        os.mkdir("temp")
    except:
        pass


    st.title("Texto a Audio")

    translator = Translator()

    text = str(result.get("GET_TEXT"))


    # ========================================================
    # INPUT LANGUAGE
    # ========================================================

    in_lang = st.selectbox(
        "Selecciona el lenguaje de Entrada",
        (
            "Inglés",
            "Español",
            "Bengali",
            "Coreano",
            "Mandarín",
            "Japonés",
            "Ruso",
            "Alemán"
        ),
    )


    if in_lang == "Inglés":
        input_language = "en"

    elif in_lang == "Español":
        input_language = "es"

    elif in_lang == "Bengali":
        input_language = "bn"

    elif in_lang == "Coreano":
        input_language = "ko"

    elif in_lang == "Mandarín":
        input_language = "zh-cn"

    elif in_lang == "Japonés":
        input_language = "ja"

    elif in_lang == "Ruso":
        input_language = "ru"

    elif in_lang == "Alemán":
        input_language = "de"


    # ========================================================
    # OUTPUT LANGUAGE
    # ========================================================

    out_lang = st.selectbox(
        "Selecciona el lenguaje de salida",
        (
            "Inglés",
            "Español",
            "Bengali",
            "Coreano",
            "Mandarín",
            "Japonés",
            "Ruso",
            "Alemán"
        ),
    )


    if out_lang == "Inglés":
        output_language = "en"

    elif out_lang == "Español":
        output_language = "es"

    elif out_lang == "Bengali":
        output_language = "bn"

    elif out_lang == "Coreano":
        output_language = "ko"

    elif out_lang == "Mandarín":
        output_language = "zh-cn"

    elif out_lang == "Japonés":
        output_language = "ja"

    elif out_lang == "Ruso":
        output_language = "ru"

    elif out_lang == "Alemán":
        output_language = "de"


    # ========================================================
    # ACCENT
    # ========================================================

    english_accent = st.selectbox(
        "Selecciona el acento",
        (
            "Defecto",
            "Español",
            "Reino Unido",
            "Estados Unidos",
            "Canada",
            "Australia",
            "Irlanda",
            "Sudáfrica",
        ),
    )


    if english_accent == "Defecto":
        tld = "com"

    elif english_accent == "Español":
        tld = "com.mx"

    elif english_accent == "Reino Unido":
        tld = "co.uk"

    elif english_accent == "Estados Unidos":
        tld = "com"

    elif english_accent == "Canada":
        tld = "ca"

    elif english_accent == "Australia":
        tld = "com.au"

    elif english_accent == "Irlanda":
        tld = "ie"

    elif english_accent == "Sudáfrica":
        tld = "co.za"


    # ========================================================
    # TEXT TO SPEECH
    # ========================================================

    def text_to_speech(
        input_language,
        output_language,
        text,
        tld
    ):

        translation = translator.translate(
            text,
            src=input_language,
            dest=output_language
        )

        trans_text = translation.text

        tts = gTTS(
            trans_text,
            lang=output_language,
            tld=tld,
            slow=False
        )

        try:
            my_file_name = text[0:20]

        except:
            my_file_name = "audio"

        tts.save(
            f"temp/{my_file_name}.mp3"
        )

        return my_file_name, trans_text


    display_output_text = st.checkbox(
        "Mostrar el texto"
    )


    # ========================================================
    # CONVERT BUTTON
    # ========================================================

    if st.button("convertir"):

        result, output_text = text_to_speech(
            input_language,
            output_language,
            text,
            tld
        )

        audio_file = open(
            f"temp/{result}.mp3",
            "rb"
        )

        audio_bytes = audio_file.read()

        st.markdown(
            "## Tú audio:"
        )

        st.audio(
            audio_bytes,
            format="audio/mp3",
            start_time=0
        )


        if display_output_text:

            st.markdown(
                "## Texto de salida:"
            )

            st.write(
                f" {output_text}"
            )


    # ========================================================
    # FILE CLEANUP
    # ========================================================

    def remove_files(n):

        mp3_files = glob.glob(
            "temp/*mp3"
        )

        if len(mp3_files) != 0:

            now = time.time()

            n_days = n * 86400

            for f in mp3_files:

                if os.stat(f).st_mtime < now - n_days:

                    os.remove(f)

                    print(
                        "Deleted ",
                        f
                    )


    remove_files(7)