import streamlit as st
import random
import string

BACKGROUND_URL = "https://i.pinimg.com/736x/1e/c4/c8/1ec4c8abfad522beca105366d71012f0.jpg"

def generate_user_id():
    prefix = "CDS"
    random_part = ''.join(random.choices(string.digits, k=5))
    return f"{prefix}-{random_part}"

def login_page():
    st.markdown(f"""
        <style>
        [data-testid="stSidebar"] {{
            display: none !important;
        }}
        .main .block-container {{
            max-width: 100%;
            padding: 0;
        }}
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
                        url('{BACKGROUND_URL}');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        div[role="dialog"] {{
            border-radius: 20px;
            border: 2px solid #7d5fff;
        }}
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style='text-align: center; color: white; padding-top: 150px;'>
            <h1 style='font-size: 60px; font-weight: 700;'>🦉 Cú Dạy Sử</h1>
            <p style='font-size: 22px;'>Hành trình di sản trong tầm tay bạn</p>
        </div>
    """, unsafe_allow_html=True)

    @st.dialog("Đăng ký thành viên Cú Dạy Sử")
    def show_login_dialog():
        st.markdown("<p style='text-align: center; color: #666;'>Chào bạn! Hãy để lại thông tin để bắt đầu hành trình nhé.</p>", unsafe_allow_html=True)
        
        full_name = st.text_input("Họ và tên của bạn")
        phone = st.text_input("Số điện thoại")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Đăng nhập 🦉", use_container_width=True, type="primary"):
                if full_name and phone:
                    st.session_state.logged_in = True
                    st.session_state.user_info = {
                        "full_name": full_name,
                        "phone": phone,
                        "user_id": generate_user_id()
                    }

                    # 🔥 FIX QUAN TRỌNG: dùng query param thay vì page
                    st.query_params.update({"p": "chatbot"})
                    st.rerun()
                else:
                    st.error("Vui lòng điền đủ thông tin nha!")

        with col2:
            if st.button("Quay lại", use_container_width=True):
                st.query_params.clear()
                st.rerun()

    if "login_dialog_opened" not in st.session_state:
        st.session_state.login_dialog_opened = True
        show_login_dialog()
    else:
        st.markdown("<div style='text-align:center; margin-top:20px;'>", unsafe_allow_html=True)
        if st.button("Mở khung đăng nhập"):
            show_login_dialog()
        st.markdown("</div>", unsafe_allow_html=True)
