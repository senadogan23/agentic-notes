import streamlit as st  # Web arayüzünü oluşturmak için Streamlit kütüphanesini dahil ediyoruz.

# Tarayıcı sekmesinde görünecek olan sayfa başlığı, ikon ve sayfa düzenini (geniş ekran) ayarlıyoruz.
st.set_page_config(
    page_title="Agentic-Notes", 
    page_icon="🚀", 
    layout="wide"
)

# Ana sayfa başlığı ve alt başlığı ekranda gösteriyoruz.
st.title("Agentic-Notes: AI Agent Tabanlı Ders Asistanı")
st.subheader("Sınav Dönemi Can Kurtaran Projesi")

# Arayüze görsel bir ayrım çizgisi çekiyoruz.
st.write("---")

# Kullanıcıyı projenin mevcut durumu hakkında bilgilendiren mavi bir bilgi kutusu ekliyoruz.
st.info("Bu proje şu an geliştirme aşamasındadır. Yakında LLM (Büyük Dil Modeli) ve Agent entegrasyonları eklenecektir.")

# Kullanıcının ders notlarını yükleyebileceği bir dosya yükleme alanı oluşturuyoruz.
# Şimdilik sadece düz metin (.txt) formatındaki dosyaları kabul ediyoruz.
uploaded_file = st.file_uploader("Ders notunu veya özetini yükle (.txt)", type=["txt"])

# Eğer kullanıcı bir dosya yüklediyse bu blok çalışır:
if uploaded_file is not None:
    # Yüklenen dosyanın adını ekranda yeşil bir başarı kutusu (success box) içinde gösteriyoruz.
    st.success(f"Dosya başarıyla algılandı: {uploaded_file.name}")