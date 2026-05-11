import streamlit as st
import google.generativeai as genai
import time
import pandas as pd

# ==========================================
# 1. KONFIGURASI HALAMAN 
# ==========================================
st.set_page_config(
    page_title="Mind Guide | Editorial Edition",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. INJEKSI CUSTOM CSS
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600&family=Playfair+Display:ital,wght@0,600;1,600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif !important;
        background-color: #FCFAFF !important;
        color: #2D2A32 !important;
    }

    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #4A3B52 !important;
    }

    .premium-card {
        background: #FFFFFF;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 40px -10px rgba(138, 90, 185, 0.08);
        border: 1px solid #F3EDF7;
        margin-bottom: 25px;
    }

    .disclaimer-box {
        background-color: #FFF5F5;
        border-left: 5px solid #FC8181;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 25px;
        font-size: 14px;
        color: #C53030;
    }

    .stButton > button {
        background: linear-gradient(135deg, #A88BEB 0%, #F8CEEC 100%) !important;
        color: #4A3B52 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 28px !important;
        font-weight: 500 !important;
        box-shadow: 0 4px 15px rgba(168, 139, 235, 0.2) !important;
    }

    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #E2D4F0 0%, #A88BEB 100%);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. KONFIGURASI API & MODEL
# ==========================================
API_KEY = "ISI-API-KEY-ANDA"
genai.configure(api_key=API_KEY)

system_instruction = (
    "Anda adalah Mind Guide, asisten edukasi psikologi bergaya editorial. "
    "Gunakan DSM-5 sebagai referensi utama. Gaya bahasa: sangat profesional, empatik, terstruktur. "
    "SELALU tekankan bahwa Anda bukan pengganti profesional medis."
)

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config={"temperature": 0.2, "top_p": 0.9, "max_output_tokens": 2048},
    system_instruction=system_instruction
)

# ==========================================
# 4. SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #8E44AD;'>Mind Guide<br><span style='font-size: 16px; font-family: Outfit; font-weight: 300; color: #A0A0A0;'>Curated Psychology</span></h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.radio("Menu Navigasi", ["✨ Interactive Session", "📚 DSM-5 Glossary", "📊 Analytics"], label_visibility="collapsed")
    st.markdown("---")
    
    with st.expander("⚙️ System Status", expanded=True):
        st.caption("🟢 API Connected")
        st.caption("🛡️ DSM-5 Guardrails: Active")

# ==========================================
# 5. DASHBOARD UTAMA
# ==========================================
col_main, col_metrics = st.columns([6.5, 3.5], gap="large")

with col_metrics:
    st.markdown("### 📊 Session Overview")
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 14px; color: #7F7F7F;'>Literacy Depth</p>", unsafe_allow_html=True)
    st.progress(78)
    st.markdown("<br>", unsafe_allow_html=True)
    
    chart_data = pd.DataFrame({"Persentase": [40, 25, 20, 15]}, index=["Anxiety", "Mood", "Stress", "Personality"])
    st.bar_chart(chart_data, color="#B9A2ED", height=180)
    st.markdown("</div>", unsafe_allow_html=True)

with col_main:
    st.markdown("<h2>Clinical Education Space</h2>", unsafe_allow_html=True)
    
    # DISCLAIMER PROMINEN
    st.markdown("""
        <div class="disclaimer-box">
            <strong>⚠️ PENTING:</strong> Mind Guide adalah alat bantu edukasi berbasis AI. 
            Informasi yang disediakan di sini <strong>tidak menggantikan</strong> saran, diagnosis, atau perawatan 
            langsung dari psikolog atau psikiater profesional. Jika Anda atau seseorang yang Anda kenal berada 
            dalam kondisi krisis atau darurat medis, segera hubungi layanan kesehatan setempat.
        </div>
    """, unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.markdown("<div class='premium-card' style='text-align: center;'><h3 style='color: #8E44AD;'>Selamat Datang di Mind Guide</h3><p style='color: #7F7F7F;'>Tanyakan apa saja seputar terminologi psikologi berdasarkan pedoman DSM-5.</p></div>", unsafe_allow_html=True)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Apa yang ingin Anda pelajari hari ini?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Menganalisis literatur DSM-5..."):
                time.sleep(0.8)
                try:
                    response = model.generate_content(prompt)
                    bot_reply = response.text
                    st.markdown(bot_reply)
                    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                except Exception as e:
                    st.error(f"Error: {e}")
