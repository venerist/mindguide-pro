import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
# Pastikan API Key Anda aman
API_KEY = "ISI_DENGAN_API_KEY_BARU_ANDA" 
genai.configure(api_key=API_KEY)

# Konfigurasi Model
generation_config = {
    "temperature": 0.2,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}

# System Instruction untuk menjaga persona profesional
system_instruction = (
    "Anda adalah asisten ahli psikologi klinis dari MindGuide Pro. "
    "Tugas Anda adalah memberikan edukasi kesehatan mental berdasarkan referensi akademik DSM-5. "
    "Gunakan bahasa Indonesia yang formal, empatik, dan faktual. "
    "Jangan memberikan diagnosis medis mandiri, arahkan selalu ke profesional jika diperlukan."
)

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
    system_instruction=system_instruction
)

# --- UI CUSTOMIZATION (PETER SAVILLE INSPIRED) ---
st.set_page_config(page_title="MindGuide Pro", layout="wide")

st.markdown("""
    <style>
    /* Import Font Modern Swiss */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;300;400;600&family=Playfair+Display:ital,wght@0,400;1,700&display=swap');

    /* Global Style - Luxury Minimalism */
    .stApp {
        background-color: #FAFAFA;
        color: #2D2D2D;
        font-family: 'Inter', sans-serif;
    }

    /* Heading Style - Editorial Modern */
    h1 {
        font-family: 'Playfair Display', serif;
        font-weight: 100;
        font-size: 4rem !important;
        letter-spacing: -2px;
        color: #6D5B97;
        margin-bottom: 0px;
    }

    .subtitle {
        font-weight: 300;
        letter-spacing: 2px;
        text-transform: uppercase;
        font-size: 0.8rem;
        color: #A0A0A0;
        margin-bottom: 50px;
    }

    /* Sidebar - Ultra Clean */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #F0F0F0;
    }

    /* Chat Input - Modern Underline */
    .stChatInputContainer {
        padding-bottom: 50px;
        background-color: transparent !important;
    }

    /* Message Bubble - Geometric Balance */
    .stChatMessage {
        background-color: #FFFFFF !important;
        border: 1px solid #F0F0F0;
        border-radius: 0px !important; /* Sharp minimalist look */
        padding: 25px !important;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.02);
    }

    /* Buttons - Elegant & Thin */
    .stButton>button {
        border-radius: 0px;
        border: 1px solid #6D5B97;
        background-color: transparent;
        color: #6D5B97;
        padding: 10px 25px;
        transition: all 0.4s ease;
    }

    .stButton>button:hover {
        background-color: #6D5B97;
        color: white;
        border: 1px solid #6D5B97;
    }

    /* Hide redundant elements for clean look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown("<h1>MindGuide Pro</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Contemporary Mental Health Literacy / DSM-5 Standard</p>", unsafe_allow_html=True)

# --- CHAT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input User
if prompt := st.chat_input("Apa yang ingin Anda diskusikan hari ini?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Otorisasi diperlukan. Detail: {e}")
