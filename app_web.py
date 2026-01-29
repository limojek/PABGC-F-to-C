import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image
from fpdf import FPDF # Pastikan di requirements.txt adalah fpdf2
import time

# Konfigurasi Halaman
st.set_page_config(page_title="PABGC Audit Mobile", layout="wide")

# --- HEADER LOGO & JUDUL ---
col1, col2 = st.columns([1, 3])

with col1:
    try:
        # Mencoba membuka logo.png
        img = Image.open("logo.png")
        st.image(img, width=200)
    except:
        st.warning("Tips: Unggah file logo.png ke GitHub agar logo muncul di sini.")

with col2:
    st.title("PABGC")
    st.subheader("AUDIT DISTRIBUSI - Groundtank C")
    
    # JAM REAL-TIME
    skrg = datetime.now()
    # Format bahasa Indonesia sederhana
    st.write(f"### {skrg.strftime('%A, %d %B %Y | %H:%M:%S')}")

st.divider()

# --- INPUT DATA ---
st.sidebar.header("Input Data Lapangan")
h1 = st.sidebar.number_input("Tinggi Awal (cm)", value=0.0, step=0.1)
h2 = st.sidebar.number_input("Tinggi Akhir (cm)", value=0.0, step=0.1)
suplai = st.sidebar.number_input("Debit Suplai (l/dtk)", value=0.0, step=0.1)
t_val = st.sidebar.number_input("Durasi", value=0.0, step=1.0)
unit = st.sidebar.selectbox("Satuan Durasi", ["Menit", "Jam", "Detik"])

if st.sidebar.button("HITUNG & SIMPAN"):
    # Logika Hitung
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
        "H1 (cm)": h1,
        "H2 (cm)": h2,
        "Naik (cm)": round(nr, 1),
        "Target (cm)": round(nt, 1),
        "Selisih (cm)": round(dev, 1),
        "Warga (m3)": round(vw, 2),
        "L/s": round(dw, 2)
    }
    
    if 'audit_data' not in st.session_state:
        st.session_state.audit_data = []
    
    # Masukkan data baru di posisi paling atas
    st.session_state.audit_data.insert(0, new_data)
    st.success("Data berhasil dihitung dan disimpan!")

# --- TAMPILAN TABEL ---
if 'audit_data' in st.session_state and st.session_state.audit_data:
    df = pd.DataFrame(st.session_state.audit_data)
    st.table(df)
    
    # Tombol Download CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Laporan (CSV)",
        data=csv,
        file_name=f"audit_pabgc_{datetime.now().strftime('%Y%m%d')}.csv",
        mime='text/csv',
    )
else:
    st.info("Belum ada data. Masukkan angka di samping kiri dan klik HITUNG.")