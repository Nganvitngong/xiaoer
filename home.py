import streamlit as st

def run_home():
    # --- CSS CỐ ĐỊNH LAYOUT TUYỆT ĐỐI ---
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
        <style>
            /* Reset giao diện Streamlit */
            .block-container { padding: 0 !important; max-width: 100% !important; }
            [data-testid="stHeader"], [data-testid="stFooter"] { display: none !important; }
            .stApp { background-color: #ffffff; font-family: 'Poppins', sans-serif; }

            /* --- PHẦN 1: HERO SECTION (Gộp tất cả để tránh văng layout) --- */
            .hero-section {
                background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
                            url('https://i.pinimg.com/736x/1e/c4/c8/1ec4c8abfad522beca105366d71012f0.jpg');
                background-size: cover;
                background-position: center;
                height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                color: white;
                width: 100%;
            }

            .logo-container img {
                width: 130px; height: 130px;
                border-radius: 50%; object-fit: cover;
                border: 4px solid #52e067; margin-bottom: 20px;
                background: white;
            }

            .hero-title { font-size: 65px; font-weight: 700; margin: 0; line-height: 1.2; }
            .hero-subtitle { font-size: 22px; opacity: 0.9; margin-top: 10px; margin-bottom: 35px; }

            /* NÚT BẤM HTML THUẦN - Đảm bảo liên kết và thẩm mỹ */
            .btn-explore {
                background: #52e067;
                color: white !important;
                border-radius: 50px;
                padding: 15px 50px;
                font-weight: 700;
                font-size: 18px;
                text-decoration: none !important;
                display: inline-block;
                box-shadow: 0 10px 25px rgba(82, 224, 103, 0.4);
                transition: 0.3s ease;
                border: none;
            }
            .btn-explore:hover {
                transform: translateY(-3px);
                box-shadow: 0 15px 30px rgba(82, 224, 103, 0.6);
            }

            /* --- PHẦN 2: THÔNG TIN CHI TIẾT --- */
            .info-section {
                max-width: 1100px; margin: -80px auto 100px;
                background: white; padding: 50px;
                border-radius: 20px; box-shadow: 0 20px 50px rgba(0,0,0,0.1);
                display: grid; grid-template-columns: 1fr 1.2fr;
                gap: 50px; align-items: center;
                position: relative; z-index: 10;
            }
            .info-img img { width: 100%; border-radius: 15px; height: 350px; object-fit: cover; }
            .info-content h2 { color: #222; font-size: 32px; margin-bottom: 20px; }
            .info-content p { color: #666; line-height: 1.8; }
            .tag-green { color: #52e067; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px; font-size: 13px; }
        </style>
    """, unsafe_allow_html=True)

    # --- RENDER PHẦN 1: HERO (Nút bấm gắn tham số điều hướng ?nav=login) ---
    st.markdown(f"""
        <div class="hero-section">
            <div class="logo-container">
                <img src="https://i.pinimg.com/736x/16/1f/5c/161f5c81d2da6626d1ed2b2efdf57202.jpg">
            </div>
            <h1 class="hero-title">Cú Dạy Sử</h1>
            <p class="hero-subtitle">Hành trình khám phá Lịch sử cùng Trợ lý AI thông minh</p>
            <a href="/?nav=login" class="btn-explore" target="_self">Khám phá ngay</a>
        </div>
    """, unsafe_allow_html=True)

    # --- RENDER PHẦN 2: VỀ DỰ ÁN ---
    st.markdown(f"""
        <div class="info-section">
            <div class="info-img">
                <img src="https://images.unsplash.com/photo-1461360370896-922624d12aa1?q=80&w=2070">
            </div>
            <div class="info-content">
                <span class="tag-green">Về dự án</span>
                <h2>Ứng dụng Công nghệ AI vào dạy học Lịch sử</h2>
                <p>
                    Dự án "Cú Dạy Sử" được phát triển nhằm thay đổi cách tiếp cận môn Lịch sử truyền thống. 
                    Bằng việc ứng dụng mô hình ngôn ngữ lớn (LLM) và kỹ thuật RAG, chúng tôi mang đến một 
                    người bạn đồng hành thông thái, giúp học sinh tra cứu, ôn luyện và hiểu sâu hơn về 
                    các cột mốc hào hùng của dân tộc theo bộ sách "Kết nối tri thức".
                </p>
                <br>
                <p style="font-style: italic; color: #888;">
                    "Lịch sử không chỉ là những trang sách, đó là những câu chuyện cần được kể lại bằng ngôn ngữ của tương lai."
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    run_home()