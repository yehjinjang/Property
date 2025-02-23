import streamlit as st
import time
import folium
from streamlit_folium import folium_static
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Address, Building, Tag, RealestateDeal
from sqlalchemy.orm import aliased  

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
session = Session()

st.set_page_config(page_title="🏡 부동산 추천 서비스", layout="wide")

# 사용자 입력 필터 화면
def show_filter_page():
    st.title("🏡 REAL-ESTATE")
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
        st.session_state["page"] = "loading"
        st.rerun()

# 로딩 화면
def show_loading_page():
    with st.spinner("🏡 추천 매물을 찾고 있습니다..."):
        time.sleep(3)
    st.session_state["page"] = "results"
    st.rerun()

# 결과 화면 (필터 적용)
def show_results_page():
    st.title("📍 추천 매물 지도")

    if st.button("🔙 뒤로 가기", key="back_results"):
        st.session_state["page"] = "filters"
        st.rerun()

    filters = st.session_state.get("filters", {})

    # SQLAlchemy 쿼리 적용
    query = session.query(Building).join(Address, Building.address_id == Address.id)
    # tag 필터 
    tag_alias1 = aliased(Tag)
    tag_alias2 = aliased(Tag)
    tag_alias3 = aliased(Tag)
    
    if filters.get("병세권"):
        query = query.join(tag_alias1, Building.id == tag_alias1.building_id).filter(tag_alias1.label == "병원 가까움")
    if filters.get("역세권"):
        query = query.join(tag_alias2, Building.id == tag_alias2.building_id).filter(tag_alias2.label == "역세권")
    if filters.get("주세권"):
        query = query.join(tag_alias3, Building.id == tag_alias3.building_id).filter(tag_alias3.label == "주세권")
    
    # 신축여부 
    if filters.get("신축 여부"):
        from datetime import datetime
        current_year = datetime.now().year
        query = query.filter(Building.construction_year >= current_year - 5)

    # 건물 유형 필터
    if filters.get("건물 유형") and filters["건물 유형"] != "전체":
        query = query.filter(Building.purpose == filters["건물 유형"])

    # 몇 층 필터
    if filters.get("층") and filters["층"] != "전체":
        if filters["층"] == "1~5층 (저층)":
            query = query.filter(Building.floor.between(1, 5))
        elif filters["층"] == "6~8층 (중층)":
            query = query.filter(Building.floor.between(6, 8))
        elif filters["층"] == "9층 이상 (고층)":
            query = query.filter(Building.floor >= 9)

    # 건물 면적 필터
    if filters.get("건물 면적"):
        min_size, max_size = filters["건물 면적"]
        query = query.filter(Building.area_sqm.between(min_size * 3.3, max_size * 3.3))

    # 가격 필터 (RealestateDeal과 조인)
    if filters.get("가격 범위"):
        price_map = {
            "1억 이하": (0, 10000),
            "1~3억": (10000, 30000),
            "3~5억": (30000, 50000),
            "5~10억": (50000, 100000),
            "10억 이상": (100000, 99999999)
        }
        min_price, max_price = price_map[filters["가격 범위"]]
        query = query.join(RealestateDeal).filter(
            RealestateDeal.transaction_price_million.between(min_price, max_price)
        )

    buildings = query.limit(10).all()

    map = folium.Map(location=[37.5, 127.0], zoom_start=12)
    for building in buildings:
        folium.Marker(
            location=[building.address.latitude, building.address.longitude],
            popup=f"<b>{building.name}</b><br>💰 {building.area_sqm}㎡, {building.floor}층",
            icon=folium.Icon(color="blue")
        ).add_to(map)
    folium_static(map)

    st.subheader("🏡 추천 매물 Top 5")
    for building in buildings:
        st.markdown(f"**🏠 {building.name}**")
        st.write(f"💰 면적: {building.area_sqm}㎡")
        st.write(f"📍 위치: {building.address.district}, {building.address.legal_dong}")
        # st.image("https://source.unsplash.com/200x150/?house,apartment", use_column_width=True)

if "page" not in st.session_state:
    st.session_state["page"] = "filters"
if st.session_state["page"] == "filters":
    show_filter_page()
elif st.session_state["page"] == "loading":
    show_loading_page()
elif st.session_state["page"] == "results":
    show_results_page()