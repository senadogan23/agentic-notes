import streamlit as st

st.set_page_config(page_title="Agentic-Notes", page_icon="🚀", layout="wide")

st.title(" Agentic-Notes: AI Agent Tabanlı Ders Asistanı")
st.subheader("Sınav Dönemi Can Kurtaran Projesi")

st.write("---")
st.info("Bu proje şu an geliştirme aşamasındadır. Yakında LLM ve Agent entegrasyonları eklenecektir.")

# Basit bir dosya yükleme alanı (Arayüz iskeleti için)
uploaded_file = st.file_uploader("Ders notunu veya özetini yükle (.txt)", type=["txt"])

if uploaded_file is not None:
    st.success(f"Dosya başarıyla algılandı: {uploaded_file.name}")