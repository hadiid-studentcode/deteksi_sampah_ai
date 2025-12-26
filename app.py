import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import io
from dotenv import dotenv_values 


# --- KONFIGURASI CLIENT BARU ---
# Ganti dengan API KEY kamu

env_config = dotenv_values('.env')
API_KEY = env_config.get('GENAI_API_KEY')

if not API_KEY:
    raise ValueError("API Key tidak ditemukan! Pastikan file .env ada dan berisi GENAI_API_KEY.")



def deteksi_sampah(image_bytes, mime_type):
    # Inisialisasi Client sesuai SDK baru
    client = genai.Client(api_key=API_KEY)
    
    prompt_text = """
    Kamu adalah ahli lingkungan. Analisa gambar ini.
    1. Tentukan apakah ini sampah ORGANIK atau ANORGANIK.
    2. Berikan alasan singkat (1 kalimat).
    3. Berikan saran pengolahan singkat.
    
    Format jawaban:
    **Kategori:** [Organik/Anorganik]
    **Alasan:** [Alasan]
    **Saran:** [Saran]
    """

    # Memanggil model dengan format baru (types.Part)
    response = client.models.generate_content(
        model='gemini-2.5-flash', # Gunakan 1.5 Flash untuk performa stabil
        contents=[
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=mime_type
            ),
            prompt_text
        ]
    )
    return response.text

# --- TAMPILAN WEBSITE (STREAMLIT) ---
st.set_page_config(page_title="Deteksi Sampah AI", page_icon="♻️")

st.title("♻️ Deteksi Sampah Pintar (New SDK)")
st.write("Upload gambar sampah, AI akan menentukan jenisnya.")

uploaded_file = st.file_uploader("Pilih gambar sampah...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 1. Tampilkan Gambar di Layar
    image = Image.open(uploaded_file)
    st.image(image, caption='Preview Gambar', use_column_width=True)
    
    # 2. Siapkan Data untuk dikirim ke Gemini
    # Streamlit file uploader perlu diubah jadi bytes agar bisa dibaca SDK baru
    image_bytes = uploaded_file.getvalue()
    image_mime_type = uploaded_file.type
    
    # Tombol Deteksi
    if st.button('🔍 Deteksi Jenis Sampah'):
        if API_KEY == "MASUKKAN_API_KEY_KAMU":
             st.error("⚠️ API Key belum dimasukkan di codingan!")
        else:
            with st.spinner('Sedang menganalisa dengan SDK Baru...'):
                try:
                    hasil = deteksi_sampah(image_bytes, image_mime_type)
                    st.success("Analisa Selesai!")
                    st.markdown(hasil)
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")

# Footer
st.markdown("---")
st.caption("Powered by Google GenAI SDK v1.0")