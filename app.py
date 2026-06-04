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

if "messages" not in st.session_state:
    st.session_state.messages = []

# Kullanıcıyı projenin mevcut durumu hakkında bilgilendiren mavi bir bilgi kutusu ekliyoruz.
st.info("Bu proje şu an geliştirme aşamasındadır. Yakında LLM (Büyük Dil Modeli) ve Agent entegrasyonları eklenecektir.")

# Kullanıcının ders notlarını yükleyebileceği bir dosya yükleme alanı oluşturuyoruz.
# Şimdilik sadece düz metin (.txt) formatındaki dosyaları kabul ediyoruz.
uploaded_file = st.file_uploader("Ders notunu veya özetini yükle (.txt)", type=["txt"])

# Eğer kullanıcı bir dosya yüklediyse bu blok çalışır:
if uploaded_file is not None:
    file_path = save_uploaded_file(uploaded_file)
    file_content = read_file_content(file_path)
    st.success(f"Dosya başarıyla algılandı ve kaydedildi: {uploaded_file.name}")
    agent = StudyAgent(document_content=file_content)
    
    st.write("---")
    st.subheader(" Agent Komut Merkezi")
    st.info("Yüklediğiniz ders notu üzerinde Agent'ın çalıştırmasını istediğiniz görevi seçin:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 Kapsamlı Özet Çıkar", use_container_width=True):
            with st.spinner("Agent notları analiz ediyor ve özetliyor..."):
                result = agent.execute_tool("ozet_cıkar")
                st.session_state.messages.append({"role": "assistant", "content": result})
                st.rerun()  # 1. BURAYA EKLENDİ (Özet biter bitmez ekranı yeniler)
                
    with col2:
        if st.button("❓ Potansiyel Soruları Üret", use_container_width=True):
            with st.spinner("Agent sınav sorularını hazırlıyor..."):
                result = agent.execute_tool("soru_uret")
                st.session_state.messages.append({"role": "assistant", "content": result})
                st.rerun()  # 2. BURAYA EKLENDİ (Sorular biter bitmez ekranı yeniler)
                
    with col3:
        if st.button("🗂️ Flashcard Kartları Oluştur", use_container_width=True):
            with st.spinner("Agent çalışma kartlarını hazırlıyor..."):
                result = agent.execute_tool("flashcard")
                st.session_state.messages.append({"role": "assistant", "content": result})
                st.rerun()  # 3. BURAYA EKLENDİ (Kartlar biter bitmez ekranı yeniler)

    st.write("---")
    st.subheader("💬 Asistan ile Canlı Sohbet")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_input := st.chat_input("Ders notu hakkında bir soru sorun..."):
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.chat_message("assistant"):
            with st.spinner("Düşünüyor..."):
                prompt = f"Kullanıcı ders notuna dayanarak şu soruyu sordu: {user_input}\n\nNot İçeriği:\n{file_content}"
                
                try:
                    response = agent.client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": agent.system_prompt},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.5
                    )
                    answer = response.choices[0].message.content
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    st.rerun()  # 4. BURAYA EKLENDİ (Cevap hafızaya yazılınca ekranı yeniler)
                except Exception as e:
                    st.error(f"Hata oluştu: {str(e)}")