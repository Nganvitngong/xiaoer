import streamlit as st
import json
import time
import os
import uuid
from streamlit_autorefresh import st_autorefresh
from supabase import create_client, Client
import threading

# --- CẤU HÌNH SUPABASE ---
SUPABASE_URL = "https://kdudfhkvpzfzkxcselxg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtkdWRmaGt2cHpmemt4Y3NlbHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzYzMjA4MjMsImV4cCI6MjA5MTg5NjgyM30.K-meGsEa0NtOZStbdwOdH-MLM7KrSD2c7uvsY41-G4U"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Tạo một ổ khóa toàn cục để chặn mọi hành vi ghi đè/ghi lặp
lock = threading.Lock()

def load_exam_data(exam_file):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(current_dir, "data", "exams", exam_file)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def run_quiz():
    # --- CSS DESIGN ---
    st.markdown("""
        <style>
        /* Chỉnh nền toàn bộ trang thành màu xanh dương nhạt pastel */
        .stApp {
            background-color: #EAEAEA;
        }

        /* Giữ nguyên các ô nội dung màu trắng */
        div[data-testid="stVerticalBlock"] > div:has(div.stRadio) {
            background-color: white; border-radius: 20px; padding: 25px;
            margin-bottom: 20px; border: 1px solid #f0f2f6; box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }
        .timer-box { text-align: center; background: white; padding: 15px; border-radius: 15px; border: 2px solid #7d5fff; margin-bottom: 15px; }
        .q-badge { display: inline-block; width: 35px; height: 35px; line-height: 35px; text-align: center; border-radius: 8px; margin: 3px; font-size: 13px; font-weight: bold; color: white; }
        button[data-testid="baseButton-primary"] { background-color: #ff4b4b !important; border: none !important; color: white !important; border-radius: 12px !important; padding: 10px 20px !important; font-weight: bold !important; }
        .stButton > button:not([data-testid="baseButton-primary"]) { background-color: #7d5fff !important; color: white !important; border: none !important; border-radius: 12px !important; padding: 12px 20px !important; }
        .user-info-banner { background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%); border-left: 5px solid #7d5fff; padding: 15px 20px; border-radius: 10px; margin-bottom: 25px; display: flex; justify-content: space-between; }
        .rule-box { background-color: #fff4e6; border-left: 5px solid #ff922b; padding: 15px; border-radius: 10px; margin-bottom: 20px; }
        .guide-box { background-color: #e7f5ff; border-left: 5px solid #228be6; padding: 15px; border-radius: 10px; margin-bottom: 20px; }
        </style>
    """, unsafe_allow_html=True)

    # --- KHỞI TẠO STATE ---
    if "quiz_step" not in st.session_state: st.session_state.quiz_step = 1
    if "user_info" not in st.session_state: 
        st.session_state.user_info = {"full_name": "Guest", "phone": "Chưa cập nhật"}
    if "current_exam" not in st.session_state: st.session_state.current_exam = None
    if "user_answers" not in st.session_state: st.session_state.user_answers = {}
    if "start_time" not in st.session_state: st.session_state.start_time = None
    if "is_saved" not in st.session_state: st.session_state.is_saved = False
    if "timer_active" not in st.session_state: st.session_state.timer_active = True

    # STEP 1: THÔNG TIN
    if st.session_state.quiz_step == 1:
        st.title("PHÒNG THI TRẮC NGHIỆM")
        st.markdown("""<div class="rule-box"><h4>⚠️ QUY ĐỊNH:</h4><ul><li>Đề thi 24 câu - 30 phút.</li><li>Hệ thống tự nộp bài khi hết giờ và lưu kết quả vĩnh viễn.</li></ul></div>""", unsafe_allow_html=True)
        with st.form("info_form"):
            # Lấy tên mặc định từ app.py nếu có
            default_name = st.session_state.user_info.get("full_name", "")
            if default_name == "Guest": default_name = ""
            
            input_name = st.text_input("Họ và tên thí sinh:", value=default_name)
            class_name = st.selectbox("Lớp:", ["12A1", "12A2", "12D1", "12D2", "12D3", "12C1", "12C3", "12B1", "12B2"])
            
            if st.form_submit_button("VÀO PHÒNG THI"):
                if input_name:
                    # CẬP NHẬT KEY 'full_name' ĐỂ ĐỒNG BỘ VỚI APP.PY
                    st.session_state.user_info.update({
                        "id": str(uuid.uuid4())[:8], 
                        "full_name": input_name, 
                        "class": class_name
                    })
                    st.session_state.quiz_step = 2
                    st.rerun()
                else: 
                    st.warning("Vui lòng nhập họ tên thí sinh nhé!")

    # STEP 2: LÀM BÀI
    elif st.session_state.quiz_step == 2:
        # Sử dụng đúng key 'full_name'
        st.markdown(f"""<div class="user-info-banner">
            <span>👤 <b>Thí sinh:</b> {st.session_state.user_info.get('full_name', 'Ẩn danh')}</span>
            <span>🏫 <b>Lớp:</b> {st.session_state.user_info.get('class', 'N/A')}</span>
            <span>🆔 <b>Mã số:</b> {st.session_state.user_info.get('id', '0000')}</span>
        </div>""", unsafe_allow_html=True)

        if st.session_state.current_exam is None:
            st.markdown("""<div class="guide-box">🎯 <b>HƯỚNG DẪN:</b> Chọn mã đề bên dưới để thi.</div>""", unsafe_allow_html=True)
            cols = st.columns(3)
            for i in range(1, 11):
                if cols[(i-1)%3].button(f"📄 Đề số {i}", key=f"exam_select_{i}", use_container_width=True):
                    data = load_exam_data(f"de_{i}.json")
                    if data:
                        st.session_state.current_exam = data
                        st.session_state.exam_name = f"Đề số {i}"
                        st.session_state.start_time = time.time()
                        st.rerun()
        else:
            if st.session_state.timer_active:
                st_autorefresh(interval=1000, key="quiz_timer")
            
            exam = st.session_state.current_exam
            remaining = int(1800 - (time.time() - st.session_state.start_time))
            
            if remaining <= 0 and not st.session_state.is_saved:
                st.session_state.timer_active = False
                st.session_state.quiz_step = 3
                st.rerun()

            col_main, col_side = st.columns([3, 1])
            with col_side:
                m, s = divmod(remaining, 60)
                st.markdown(f'<div class="timer-box"><small>THỜI GIAN</small><h2>{m:02d}:{s:02d}</h2></div>', unsafe_allow_html=True)
                
                q_cols = st.columns(4)
                for idx in range(len(exam)):
                    bg = "#2ecc71" if idx in st.session_state.user_answers else "#dee2e6"
                    q_cols[idx % 4].markdown(f'<div class="q-badge" style="background:{bg};">{idx+1}</div>', unsafe_allow_html=True)
                
                st.write("---")
                if st.button("NỘP BÀI 📤", type="primary", use_container_width=True):
                    st.session_state.confirm_sub_box = True

            with col_main:
                st.subheader(st.session_state.exam_name)
                for idx, q in enumerate(exam):
                    st.markdown(f"**Câu {idx+1}: {q['question']}**")
                    ans = st.radio(f"ans_{idx}", q['options'], key=f"radio_{idx}", index=None, label_visibility="collapsed")
                    if ans: st.session_state.user_answers[idx] = ans
                    st.write("")

            if "confirm_sub_box" in st.session_state:
                @st.dialog("Xác nhận nộp bài")
                def confirm_finish():
                    st.warning("Bạn chắc chắn muốn nộp bài? Thao tác này sẽ lưu kết quả vĩnh viễn.")
                    c1, c2 = st.columns(2)
                    
                    if c1.button("CÓ, NỘP BÀI", use_container_width=True, type="primary"):
                        with lock:
                            if not st.session_state.is_saved:
                                st.session_state.timer_active = False 
                                correct = sum(1 for i, q in enumerate(exam) if st.session_state.user_answers.get(i) == q['answer'])
                                score = (correct / len(exam)) * 100
                                try:
                                    supabase.table("student_results").insert({
                                        "student_id": st.session_state.user_info.get('id'), 
                                        "student_name": st.session_state.user_info.get('full_name'),
                                        "class_name": st.session_state.user_info.get('class'), 
                                        "exam_name": st.session_state.exam_name,
                                        "score": score, 
                                        "correct_answers": correct
                                    }).execute()
                                    st.session_state.is_saved = True
                                except:
                                    pass
                        st.session_state.quiz_step = 3
                        if "confirm_sub_box" in st.session_state: del st.session_state.confirm_sub_box
                        st.rerun()

                    if c2.button("KHÔNG, LÀM TIẾP", use_container_width=True):
                        if "confirm_sub_box" in st.session_state: del st.session_state.confirm_sub_box
                        st.rerun()
                confirm_finish()

    # STEP 3: KẾT QUẢ
    elif st.session_state.quiz_step == 3:
        st.balloons()
        exam = st.session_state.current_exam
        correct = sum(1 for i, q in enumerate(exam) if st.session_state.user_answers.get(i) == q['answer'])
        
        st.markdown(f"""<div style="background:white; padding:25px; border-radius:20px; text-align:center; border:2px solid #7d5fff; box-shadow: 0 10px 30px rgba(0,0,0,0.05);">
            <h2 style="color: #7d5fff; margin-bottom: 5px;">HOÀN THÀNH BÀI THI!</h2>
            <p>Thí sinh: <b>{st.session_state.user_info.get('full_name')}</b> - Lớp: <b>{st.session_state.user_info.get('class')}</b></p>
            <hr>
            <div style="display:flex; justify-content:space-around; margin-top:20px;">
                <div><small>ĐIỂM SỐ</small><h1 style="color: #7d5fff; margin:0;">{(correct/len(exam))*100:.1f}</h1></div>
                <div><small>CÂU ĐÚNG</small><h1 style="color: #2ecc71; margin:0;">{correct}/{len(exam)}</h1></div>
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("### 📋 CHI TIẾT ĐÁP ÁN & GIẢI THÍCH")
        for idx, q in enumerate(exam):
            u_ans = st.session_state.user_answers.get(idx, "Chưa làm")
            is_right = (u_ans == q['answer'])
            with st.expander(f"Câu {idx+1}: {'✅ ĐÚNG' if is_right else '❌ SAI'}"):
                st.write(f"**Câu hỏi:** {q['question']}")
                st.write(f"**Bạn chọn:** {u_ans}")
                st.markdown(f"<b style='color:green;'>Đáp án đúng: {q['answer']}</b>", unsafe_allow_html=True)
                st.info(f"💡 {q['explanation']}")

        if st.button("🔄 LÀM ĐỀ KHÁC NGAY"):
            # Giữ lại thông tin user để không phải nhập lại tên ở Step 1
            kept_user = st.session_state.user_info
            for key in list(st.session_state.keys()): del st.session_state[key]
            st.session_state.user_info = kept_user
            st.rerun()