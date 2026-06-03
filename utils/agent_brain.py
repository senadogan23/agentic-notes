import os
from openai import OpenAI
from dotenv import load_dotenv

# .env dosyasındaki değişkenleri sisteme yüklüyoruz
load_dotenv()

class StudyAgent:
    def __init__(self, document_content: str = ""):
        # Groq, OpenAI kütüphanesini destekler. 
        # Sadece gitmesi gereken adresi (base_url) Groq olarak değiştiriyoruz.
        self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=os.getenv("GROQ_API_KEY")
        )
        self.document_content = document_content
        
        # Agent'ın kişiliği ve sistem talimatı
        self.system_prompt = (
            "Sen 'Agentic-Notes' isimli gelişmiş bir yapay zeka ders asistanısın. "
            "Sana verilen ders notlarını analiz ederek öğrencilerin sınav döneminde en yüksek verimi "
            "almasını sağlarsın. Yanıtlarını markdown formatında, başlıklar, emojiler ve "
            "bold (kalın) metinler kullanarak son derece düzenli ve okunabilir şekilde ver."
        )

    def execute_tool(self, tool_name: str) -> str:
        """Agent'ın tetikleyeceği özel görevler (Tools)"""
        if not self.document_content:
            return "⚠️ Lütfen önce bir ders notu yükleyin."

        # Göreve göre prompt (talimat) hazırlıyoruz
        if tool_name == "ozet_cıkar":
            prompt = f"Aşağıdaki ders notunun kapsamlı, hiyerarşik bir özetini çıkar. Önemli terimleri kalın yaz:\n\n{self.document_content}"
        elif tool_name == "soru_uret":
            prompt = f"Aşağıdaki ders notundan sınavda çıkabilecek 5 adet çoktan seçmeli (şıkkı ve cevabı olan), 3 adet klasik soru ve detaylı cevap anahtarı üret:\n\n{self.document_content}"
        elif tool_name == "flashcard":
            prompt = f"Aşağıdaki notlardan aktif hatırlama (active recall) için Soru-Cevap şeklinde flashcard kartları hazırla:\n\n{self.document_content}"
        else:
            return "❌ Bilinmeyen araç."

        try:
            # Groq üzerindeki en güçlü açık kaynaklı modellerden biri: llama-3.3-70b-versatile
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3 # Yanıtların ders notuna sadık kalması için düşürdük
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ Groq API Bağlantı Hatası: {str(e)}"