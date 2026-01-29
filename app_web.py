import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="PABGC Mobile", 
    layout="wide"
)

# 2. CSS AGRESIF (Menghilangkan Footer & Header)
st.markdown("""
    <style>
    [data-testid="stHeader"], footer, .stAppDeployButton, #MainMenu {
        display: none !important;
        visibility: hidden !important;
    }
    .block-container {padding-top: 1rem !important;}
    
    /* Membuat input dan tombol lebih besar untuk jempol di Android */
    .stNumberInput, .stSelectbox {
        margin-bottom: 10px;
    }
    .stButton>button {
        width: 100%;
        height: 4rem;
        background-color: #28a745; /* Warna hijau agar kontras */
        color: white;
        border-radius: 10px;
        font-weight: bold;
        font-size: 18px;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
col_logo, col_judul = st.columns([1, 4])
with col_logo:
    try:
        st.image("logo.png", width=100)
    except:
        st.write("### PABGC")

with col_judul:
    st.subheader("Suplai F - Groundtank C")

st.divider()

# --- INPUT DATA LANGSUNG DI HALAMAN UTAMA (Tidak di Sidebar) ---
st.info("📝 **MASUKKAN DATA LAPANGAN DI BAWAH INI**")

# Menggunakan kolom agar tampilan di HP tetap rapi
c1, c2 = st.columns(2)
with c1:
    h1 = st.number_input("Tinggi Awal (cm)", value=0.0, step=0.1)
    suplai = st.number_input("Debit Suplai (l/dtk)", value=0.0, step=0.1)
with c2:
    h2 = st.number_input("Tinggi Akhir (cm)", value=0.0, step=0.1)
    t_val = st.number_input("Durasi", value=0.0, step=1.0)

unit = st.selectbox("Satuan Durasi", ["Menit", "Jam", "Detik"])

# Tombol Hitung Besar di Tengah
btn_hitung = st.button("🚀 HITUNG & SIMPAN DATA")

# --- LOGIKA HITUNG ---
if btn_hitung:
    t_detik = t_val * 60 if unit == "Menit" else (t_val * 3600 if unit == "Jam" else t_val)
    luas = 36.0
    nr = h2 - h1
    nt = ((suplai * t_detik) / 1000 / luas) * 100
    dev = nt - nr
    vw = (max(0.0, dev) / 100) * luas
    dw = (vw * 1000) / t_detik if t_detik > 0 else 0
    
    new_data = {
        "Waktu": datetime.now().strftime("%H:%M"),
        "Naik (cm)": round(nr, 1),
        "Target (cm)": round(nt, 1),
        "Selisih (cm)": round(dev, 1),
        "Warga (m3)": round(vw, 2),
        "L/s": round(dw, 2)
    }
    
    if 'audit_data' not in st.session_state:
        st.session_state.audit_data = []
    st.session_state.audit_data.insert(0, new_data)
    st.success("Data berhasil ditambahkan ke tabel!")

st.divider()

# --- TABEL HASIL (Tepat di bawah input) ---
st.write("📊 **HASIL PERHITUNGAN TERBARU**")

if 'audit_data' in st.session_state and st.session_state.audit_data:
    df_hasil = pd.DataFrame(st.session_state.audit_data)
    st.table(df_hasil)
    
    # Tombol Download
    csv = df_hasil.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download File CSV", data=csv, file_name="laporan_suplai_f.csv", mime='text/csv')
else:
    st.warning("Belum ada riwayat perhitungan.")
