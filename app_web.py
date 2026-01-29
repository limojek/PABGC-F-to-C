import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image
from fpdf import FPDF
import time

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="PABGC Audit Mobile", layout="wide")

# 2. SEMBUNYIKAN MENU GITHUB, SHARE, & FOOTER
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stAppDeployButton {display:none;}
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# 3. FUNGSI WAKTU INDONESIA
def get_waktu_indo():
    hari = {
        'Monday': 'Senin', 'Tuesday': 'Selasa', 'Wednesday': 'Rabu',
        'Thursday': 'Kamis', 'Friday': 'Jumat', 'Saturday': 'Sabtu', 'Sunday': 'Minggu'
    }
    bulan = {
        'January': 'Januari', 'February': 'Februari', 'March': 'Maret', 'April': 'April',
        'May': 'Mei', 'June': 'Juni', 'July': 'Juli', 'August': 'Agustus',
        'September': 'September', 'October': 'Oktober', 'November': 'November', 'December': 'Desember'
    }
    skrg = datetime.now()
    nama_hari = hari[skrg.strftime('%A')]
    nama_bulan = bulan[skrg.strftime('%B')]
    return f"{nama_hari}, {skrg.strftime('%d')} {nama_bulan} {skrg.strftime('%Y | %H:%M:%S')}"

# --- HEADER LOGO & JUDUL ---
col1, col2 = st.columns([1, 3])

with col1:
    try:
        img = Image.open("logo.png")
        st.image(img, width=200)
    except:
        st.info("Logo belum diunggah")

with col2:
    st.title("PABGC")
    st.subheader("AUDIT DISTRIBUSI - Groundtank C")
    st.write(f"### {get_waktu_indo()}")

st.divider()

# --- INPUT DATA ---
st.sidebar.header("Input Data Lapangan")
h1 = st.sidebar.number_input("Tinggi Awal (cm)", value=0.0, step=0.1)
h2 = st.sidebar.number_input("Tinggi Akhir (cm)", value=0.0, step=0.1)
suplai = st.sidebar.number_input("Debit Suplai (l/dtk)", value=0.0, step=0.1)
t_val = st.sidebar.number_input("Durasi", value=0.0, step=1.0)
unit = st.sidebar.selectbox("Satuan Durasi", ["Menit", "Jam", "Detik"])

if st.sidebar.button("HITUNG & SIMPAN"):
    if unit == "Menit":
        t_detik = t_val * 60
    elif unit == "Jam":
        t_detik = t_val * 3600
    else:
        t_detik = t_val
        
    luas = 36.0
    nr = h2 - h1
    nt = ((suplai * t_detik) / 1000 / luas) * 100
    dev = nt - nr
    vw = (max(0.0, dev) / 100) * luas
    dw = (vw * 1000) / t_detik if t_detik > 0 else 0
    
    new_data = {
        "Waktu": datetime.now().strftime("%H:%M:%S"),
        "Naik (cm)": round(nr, 1),
        "Target (cm)": round(nt, 1),
        "Selisih (cm)": round(dev, 1),
        "Warga (m3)": round(vw, 2),
        "L/s": round(dw, 2)
    }
    
    if 'audit_data' not in st.session_state:
        st.session_state.audit_data = []
    
    st.session_state.audit_data.insert(0, new_data)
    st.success("Data Tersimpan!")

# --- TAMPILAN TABEL ---
if 'audit_data' in st.session_state and st.session_state.audit_data:
    df = pd.DataFrame(st.session_state.audit_data)
    st.table(df)
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Laporan (CSV)",
        data=csv,
        file_name=f"audit_pabgc_{datetime.now().strftime('%Y%m%d')}.csv",
        mime='text/csv',
    )
else:
    st.info("Belum ada data.")
