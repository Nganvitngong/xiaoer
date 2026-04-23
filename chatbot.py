import streamlit as st
import streamlit.components.v1 as components

def run_chatbot():
    # --- CSS ÉP FIT TUYỆT ĐỐI VỚI HEADER (64PX) ---
    st.markdown("""
        <style>
            /* 1. Loại bỏ hoàn toàn padding của Streamlit container */
            .main .block-container {
                padding: 0 !important;
                max-width: 100% !important;
                /* Chiều cao bằng toàn màn hình trừ đi 64px của Header */
                height: calc(100vh - 64px) !important;
                overflow: hidden !important;
            }
            
            /* 2. Ép Iframe chiếm trọn không gian còn lại */
            iframe {
                position: fixed;
                /* Đẩy xuống dưới Header 64px */
                top: 64px; 
                left: 0;
                width: 100vw !important;
                height: calc(100vh - 64px) !important;
                border: none !important;
                z-index: 1;
            }

            /* 3. Khử các lớp bọc trung gian để tránh tạo khoảng trắng */
            [data-testid="stVerticalBlock"], [data-testid="stHtml"], [data-testid="stComponentV1"] {
                padding: 0 !important;
                margin: 0 !important;
            }
            
            /* Ẩn các thành phần mặc định của Streamlit */
            footer {display: none !important;}
            header {display: none !important;}
        </style>
    """, unsafe_allow_html=True)

    bot_url = "https://agent.jotform.com/019dab22261d75be9a6011d575ae864209c7"
    
    # Nhúng chatbot với chiều cao được tính toán chính xác
    components.html(
        f"""
        <style>
            body, html {{ 
                margin: 0; 
                padding: 0; 
                height: 100vh; 
                overflow: hidden; 
                background-color: transparent;
            }}
            iframe {{ 
                width: 100vw; 
                height: 100vh; 
                border: none; 
            }}
        </style>
        <iframe src="{bot_url}" allow="microphone; camera"></iframe>
        """,
        height=0, # Trick để Streamlit không tự tạo container cao ngất ngưởng
    )

if __name__ == "__main__":
    run_chatbot()