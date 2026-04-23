import os
import json
from supabase import create_client, Client

# --- THÔNG TIN KẾT NỐI (Dùng lại thông tin cũ của bạn) ---
URL = "https://kdudfhkvpzfzkxcselxg.supabase.co" 
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtkdWRmaGt2cHpmemt4Y3NlbHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzYzMjA4MjMsImV4cCI6MjA5MTg5NjgyM30.K-meGsEa0NtOZStbdwOdH-MLM7KrSD2c7uvsY41-G4U" 

supabase: Client = create_client(URL, KEY)

def upload_exams_from_json(folder_path):
    # Lấy đường dẫn tuyệt đối
    base_path = os.path.dirname(os.path.abspath(__file__))
    target_folder = os.path.join(base_path, folder_path)
    
    if not os.path.exists(target_folder):
        print(f"❌ Không tìm thấy thư mục: {target_folder}")
        return

    files = [f for f in os.listdir(target_folder) if f.endswith(".json")]
    print(f"📦 Tìm thấy {len(files)} file đề thi. Đang tải lên...")

    for filename in files:
        try:
            with open(os.path.join(target_folder, filename), "r", encoding="utf-8") as f:
                questions = json.load(f)
            
            # Lấy tên bài từ tên file (Ví dụ: "de_bai_1.json" -> "BÀI 1")
            lesson_num = filename.replace(".json", "").upper()
            
            for q in questions:
                data = {
                    "lesson_number": lesson_num,
                    "question": q["question"],
                    "options": q["options"], # Lưu nguyên mảng các lựa chọn
                    "answer": q["answer"],
                    "explanation": q.get("explanation", "Đang cập nhật giải thích...")
                }
                supabase.table("exams").insert(data).execute()
            
            print(f"✅ Đã tải lên thành công các câu hỏi từ: {filename}")
            
        except Exception as e:
            print(f"❌ Lỗi khi xử lý file {filename}: {e}")

if __name__ == "__main__":
    # Nga hãy chắc chắn tên thư mục chứa file JSON là 'data/exams' nhé
    upload_exams_from_json("data/exams")
    print("\n🏁 HOÀN TẤT ĐẨY DỮ LIỆU TRẮC NGHIỆM!")