import os
from docx import Document
from supabase import create_client, Client
import google.generativeai as genai

# =============================================================
# 1. DÁN TRỰC TIẾP THÔNG TIN CỦA NGA VÀO ĐÂY
# =============================================================
# Lấy từ Supabase -> Settings -> API -> Project URL
URL = "https://kdudfhkvpzfzkxcselxg.supabase.co" 

# Lấy từ Supabase -> Settings -> API -> Project API keys (anon public)
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtkdWRmaGt2cHpmemt4Y3NlbHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzYzMjA4MjMsImV4cCI6MjA5MTg5NjgyM30.K-meGsEa0NtOZStbdwOdH-MLM7KrSD2c7uvsY41-G4U" 

# Lấy từ Google AI Studio (Gemini)
GEMINI_KEY = "AQ.Ab8RN6LYSFtSJVEe12LTP0s2YbTvYsTM1om726RACSPLNge67Q" 
# =============================================================

# KHỞI TẠO HỆ THỐNG
try:
    print("--- 🦉 ĐANG KẾT NỐI HỆ THỐNG ---")
    supabase: Client = create_client(URL, KEY)
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')
    print("✅ Kết nối Supabase và Gemini thành công!\n")
except Exception as e:
    print(f"❌ Lỗi kết nối: {e}")
    exit()

def get_lesson_title(text_preview):
    """Dùng AI để lấy tiêu đề bài học từ nội dung file"""
    try:
        prompt = f"Trích xuất tên tiêu đề chính của bài học lịch sử từ đoạn văn sau (chỉ trả về tên tiêu đề): {text_preview}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except:
        return "Tiêu đề bài học"

def upload_lessons(folder_path):
    # Kiểm tra thư mục có tồn tại thực sự không
    if not os.path.exists(folder_path):
        print(f"❌ Vẫn không thấy thư mục tại: {folder_path}")
        return

    # Lấy danh sách file .docx
    files = [f for f in os.listdir(folder_path) if f.endswith(".docx")]
    
    if not files:
        print(f"❓ Folder có tồn tại nhưng không thấy file .docx nào bên trong.")
        return

    print(f"📦 Tìm thấy {len(files)} file bài học. Đang bắt đầu tải lên...")

    for filename in files:
        try:
            print(f"🔄 Đang xử lý: {filename}...")
            path = os.path.join(folder_path, filename)
            doc = Document(path)
            full_text = "\n".join([p.text for p in doc.paragraphs])
            
            lesson_number = filename.replace(".docx", "").upper()
            lesson_title = get_lesson_title(full_text[:1000])
            
            data = {
                "lesson_number": lesson_number,
                "lesson_title": lesson_title,
                "content": full_text
            }
            
            supabase.table("lessons").insert(data).execute()
            print(f"   ✨ Xong: {lesson_number} - {lesson_title}")
            
        except Exception as e:
            print(f"   ❌ Lỗi file {filename}: {e}")

if __name__ == "__main__":
    # TỰ ĐỘNG XÁC ĐỊNH ĐƯỜNG DẪN TỐI ƯU
    # Lấy thư mục mà file upload_data.py đang đứng
    base_path = os.path.dirname(os.path.abspath(__file__))
    # Kết hợp với data/docs
    target_folder = os.path.join(base_path, "data", "docs")
    
    print(f"🔎 Đường dẫn máy tính đang quét: {target_folder}")
    upload_lessons(target_folder)
    print("\n🏁 QUÁ TRÌNH HOÀN TẤT!")