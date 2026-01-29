import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="PABGC Mobile", 
    layout="wide", 
    initial_sidebar_state="auto"
)

# 2. CSS AGRESIF (Menghilangkan Footer & Header secara Total)
st.markdown("""
    <style>
    [data-testid="stHeader"], footer, .stAppDeployButton, #MainMenu {
        display: none !important;
        visibility: hidden !important;
    }
    .block-container {padding-top: 1rem !important;}
    
    /* Memperbesar tombol agar mudah ditekan di HP */
    .stButton>button {
        width: 100%;
        height: 3.5rem;
        background-color: #007bff;
        color: white;
        border-radius: 8px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER (Tanpa Jam) ---
col1, col2 = st.columns([1, 4])
with col1:
    try:
        st.image("logo.png", width=120)
    except:
        st.subheader("PABGC")

with col2:
    st.subheader("Suplai F - Groundtank C")
    st.write("Aplikasi Audit Distribusi")

st.divider()

# --- INPUT DATA (SIDEBAR) ---
with st.sidebar:
    st.header("Input Lapangan")
    h1 = st.number_input("Tinggi Awal (cm)", value=0.0, step=0.1)
    h2 = st.number_input("Tinggi Akhir (cm)", value=0.0, step=0.1)
    suplai = st.number_input("Debit Suplai (l/dtk)", value=0.0, step=0.1)
    t_val = st.number_input("Durasi", value=0.0, step=1.0)
    unit = st.selectbox("Satuan", ["Menit", "Jam", "Detik"])
    
    btn_hitung = st.button("💾 HITUNG & SIMPAN")

# --- LOGIKA HITUNG ---
if btn_hitung:
    # Konversi waktu
    t_detik = t_val * 60 if unit == "Menit" else (t_val * 3600 if unit == "Jam" else t_val)
    
    # Rumus
    luas = 36.0
    nr = h2 - h1
    nt = ((suplai * t_detik) / 1000 / luas) * 100
    dev = nt - nr
    vw = (max(0.0, dev) / 100) * luas
    dw = (vw * 1000) / t_detik if t_detik > 0 else 0
    
    # Data Baru
    new_data = {
        "Waktu": datetime.now().strftime("%H:%M"),
        "Naik": f"{round(nr, 1)} cm",
        "Target": f"{round(nt, 1)} cm",
        "Selisih": f"{round(dev, 1)} cm",
        "Warga": f"{round(vw, 2)} m3",
        "L/s": round(dw, 2)
    }
    
    if 'audit_data' not in st.session_state:
        st.session_state.audit_data = []
    
    st.session_state.audit_data.insert(0, new_data)
    st.toast("Data Berhasil Disimpan!")

# --- TABEL HASIL ---
if 'audit_data' in st.session_state and st.session_state.audit_data:
    st.table(pd.DataFrame(st.session_state.audit_data))
    
    # Tombol Download
    csv = pd.DataFrame(st.session_state.audit_data).to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Laporan (CSV)", data=csv, file_name="laporan_audit.csv", mime='text/csv')
else:
    st.info("Silakan masukkan data pada menu Sidebar (sebelah kiri).")
