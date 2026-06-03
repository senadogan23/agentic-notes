# Eğer OpenAI kullanacaksan: pip install openai komutunu terminalde çalıştırmalısın
# Ortam değişkeni olarak OPENAI_API_KEY tanımlanmalı.
import os
from openai import OpenAI

class StudyAgent:
    def __init__(self, document_content: str = ""):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "ŞİMDİLİK_BOŞ_BIRAKIN"))
        self.document_content = document_content
        self.system_prompt = (
            "Sen 'Agentic-Notes' isimli gelişmiş bir yapay zeka ders asistanısın. "
            "Sana verilen ders notlarını analiz ederek öğrencilerin sınav döneminde en yüksek verimi "
            "almasını sağlarsın. Yanıtlarını markdown formatında, düzenli ve profesyonel ver."
        )

    def execute_tool(self, tool_name: str) -> str:
        """Agent'ın tetikleyeceği özel araçlar (Tools)"""
        if not self.document_content:
            return "Lütfen önce bir ders notu yükleyin."

        if tool_name == "ozet_cıkar":
            prompt = f"Aşağıdaki ders notunun kapsamlı bir özetini çıkar, önemli kavramları kalın yaz:\n\n{self.document_content}"
        elif tool_name == "soru_uret":
            prompt = f"Aşağıdaki ders notundan sınavda çıkabilecek 5 adet çoktan seçmeli, 5 adet klasik soru ve cevap anahtarı üret:\n\n{self.document_content}"
        elif tool_name == "flashcard":
            prompt = f"Aşağıdaki notlardan aktif hatırlama (active recall) için Soru:Cevap şeklinde flashcard kartları hazırla:\n\n{self.document_content}"
        else:
            return "Bilinmeyen araç."

        # LLM'e istek gönderme alanı
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini", # Veya projenize göre uygun model
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"LLM Bağlantı Hatası (API anahtarınızı kontrol edin): {str(e)}"