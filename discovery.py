import streamlit as st

def run_discovery():
    # --- 1. CẤU HÌNH HỆ THỐNG ĐỂ ẨN THANH CUỘN VÀ LÀM TRONG SUỐT ---
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@100;400;700;800;900&display=swap&subset=vietnamese" rel="stylesheet">
        <style>
            /* Ẩn dải cuộn mặc định trên toàn bộ trang */
            ::-webkit-scrollbar { display: none; }
            html, body { 
                -ms-overflow-style: none; 
                scrollbar-width: none; 
                background: transparent !important;
            }

            /* Ép Streamlit container trong suốt để thấy ảnh nền */
            .stAppViewContainer, .stApp, .main, .block-container { 
                background: transparent !important; 
                padding-top: 2rem !important;
            }

            /* Ảnh nền cố định */
            .fixed-background {
                position: fixed;
                top: 0; left: 0; width: 100vw; height: 100vh;
                background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.7)), 
                                  url('https://i.pinimg.com/736x/1e/c4/c8/1ec4c8abfad522beca105366d71012f0.jpg');
                background-size: cover;
                background-position: center;
                z-index: -1;
            }

            /* Thiết kế Card Kho tư liệu */
            .discovery-card {
                background-color: rgba(255, 255, 255, 0.9); 
                border-radius: 24px;
                overflow: hidden;
                box-shadow: 0 10px 25px rgba(0,0,0,0.3);
                transition: all 0.4s ease;
                margin-bottom: 20px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }

            .discovery-card:hover {
                transform: translateY(-10px);
                border-color: #52e067; 
            }

            .card-img { width: 100%; height: 200px; object-fit: cover; }
            .card-body { padding: 20px; text-align: left; }
            .card-title { font-size: 18px; font-weight: 800; color: #1e293b; margin-bottom: 5px; }
            .card-desc { font-size: 14px; color: #475569; }

            /* Thiết kế Card Thực tế ảo (VR) */
            .vr-card-item {
                position: relative;
                border-radius: 20px;
                overflow: hidden;
                height: 180px;
                margin-bottom: 15px;
                box-shadow: 0 8px 20px rgba(0,0,0,0.4);
                transition: 0.3s;
            }

            .vr-card-item:hover { transform: scale(1.03); border: 2px solid #52e067; }
            .vr-img-bg { width: 100%; height: 100%; object-fit: cover; filter: brightness(0.7); }
            .vr-text-overlay {
                position: absolute;
                bottom: 0; left: 0; right: 0;
                padding: 15px;
                background: linear-gradient(to top, rgba(0, 0, 0, 0.8), transparent);
                color: white;
            }

            .section-header {
                text-align: center;
                color: #52e067 !important; 
                font-weight: 900;
                text-transform: uppercase;
                margin: 40px 0;
                text-shadow: 0 4px 10px rgba(0,0,0,0.5);
            }

            /* Nút bấm đồng bộ Home */
            div.stButton > button {
                background-color: #52e067 !important; 
                color: white !important;
                border-radius: 50px !important; 
                font-weight: 800 !important;
                height: 45px !important;
                width: 100%;
            }
        </style>
        
        <div class="fixed-background"></div>
    """, unsafe_allow_html=True)

    # DỮ LIỆU TƯ LIỆU
    articles = [
        {"title": "Chiến Tranh Lạnh", "desc": "Tóm tắt các nội dung về Chiến tranh Lạnh", "img": "https://cdn2.fptshop.com.vn/unsafe/800x0/chien_tranh_lanh_la_gi_2_170d83d749.png", "url": "https://nghiencuuquocte.org/2015/01/18/chien-tranh-lanh/"},
        {"title": "ASEAN", "desc": "Tóm tắt lịch sử hình thành và phát triển của ASEAN", "img": "https://daknong.1cdn.vn/thumbs/1200x630/2023/08/07/image.nhandan.vn-uploaded-2023-ovhunoh-2023_08_07-_asean-01-630.jpg", "url": "https://yeulichsu.edu.vn/lich-su-hinh-thanh-asean"},
        {"title": "Cách mạng tháng 8", "desc": "Nội dung quan trọng của Cách mạng Tháng Tám năm 1945", "img": "https://th.bing.com/th/id/R.290bec70072e023b6c01928292ee8178?rik=nNrARDMTUqs7MA&riu=http%3a%2f%2fhoanghamobile.com%2ftin-tuc%2fwp-content%2fuploads%2f2023%2f07%2fcach-mang-thang-8-6.jpg&ehk=rxe4SO2Jqz%2b9%2b1rl0gBGIxvTYWEpeM%2fbhA01GBCX9Ys%3d&risl=&pid=ImgRaw&r=0", "url": "https://vi.wikipedia.org/wiki/C%C3%A1ch_m%E1%BA%A1ng_Th%C3%A1ng_T%C3%A1m"},
        {"title": "Vị lãnh tụ Hồ Chí Minh", "desc": "Cuộc đời và sự nghiệp cách mạng vẻ vang của Chủ tịch Hồ Chí Minh", "img": "https://bvhttdl.gov.vn/uploads/oldscontents/20201026145330541/5-15875454604011998230042-16036836450041268704454-1603763865239-1603763866080171610522.jpg", "url": "https://vi.wikipedia.org/wiki/H%E1%BB%93_Ch%C3%AD_Minh"},
        {"title": "Dấu ấn Hồ Chí Minh", "desc": "9 dấu ấn lớn trong cuộc đời của chủ tịch Hồ Chí Minh", "img": "https://tuoitredhdn.udn.vn/uploads/images/E1(1).JPG", "url": "https://tuoitredhdn.udn.vn/chu-tich-ho-chi-minh/cuoc-doi-va-su-nghiep-cmbs1p43tj/9-dau-an-lon-trong-cuoc-doi-cua-chu-tich-ho-chi-minh-956.html"},
        {"title": "Liên Hợp Quốc", "desc": "Tìm hiểu thông tin về Liên Hợp Quốc", "img": "https://media-cdn-v2.laodong.vn/Storage/NewsPortal/2022/10/22/1108110/LHQ.jpg", "url": "https://vi.wikipedia.org/wiki/Li%C3%AAn_H%E1%BB%A3p_Qu%E1%BB%91c"},
        {"title": "Chiến dịch Hồ Chí Minh", "desc": " Tìm hiểu ngay về chiến dịch này", "img": "https://vov2.vov.vn/sites/default/files/styles/large/public/2022-04/muaxuan751_ihoq.jpg", "url": "https://vi.wikipedia.org/wiki/Chi%E1%BA%BFn_d%E1%BB%8Bch_H%E1%BB%93_Ch%C3%AD_Minh"},
        {"title": "Chiến dịch Điện Biên Phủ", "desc": "Chiến thắng lịch sử Điện Biên Phủ (7/5/1954)", "img": "https://media-cdn-v2.laodong.vn/Storage/NewsPortal/2023/3/12/1156768/11-2.jpg", "url": "https://dinhnghia.vn/chien-thang-lich-su-dien-bien-phu.html"},
        {"title": "Cuộc kháng chiến chống Mỹ cứu nước", "desc": "21 năm kháng chiến chống Mỹ cứu nước (1954-1975)", "img": "https://thethaovanhoa.mediacdn.vn/372676912336973824/2025/4/26/vnapotalchiendichhochiminh-chiendichquyetchienchienluoctrongcuoctongtiencongvanoidaymuaxuan19757985184-1745629327394169319730.jpg", "url": "https://thcsanphudong.hcm.edu.vn/theo-dong-lich-su/21-nam-khang-chien-chong-my-cuu-nuoc-1954-1975/ctfull/104857/693958"},
    ]

    # DỮ LIỆU VR360
    vr_tours = [
        {"name": "Bảo tàng Lịch sử Quân sự VN", "img": "https://backstage.vn/storage/2024/06/he-thong-bao-tang-ha-noi-3.jpg", "url": "https://vr360.yoolife.vn/bao-tang-lich-su-quan-su-viet-nam-zmuseumc118u26724"},
        {"name": "Văn miếu Quốc tử Giám", "img": "https://nld.mediacdn.vn/291774122806476800/2024/1/1/van-mieu-quoc-tu-giam-8-17040745334591615475843.jpg", "url": "https://vr360.yoolife.vn/van-mieu-zbdsc880u26822"},
        {"name": "Bến Nhà Rồng", "img": "https://owa.bestprice.vn/images/media/3a13e27f-9197-4a73-9457-100ea67fdc8b-61ef603f31244.png", "url": "https://yoolife.vn/@ditichhochiminh/post/7b43482a7b764cb0899df102e8bdccdf"},
        {"name": "Chiến dịch Điện biên Phủ", "img": "https://media-cdn-v2.laodong.vn/Storage/NewsPortal/2023/3/12/1156768/11-2.jpg", "url": "https://yoolife.vn/@yoolifevr360giaoduc/post/b8328d4af6fb4cb99e394f9f031e01fe"},
        {"name": "Chiến dịch Hồ Chí Minh", "img": "https://vov2.vov.vn/sites/default/files/styles/large/public/2022-04/muaxuan751_ihoq.jpg", "url": "https://yoolife.vn/@yoolifevr360giaoduc/post/7ee35eeee46846b78a26dd7c0af38ba1"},
        {"name": "Cách mạng Tháng Tám 1945", "img": "https://cdn.tgdd.vn/Files/2022/07/26/1450679/nguon-goc-y-nghia-ngay-cach-mang-thang-tam-thanh-cong-202207262209323836.jpg", "url": "https://yoolife.vn/@yoolifevr360giaoduc/post/32af8fbe30f84a9e8e19f178e44b3be0"},
        {"name": "Bảo tàng Hà Nội", "img": "https://live.staticflickr.com/8103/8561236629_9fcaafce9e_b.jpg", "url": "https://yoolife.vn/@yoolifevr360vanhoa/post/5044c78543ef4d8eae5744f321c11fb8"},
        {"name": "Bảo tàng ảo về vũ khí", "img": "https://cdn.xanhsm.com/2024/12/ff2821e9-bao-tang-vu-khi-8.jpg", "url": "https://yoolife.vn/@YooLifeOfficial/post/52a2e9c415a8421db698a47817598f41"},
    ]

    # Cố định Pop-up
    @st.dialog("Nội dung tư liệu", width="large")
    def show_article(url):
        # Ẩn thanh cuộn của iframe và fix height
        st.markdown("""
            <style>
                iframe { border: none !important; border-radius: 15px; }
                ::-webkit-scrollbar { display: none; }
            </style>
        """, unsafe_allow_html=True)
        st.components.v1.iframe(url, height=750, scrolling=True)

    # 1. HIỂN THỊ KHO TƯ LIỆU
    st.markdown("<h1 class='section-header'>Kho Tư Liệu Lịch Sử</h1>", unsafe_allow_html=True)
    
    for i in range(0, len(articles), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(articles):
                item = articles[i + j]
                with cols[j]:
                    st.markdown(f"""
                        <div class="discovery-card">
                            <img src="{item['img']}" class="card-img">
                            <div class="card-body">
                                <div class="card-title">{item['title']}</div>
                                <div class="card-desc">{item['desc']}</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button("KHÁM PHÁ NGAY", key=f"btn_{i+j}", use_container_width=True):
                        show_article(item['url'])

    # 2. HIỂN THỊ VR360
    st.markdown("<h1 class='section-header'>Thực Tế Ảo VR360</h1>", unsafe_allow_html=True)

    for i in range(0, len(vr_tours), 4):
        cols_vr = st.columns(4)
        for j in range(4):
            if i + j < len(vr_tours):
                tour = vr_tours[i + j]
                with cols_vr[j]:
                    st.markdown(f"""
                        <div class="vr-card-item">
                            <img src="{tour['img']}" class="vr-img-bg">
                            <div class="vr-text-overlay">
                                <div style="font-size: 14px; font-weight: 800; line-height: 1.2;">{tour['name']}</div>
                                <div style="font-size: 11px; margin-top: 5px; color: #52e067; font-weight:800;">TRẢI NGHIỆM NGAY →</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Vào xem VR", key=f"vr_btn_{i+j}", use_container_width=True):
                        show_article(tour['url'])

if __name__ == "__main__":
    run_discovery()