import streamlit as st
import time
import random
import folium
from streamlit_folium import folium_static
import streamlit.components.v1 as components

def show_filter_page():
    st.title("🏡 REAL-ESTATE")
    st.subheader("권병진님, 원하는 집을 찾아드려요!")
    
    st.markdown("### 원하는 조건을 선택하세요!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        bs = st.checkbox("병세권 (응급실 가까이)")
        ys = st.checkbox("역세권 (대중교통 가까이)")
        js = st.checkbox("주세권 (주차장 가까이)")
    
    with col2:
        new_building = st.checkbox("신축 여부 (최근 5년)")
        building_type = st.selectbox("건물 유형", ["전체", "아파트", "오피스텔", "연립다세대"])
    
    with col3:
        size = st.slider("건물 면적 (평)", 10, 100, (20, 80))
        price = st.selectbox("가격 범위", ["1억 이하", "1~3억", "3~5억", "5~10억", "10억 이상"])
        floor = st.selectbox("층 선택", ["전체", "1~5층 (저층)", "6~8층 (중층)", "9층 이상 (고층)"])
    
    if st.button("🏠 추천 받기"):
        st.session_state["filters"] = {
            "병세권": bs, "역세권": ys, "주세권": js,
            "신축 여부": new_building, "건물 유형": building_type,
            "건물 면적": size, "가격 범위": price, "층": floor
        }
        st.session_state["page"] = "splash"
        st.rerun()
        
def show_splash_page():
    st.title("🔍 선택한 조건 정리")
    
    if st.button("🔙 뒤로 가기", key="back_splash"):
        st.session_state["page"] = "filters"
        st.rerun()
    
    st.markdown("**아래 조건으로 매물을 찾고 있어요!**")
    
    filters = st.session_state["filters"]
    keywords = [f"🏷️ {k}: {v}" for k, v in filters.items() if v]
    
    st.markdown("**선택한 조건:**  \n" + "  \n".join(keywords))  # 줄 바꿈 추가

    if st.button("확인", key="confirm_splash"):  
        st.session_state["loading"] = True
        st.session_state["page"] = "loading"
        st.rerun()
        
def show_loading_page():
    with st.spinner("🏡 추천 매물을 찾고 있습니다..."):
        time.sleep(3)  
    st.session_state["page"] = "results"
    st.rerun()
        
def show_results_page():
    st.title("📍 추천 매물 지도")
    
    if st.button("🔙 뒤로 가기", key="back_results"):
        st.session_state["page"] = "filters"
        st.rerun()
    
    recommendations = [
        {"이름": "래미안 아파트", "가격": "4억", "면적": "35평", "위치": "서울 강남구", "lat": 37.497, "lon": 127.027},
        {"이름": "자이 오피스텔", "가격": "3.2억", "면적": "25평", "위치": "서울 서초구", "lat": 37.502, "lon": 127.024},
        {"이름": "힐스테이트 주택", "가격": "2.8억", "면적": "30평", "위치": "서울 마포구", "lat": 37.551, "lon": 126.980},
        {"이름": "롯데캐슬 아파트", "가격": "6억", "면적": "40평", "위치": "서울 송파구", "lat": 37.506, "lon": 127.055},
        {"이름": "푸르지오 오피스텔", "가격": "5억", "면적": "28평", "위치": "서울 동작구", "lat": 37.479, "lon": 126.921}
    ]
    
    map = folium.Map(location=[37.5, 127.0], zoom_start=12)
    
    for rec in recommendations:
        folium.Marker(
            location=[rec["lat"], rec["lon"]],
            popup=f"<b>{rec['이름']}</b><br>💰 {rec['가격']}<br>📏 {rec['면적']}<br>📍 {rec['위치']}",
            icon=folium.Icon(color="blue")
        ).add_to(map)
    
    folium_static(map)
    
    st.subheader("🏡 추천 매물 Top 5")
    container = st.container()
    with container:
        cols = st.columns(len(recommendations))
        for idx, rec in enumerate(recommendations):
            with cols[idx]:
                st.write(f"### {rec['이름']}")
                st.write(f"1. 가격: {rec['가격']}")
                st.write(f"2. 면적: {rec['면적']}")
                st.write(f"3. 위치: {rec['위치']}")
                st.image("https://source.unsplash.com/200x150/?house,apartment", use_container_width=True)
    
if "page" not in st.session_state:
    st.session_state["page"] = "filters"
    
if st.session_state["page"] == "filters":
    show_filter_page()
elif st.session_state["page"] == "splash":
    show_splash_page()
elif st.session_state["page"] == "loading":
    show_loading_page()
elif st.session_state["page"] == "results":
    show_results_page()