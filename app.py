from utils.file_manager import save_uploaded_file, read_file_content
from utils.agent_brain import StudyAgent
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
    # 1. Dosyayı kaydet ve içeriğini oku
    file_path = save_uploaded_file(uploaded_file)
    file_content = read_file_content(file_path)
    
    st.success(f"Dosya başarıyla algılandı ve kaydedildi: {uploaded_file.name}")
    
    # 2. Agent nesnesini initialize et
    agent = StudyAgent(document_content=file_content)
    
    st.write("---")
    st.subheader("🤖 Agent Komut Merkezi")
    st.info("Yüklediğiniz ders notu üzerinde Agent'ın çalıştırmasını istediğiniz görevi seçin:")
    
    # Yan yana butonlar için Streamlit kolonları oluşturalım
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 Kapsamlı Özet Çıkar", use_container_width=True):
            with st.spinner("Agent notları analiz ediyor ve özetliyor..."):
                result = agent.execute_tool("ozet_cıkar")
                st.markdown(result)
                
    with col2:
        if st.button("❓ Potansiyel Soruları Üret", use_container_width=True):
            with st.spinner("Agent sınav sorularını hazırlıyor..."):
                result = agent.execute_tool("soru_uret")
                st.markdown(result)
                
    with col3:
        if st.button("🗂️ Flashcard Kartları Oluştur", use_container_width=True):
            with st.spinner("Agent çalışma kartlarını hazırlıyor..."):
                result = agent.execute_tool("flashcard")
                st.markdown(result)