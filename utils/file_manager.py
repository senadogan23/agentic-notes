import os

def save_uploaded_file(uploaded_file):
    """Yüklenen dosyayı 'data/' klasörüne kaydeder."""
    # data/ klasörü yoksa oluşturur
    if not os.path.exists("data"):
        os.makedirs("data")
        
    file_path = os.path.join("data", uploaded_file.name)
    
    # Dosyayı yazma modunda açıp içeriğini kaydediyoruz
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    return file_path

def read_file_content(file_path):
    """Kaydedilen dosyanın içeriğini metin olarak okur."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()