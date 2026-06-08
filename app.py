from utils.file_manager import save_uploaded_file, read_file_content
from utils.agent_brain import StudyAgent
import streamlit as st  # Web arayüzünü oluşturmak için Streamlit kütüphanesini dahil ediyoruz.
from fpdf import FPDF
from dotenv import load_dotenv

# Sayfa ayarları Streamlit'te her zaman İLK sırada olmalıdır
st.set_page_config(
    page_title="Agentic-Notes", 
    page_icon="🚀", 
    layout="wide"
)

# Dışarıdaki CSS dosyasını okuyan fonksiyon
def load_css(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# CSS dosyamızı yüklüyoruz
load_css("assets/style.css")

load_dotenv()  # .env dosyasını projenin en başında sisteme zorla yüklüyoruz



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

  # Geçmiş mesajları ekrana basan YENİ döngü
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant" and "### KART" in message["content"]:
                st.subheader("🗂️ Sınav Dönemi İnteraktif Bilgi Kartların")
                st.caption("💡 Kartların üzerine gelerek veya tıklayarak arkasındaki cevapları görebilirsin!")
                
                raw_cards = message["content"].split("### KART")
                card_count = 0
                
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Helvetica", "B", 16)
                pdf.cell(40, 10, "Agentic-Notes - Flashcard Kartlari", ln=True)
                pdf.ln(10)
                pdf.set_font("Helvetica", size=12)

                # HTML Grid Başlangıcı (Kare düzeni kuruyoruz)
                grid_html = '<div class="flashcard-grid">'

                for raw_card in raw_cards:
                    if raw_card.strip():
                        card_count += 1
                        card_content = raw_card.strip()
                        
                        # Metni Soru ve Cevap olarak ikiye bölüyoruz
                        parts = card_content.split("**Cevap:**")
                        soru_kısmi = parts[0].replace("**Soru:**", "").strip()
                        cevap_kısmi = parts[1].strip() if len(parts) > 1 else "Cevap detaylandırılamadı."
                        
                        # PDF için Türkçe karakter temizliği
                        # Türkçe karakterleri ve Helvetica fontunun desteklemediği özel sembolleri temizler
                        tr_map = str.maketrans({'ğ':'g','Ğ':'G','ş':'s','Ş':'S','ı':'i','İ':'I','ç':'c','Ç':'C','ö':'o','Ö':'O','ü':'u','Ü':'U'})
                        safe_content = card_content.translate(tr_map).replace("**Soru:**", "Soru:").replace("**Cevap:**", "Cevap:")
                        
                        # Font hatası vermemesi için desteklenmeyen karakterleri filtreler
                        pdf_clean_content = safe_content.encode('latin-1', 'ignore').decode('latin-1')
                        pdf.multi_cell(0, 10, f"KART {card_count}\n{pdf_clean_content}\n")
                        pdf.ln(5)

                        # style.css dosyasındaki animasyonları tetikleyen HTML yapısı
                        grid_html += f"""
                        <div class="flip-card" tabindex="0">
                            <div class="flip-card-inner">
                                <div class="flip-card-front">
                                    <span class="card-tag" style="background-color: #FF4B4B;">🃏 KART {card_count}</span>
                                    <div style="margin-top: 15px;">{soru_kısmi}</div>
                                </div>
                                <div class="flip-card-back">
                                    <span class="card-tag" style="background-color: #4CAF50;">✅ CEVAP</span>
                                    <div style="margin-top: 15px;">{cevap_kısmi}</div>
                                </div>
                            </div>
                        </div>
                        """
                
                grid_html += '</div>' # Grid Kapanış
                st.markdown(grid_html, unsafe_allow_html=True) # Kartları ekrana matris olarak bas
                
                # PDF İndirme ve Daha Fazla Üret Butonları
                pdf_bytes = pdf.output(dest='S')
                st.write("---")
                col_down, col_more = st.columns([1, 1])
                with col_down:
                    st.download_button(
                        label="📥 Kartları PDF Olarak İndir (Sınava Çalış)",
                        data=pdf_bytes,
                        file_name="ders_notu_flashcards.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                with col_more:
                    if st.button("🔄 Daha Fazla Kart Üretmek İster misiniz?", use_container_width=True):
                        st.info("💡 Notun diğer kısımlarından yeni kartlar üretmek için yukarıdaki butona tekrar basabilirsiniz!")
            else:
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