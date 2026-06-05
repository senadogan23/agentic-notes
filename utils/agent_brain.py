import os
from openai import OpenAI
from dotenv import load_dotenv

# .env dosyasındaki değişkenleri sisteme yüklüyoruz
load_dotenv()

class StudyAgent:
    def __init__(self, document_content: str = ""):
        # Groq, OpenAI kütüphanesini destekler. 
        self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=os.getenv("GROQ_API_KEY") # Sadece bunu bırakıyoruz, varsayılan değeri sildik
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
        """Agent'ın tetikleyeceği özel görevler (Büyük dökümanları parçalayarak çalışır)"""
        if not self.document_content:
            return "⚠️ Lütfen önce bir ders notu yükleyin."

        # file_manager içindeki parçalama fonksiyonunu burada çağırabilmek için import ediyoruz
        from utils.file_manager import create_text_chunks
        
        # Metni 4000 karakterlik parçalara bölüyoruz
        chunks = create_text_chunks(self.document_content, chunk_size=4000, chunk_overlap=400)
        
        combined_results = []
        
        # Her bir parçayı sırayla Groq'a gönderip sonuçları topluyoruz
        for index, chunk in enumerate(chunks):
            if tool_name == "ozet_cıkar":
                prompt = f"Aşağıdaki ders notu parçasının (Kısım {index+1}) kapsamlı ve hiyerarşik bir özetini çıkar. Önemli terimleri kalın yaz:\n\n{chunk}"
            elif tool_name == "soru_uret":
                prompt = f"Aşağıdaki ders notu parçasına (Kısım {index+1}) dayanarak 2 adet çoktan seçmeli, 1 adet klasik sınav sorusu ve cevaplarını üret:\n\n{chunk}"
            elif tool_name == "flashcard":
                prompt = f"Aşağıdaki not parçası (Kısım {index+1}) için Soru-Cevap şeklinde flashcard kartları hazırla:\n\n{chunk}"
            else:
                return "❌ Bilinmeyen araç."

            try:
                response = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3
                )
                combined_results.append(response.choices[0].message.content)
            except Exception as e:
                return f"❌ Groq API Bağlantı Hatası (Kısım {index+1}): {str(e)}"

        # Tüm parçalardan gelen yanıtları şık bir şekilde birleştirip arayüze döndürüyoruz
        return "\n\n---\n\n".join(combined_results)