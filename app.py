from utils.file_manager import save_uploaded_file, read_file_content
from utils.agent_brain import StudyAgent
import streamlit as st  # Web arayüzünü oluşturmak için Streamlit kütüphanesini dahil ediyoruz.
from dotenv import load_dotenv

load_dotenv()  # .env dosyasını projenin en başında sisteme zorla yüklüyoruz

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

# Projenin beyninin başarıyla bağlandığını belirten tatlı bir yeşil kutu
st.success("🤖 Llama 3.3 Süper Bilgisayarı Bağlandı! Ders notlarınızı analiz etmeye hazır.")

# Kullanıcının ders notlarını yükleyebileceği bir dosya yükleme alanı oluşturuyoruz.
# Şimdilik pdf ve txt formatındaki dosyaları kabul ediyoruz.
uploaded_file = st.file_uploader("Ders notunu veya özetini yükle (.txt, .pdf)", type=["txt", "pdf"])

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

    # Geçmiş mesajları ekrana basan döngü
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            # Eğer asistan mesajı bir flashcard çıktısı ise özel kart tasarımı yap
            if message["role"] == "assistant" and "### KART" in message["content"]:
                st.subheader("🗂️ Üretilen Bilgi Kartları")
                
                # Çıktıyı kartlara bölüp listeliyoruz
                raw_cards = message["content"].split("### KART")
                for raw_card in raw_cards:
                    if raw_card.strip():
                        card_content = raw_card.strip()
                        st.markdown(
                            f"""
                            <div style="
                                background-color: #262730; 
                                padding: 20px; 
                                border-radius: 10px; 
                                border-left: 5px solid #FF4B4B; 
                                margin-bottom: 15px;
                                box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
                            ">
                                <strong>🃏 KART</strong><br><br>
                                {card_content}
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                
                # --- BUGÜNÜN ZAFERİ: Markdown İndirme Butonu ---
                st.write("---")
                st.download_button(
                    label="📥 Bu Kartları Markdown Olarak İndir",
                    data=message["content"],
                    file_name="agentic_notes_flashcards.md",
                    mime="text/markdown",
                    help="Kartları .md formatında indirerek dilediğin cihazda çalışabilirsin!"
                )
            else:
                # Normal kullanıcı mesajları ve düz asistan yanıtları eski usul görünsün
                st.markdown(message["content"])

    # Kullanıcıdan yeni mesaj alma alanı (Chat Input)
    if user_input := st.chat_input("Ders notu hakkında bir soru sorun..."):
        # Kullanıcının yazdığı mesajı hafızaya kaydet
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Agent'ı ve LLM'i devreye sokup cevap üretiyoruz
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
            # Asistanın cevabını hafızaya ekleyip sayfayı yeniliyoruz, böylece akış bozulmuyor
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()
        except Exception as e:
            st.error(f"Hata oluştu: {str(e)}")