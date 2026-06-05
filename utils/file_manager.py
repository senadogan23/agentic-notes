import os
from pypdf import PdfReader

def save_uploaded_file(uploaded_file) -> str:
    """Yüklenen dosyayı güvenli bir şekilde data/ klasörüne kaydeder."""
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        
    file_path = os.path.join(data_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def read_file_content(file_path: str) -> str:
    """Dosya uzantısına göre (.txt veya .pdf) içeriği okur ve metin olarak döner."""
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == ".txt":
        # Klasik metin dosyası okuma
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
            
    elif ext == ".pdf":
        # PDF dosyası okuma mekanizması
        text_content = ""
        try:
            reader = PdfReader(file_path)
            # PDF içindeki tüm sayfaları tek tek gezip metinleri birleştiriyoruz
            for page in reader.pages:
                extracted_text = page.extract_text()
                if extracted_text:  # Eğer sayfada okunabilir bir metin varsa ekle
                    text_content += extracted_text + "\n"
            return text_content
        except Exception as e:
            return f"🚨 PDF okunurken bir hata oluştu: {str(e)}"
            
    else:
        return "⚠️ Desteklenmeyen dosya formatı!"