import streamlit as st
import google.generativeai as genai
import time
import pandas as pd

# ==========================================
# 1. KONFIGURASI HALAMAN & TEMA DASAR
# ==========================================
st.set_page_config(
    page_title="MindGuide Pro | Enterprise",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. INJEKSI CUSTOM CSS (UI/UX MODERN)
# ==========================================
st.markdown("""
    <style>
    /* Import Font Modern */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    /* Global Typography & Background */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #FAFAFC !important; /* Very light gray/lavender tint */
        color: #2D3748 !important;
    }

    /* Minimalist Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #F0EDF5 !important;
        box-shadow: 2px 0 10px rgba(138, 90, 185, 0.02);
    }
    
    /* Modern Card Containers */
    .modern-card {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(142, 68, 173, 0.04);
        border: 1px solid #F4F1F8;
        margin-bottom: 24px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .modern-card:hover {
        box-shadow: 0 6px 25px rgba(142, 68, 173, 0.08);
    }

    /* Soft Purple Gradient Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        letter-spacing: 0.3px;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(155, 89, 182, 0.2) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(155, 89, 182, 0.3) !important;
    }

    /* Subtle Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #D7BDE2 0%, #9B59B6 100%);
        border-radius: 10px;
    }

    /* Header Styling */
    h1, h2, h3 {
        color: #1A202C !important;
        font-weight: 700 !important;
    }
    .text-purple { color: #8E44AD; }
    .text-lavender { color: #A569BD; }

    /* Hide Default Streamlit Elements for Cleanliness */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. KONFIGURASI GEMINI API & DSM-5 PROMPT
# ==========================================
API_KEY = "YOUR_GEMINI_API_KEY_HERE"  # Ganti dengan API Key Anda
genai.configure(api_key=API_KEY)

# Instruksi sistem ketat berbasis DSM-5
system_instruction = (
    "Anda adalah MindGuide Pro, sebuah sistem AI asisten edukasi psikologi tingkat enterprise. "
    "Anda diwajibkan menggunakan Diagnostic and Statistical Manual of Mental Disorders, Edisi Kelima (DSM-5) "
    "sebagai referensi mutlak untuk definisi, indikator, kriteria, dan terminologi psikologi. "
    "PERINGATAN KRITIS: Anda BUKAN alat diagnostik medis. Setiap respons yang membahas kriteria klinis "
    "harus menyertakan penafian (disclaimer) bahwa informasi ini untuk tujuan edukasi akademik dan literasi semata, "
    "bukan diagnosis. "
    "Gaya Bahasa: Sangat profesional, empatik, terstruktur (gunakan bullet points/tabel), menenangkan (calming), "
    "dan mudah dipahami oleh awam tanpa menghilangkan bobot ilmiah. Hindari asumsi; selalu rujuk pada kriteria standar."
)

# Konfigurasi Model (Temperature rendah untuk akurasi ilmiah)
generation_config = {
  "temperature": 0.2, 
  "top_p": 0.9,
  "max_output_tokens": 2048,
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
    system_instruction=system_instruction
)

# ==========================================
# 4. KOMPONEN UI SIDEBAR (NAVIGASI)
# ==========================================
with st.sidebar:
    st.markdown("### ✨ <span class='text-purple'>MindGuide</span> Pro", unsafe_allow_html=True)
    st.caption("Enterprise Mental Health Literacy")
    st.markdown("---")
    
    # Navigasi dummy untuk kesan enterprise
    st.radio("Navigasi Utama", ["💬 Konsultasi Edukasi", "📚 Direktori DSM-5", "📊 Laporan Analisis", "⚙️ Pengaturan"], label_visibility="collapsed")
    st.markdown("---")
    
    # Empty State / Info Panel
    st.markdown("""
        <div style='background-color:#F4F1F8; padding:15px; border-radius:10px;'>
            <h5 style='color:#8E44AD; margin-bottom:5px; font-size:14px;'>Sesi Aktif</h5>
            <p style='font-size:12px; color:#666;'>Model: Gemini-1.5-Flash<br>Referensi: DSM-5 Standard<br>Status: Secure & Encrypted</p>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# 5. KOMPONEN UI UTAMA (DASHBOARD)
# ==========================================
col_main, col_side = st.columns([7, 3], gap="large")

with col_side:
    # Komponen Visualisasi Modern & Progress
    st.markdown("### 📊 Status Literasi")
    st.markdown("<div class='modern-card'>", unsafe_allow_html=True)
    
    st.markdown("<span style='font-size:14px; color:#555;'>Kelengkapan Modul Edukasi</span>", unsafe_allow_html=True)
    st.progress(85)
    
    st.markdown("<hr style='border:1px dashed #E2E8F0'>", unsafe_allow_html=True)
    
    # Chart Elegan (Dummy data untuk tampilan startup)
    st.markdown("<span style='font-size:14px; color:#555;'>Fokus Topik Bulan Ini</span>", unsafe_allow_html=True)
    chart_data = pd.DataFrame(
        {"Skor": [45, 30, 15, 10]}, 
        index=["Anxiety", "Mood Disorders", "Stress Management", "Lainnya"]
    )
    st.bar_chart(chart_data, color="#A569BD", height=150)
    
    st.markdown("</div>", unsafe_allow_html=True)

    # Disclaimer Profesional
    st.info("💡 **Disclaimer Medis:** Sistem ini dirancang sebagai panduan edukasi berdasarkan DSM-5, bukan pengganti konsultasi dengan psikolog klinis atau psikiater.")

with col_main:
    # Header Utama
    st.markdown("<h2 style='margin-bottom: 5px;'>Ruang Edukasi & Analisis Psikologi</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #718096; font-size: 15px; margin-bottom: 25px;'>Asisten berbasis AI ini siap membantu Anda memahami konsep kesehatan mental secara saintifik dan mudah dipahami.</p>", unsafe_allow_html=True)

    # Inisialisasi Memori Percakapan
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Empty State Professional
        st.markdown("""
            <div class='modern-card' style='text-align:center; padding:40px 20px;'>
                <h3 style='color:#A569BD;'>Selamat Datang di MindGuide Pro</h3>
                <p style='color:#718096;'>Ketik pertanyaan Anda di bawah untuk memulai analisis terminologi, kriteria, atau konsep psikologi berdasarkan pedoman DSM-5.</p>
            </div>
        """, unsafe_allow_html=True)

    # Render Riwayat Percakapan
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Form Input Nyaman Dibaca (Sticky Bottom)
    if prompt := st.chat_input("Contoh: Jelaskan kriteria utama Generalized Anxiety Disorder menurut DSM-5..."):
        
        # Tambahkan pesan user ke UI
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Proses dengan Loading State Profesional
        with st.chat_message("assistant"):
            with st.spinner("Menganalisis pedoman DSM-5 dan menyusun literatur..."):
                time.sleep(0.5) # Animasi jeda halus
                try:
                    response = model.generate_content(prompt)
                    bot_reply = response.text
                    st.markdown(bot_reply)
                    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                except Exception as e:
                    st.error(f"Detail Error: {e}")