import streamlit as st
import numpy as np
from utils import diagnosis
from PIL import Image
from torchvision import transforms

st.set_page_config(page_title="Pocketmed", page_icon= "💊")
st.sidebar.header("Cek Kulit")
st.write("# POCKETMED")

st.text("⚕️Selamat datang di Pocketmed!⚕️")
if "close_warning" not in st.session_state:
    st.warning("Selain cek kesehatan kulit, di Pocketmed ini, kamu juga bisa berbincang dengan dokter virtual kami. Silahkan klik tombol di kiri atas layar kalian dan pilih 'Dokter Virtual'", icon="🤖")

img_file = st.file_uploader("Masukkan gambar", type=["jpg", "png", "jpeg", "webp"], accept_multiple_files=False)
st.set_option("deprecation.showfileUploaderEncoding", False)


if img_file is not None:
    st.session_state.close_warning = True
    gbr = Image.open(img_file).resize((224,224)).convert("RGB")
    tensorImage = np.asarray(gbr, dtype=np.uint8)
    st.image(gbr, use_column_width=True,channels= "RGB")
    st.write("klik tombol dibawah untuk memulai prediksi")
    if st.button("Cek kondisi kulit"):
        data = list(diagnosis(tensorImage))
        st.markdown("""<style>
        p {
            text-align: justify;
        }
    </style>""", unsafe_allow_html=True)
        st.markdown('<h4>Hasil diagnosis anda adalah sebagai berikut:</h4>',unsafe_allow_html=True)
        text = f''' <p style="text-indent: 30px;">Dari gambar yang kamu berikan, kami mengklasifikasikannya sebagai {data[0]}.</p>
            {data[2]}
            Berikut adalah tautan yang mungkin bisa kamu baca : <a href="{data[1]}">{data[1]}</a>.</p>
            
            
           ⚠️ Peringatan : Hasil prediksi bisa saja salah, silahkan hubungi dan kunjungi dokter untuk penjelasan lebih lanjut.
        '''
        st.markdown(text, unsafe_allow_html=True)
    else:
        pass
else:
    pass
