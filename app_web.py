import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="PABGC Mobile", layout="wide")

# 2. CSS AGRESIF (Menghilangkan Header/Footer & Merapikan Tabel)
st.markdown("""
    <style>
    [data-testid="stHeader"], footer, .stAppDeployButton, #MainMenu {
        display: none !important;
        visibility: hidden !important;
    }
    .block-container {padding-top: 1rem !important;}
    
    /* Center angka di dalam tabel agar sejajar di bawah header */
    th, td {
        text-align: center !important;
        font-size: 13px !important;
    }
    
    /* Tombol Hitung Hijau */
    .stButton>button:first-child {
        width: 100%; height: 3.5rem; background-color: #28a745;
        color: white; border-radius: 10px; font-weight: bold; border: none;
    }
    /* Tombol Reset Merah */
    div[data-testid="stVerticalBlock"] > div:last-child .stButton>button {
        background-color: #dc3545 !important;
        height: 2.5rem !important;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
col_logo, col_judul = st.columns([1, 4])
with col_logo:
    try:
        st.image("logo.png", width=80)
    except:
        st.write("### PABGC")
with col_judul:
    st.subheader("Suplai F - Groundtank C")

st.divider()

# --- INPUT DATA (H GANTI L) ---
st.info("📝 **INPUT DATA LAPANGAN**")
c1, c2 = st.columns(2)
with c1:
    l1 = st.number_input("L1 (cm)", value=0.0, step=0.1)
    suplai = st.number_input("Suplai (l/dtk)", value=0.0, step=0.1)
with c2:
    l2 = st.number_input("L2 (cm)", value=0.0, step=0.1)
    t_val = st.number_input("Durasi", value=0.0, step=1.0)

# Singkatan satuan sesuai permintaan
unit_opt = {"Menit": "mnt", "Detik": "dtk", "Jam": "jam"}
unit_choice = st.selectbox("Satuan Durasi", list(unit_opt.keys()))
unit_abbr = unit_opt[unit_choice]

if st.button("🚀 HITUNG & SIMPAN"):
    # Konversi durasi ke detik untuk rumus
    if unit_choice == "Menit": t_detik = t_val * 60
    elif unit_choice == "Jam": t_detik = t_val * 3600
    else: t_detik = t_val
        
    luas = 36.0
    nr = l2 - l1
    nt = ((suplai * t_detik) / 1000 / luas) * 100
    dev = nt - nr
    vw = (max(0.0, dev) / 100) * luas
    dw = (vw * 1000) / t_detik if t_detik > 0 else 0
    
    # Format data 1 angka di belakang koma
    new_data = {
        "Durasi": f"{int(t_val)} {unit_abbr}",
        "Naik(cm)": round(float(nr), 1),
        "Tgt(cm)": round(float(nt), 1),
        "Slsh(cm)": round(float(dev), 1),
        "Warga(m3)": round(float(vw), 1),
        "L/dtk": round(float(dw), 1)
    }
    
    if 'audit_data' not in st.session_state:
        st.session_state.audit_data = []
    st.session_state.audit_data.insert(0, new_data)
    st.toast("Data disimpan!")

st.divider()

# --- TABEL HASIL ---
st.write("📊 **HASIL PERHITUNGAN**")

if 'audit_data' in st.session_state and st.session_state.audit_data:
    df_hasil = pd.DataFrame(st.session_state.audit_data)
    # Tampilan tabel dengan angka sejajar di tengah
    st.table(df_hasil)
    
    c_down, c_reset = st.columns(2)
    with c_down:
        csv = df_hasil.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Simpan CSV", data=csv, file_name="audit_f.csv")
    
    with c_reset:
        if st.button("🗑️ RESET TABEL"):
            st.session_state.audit_data = []
            st.rerun()
else:
    st.info("Belum ada riwayat data.")
