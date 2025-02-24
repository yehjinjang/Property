import streamlit as st
import time
import folium
from streamlit_folium import folium_static
import streamlit.components.v1 as components
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
import pandas as pd
import os
from datetime import datetime
import sys
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from dotenv import load_dotenv
from models import Building, Tag, RealestateDeal, Address

BUILDING_AGE_THRESHOLD = 5
load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"), echo=False)

Session = sessionmaker(bind=engine)
session = Session()


def get_price(price):
    if price == "1억 이하":
        return (0, 10000)
    elif price == "1~3억":
        return (10001, 30000)
    elif price == "3~5억":
        return (30001, 50000)
    elif price == "5~10억":
        return (50001, 100000)
    elif price == "10억 이상":
        return (100001, None)


def get_floor(floor):
    if floor == "전체":
        return None
    elif floor == "1~5층 (저층)":
        return (1, 5)
    elif floor == "6~8층 (중층)":
        return (6, 8)
    elif floor == "9층 이상 (고층)":
        return (9, None)

def toggle_filter(filter_key):
    st.session_state["filters"][filter_key] = not st.session_state["filters"][filter_key]
    
# 첫 enter filter page
def show_filter_page():
    st.title("🏡 REAL-ESTATE")
    st.subheader("권병진님, 원하는 집을 찾아드려요!")

    st.markdown("### 원하는 조건을 선택하세요")
    col1, col2 = st.columns(2)
    
    if "filters" not in st.session_state:
        st.session_state["filters"] = {
            "병세권": False,
            "역세권": False,
            "버세권": False,
            "신축 여부": False
        }

    with col1:
        st.markdown("#### 🏘️ 입지 조건")  
        
        # 체크박스에서 버튼으로 변경
        st.button(
            f"🏥 병세권 (응급실 가까이) {'✅' if st.session_state['filters']['병세권'] else ''}",
            on_click=toggle_filter,
            args=("병세권",)
        )
        st.button(
            f"🚇 역세권 (지하철역 가까이) {'✅' if st.session_state['filters']['역세권'] else ''}",
            on_click=toggle_filter,
            args=("역세권",)
        )
        st.button(
            f"🚏 버세권 (버스정류장 가까이) {'✅' if st.session_state['filters']['버세권'] else ''}",
            on_click=toggle_filter,
            args=("버세권",)
        )
        st.button(
            f"🏗️ 신축 여부 (최근 5년) {'✅' if st.session_state['filters']['신축 여부'] else ''}",
            on_click=toggle_filter,
            args=("신축 여부",)
        )

    with col2:
        st.markdown("#### 🏢 건물 정보")
        building_type = st.selectbox("건물 유형", ["전체", "아파트", "오피스텔", "연립다세대"])
        size = st.slider("건물 면적 (평)", 1, 100, (20, 80))
        price = st.selectbox("가격 범위", ["1억 이하", "1~3억", "3~5억", "5~10억", "10억 이상"])
        floor = st.selectbox("층 선택", ["전체", "1~5층 (저층)", "6~8층 (중층)", "9층 이상 (고층)"])
        
    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 5, 1])

    with col2:
        if st.button("추천 받기", use_container_width=True):
            st.session_state["filters"].update({
                "건물 유형": building_type,
                "건물 면적": size,
                "가격 범위": price,
                "층": floor,
            })
            st.session_state["page"] = "splash"
            st.rerun()
            
# for spalsh pages
ICON_MAP = {
    "병세권": "🏥",  
    "역세권": "🚇",  
    "버세권": "🚏",  
    "건물 유형": "🏢",
    "건물 면적": "📏", 
    "가격 범위": "💰",  
    "층": "🛗",  
}

# 확인 페이지 
def show_splash_page():
    if st.button("<", key="back_splash"):
        st.session_state["page"] = "filters"
        st.rerun()

    st.title("🔍 이런 매물을 원하시는군요!")

    filters = st.session_state.get("filters", {})
    selected_filters = {k: v for k, v in filters.items() if v}

    if selected_filters:
        st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
        for key, value in selected_filters.items():
            icon = ICON_MAP.get(key, "🏷️")
            
            if isinstance(value, bool):
                # bool 타입은 기존처럼 키 값만 출력
                display_text = f"{icon} {key}"
            elif key == "건물 유형":
                display_text = f"{icon} 건물 유형은 {value}"
            elif key == "가격 범위":
                display_text = f"{icon} 가격 범위는 {value}"
            elif key == "건물 면적" and isinstance(value, (list, tuple)) and len(value) == 2:
                display_text = f"{icon} 건물 면적은 {value[0]} ~ {value[1]} 평"
            elif key == "층":
                display_text = f"{icon} 층은 {value}"
            else:
                # 나머지 경우 기존 방식 그대로
                display_text = f"{icon} {key}: {value}"
            
            st.markdown(
                f'<p style="text-align: center; font-weight: bold; background-color: #000000; padding: 20px; border-radius: 10px;">{display_text}</p>', 
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("🔎 선택한 조건이 없습니다.")

    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        if st.button("확인", key="confirm_splash", use_container_width=True):
            st.session_state["loading"] = True
            st.session_state["page"] = "loading"
            st.rerun()

# loading pages
def show_loading_page():
    with st.spinner("🏡 추천 매물을 찾고 있습니다..."):
        search_building()
        get_recommend()
    st.session_state["page"] = "results"
    st.rerun()
    
# 결과 pages
def show_results_page():
    if st.button("홈으로", key="back_results"):
        st.session_state["page"] = "filters"
        st.rerun()
    st.title("📍 추천 매물 지도")
    
    recommendations = [
        {
            "이름": building.name,
            "가격": f"{sum(deal.transaction_price_million for deal in building.deals)
            // len(building.deals)
            // 10000}억",
            "면적": building.area_sqm,
            "위치": f"서울 {building.addresses.district}",
            "lat": building.addresses.latitude,
            "lon": building.addresses.longitude,
        }
        for building in session.query(Building)
        .filter(Building.id.in_(st.session_state["recommendations"]))
        .all()
    ]

    map = folium.Map(location=[37.5, 127.0], zoom_start=12)

    for rec in recommendations:
        folium.Marker(
            location=[rec["lat"], rec["lon"]],
            popup=f"<b>{rec['이름']}</b><br>💰 {rec['가격']}<br>📏 {rec['면적']}<br>📍 {rec['위치']}",
            icon=folium.Icon(color="blue"),
        ).add_to(map)

    folium_static(map)

    st.subheader("🏡 추천 매물 Top 5")
    container = st.container()
    if recommendations:
        with container:
            cols = st.columns(len(recommendations))
            for idx, rec in enumerate(recommendations):
                with cols[idx]:
                    st.write(f"### {rec['이름']}")
                    st.write(f"1. 가격: {rec['가격']}")
                    st.write(f"2. 면적: {rec['면적']}")
                    st.write(f"3. 위치: {rec['위치']}")
                    st.image(
                        "https://source.unsplash.com/200x150/?house,apartment",
                        use_container_width=True,
                    )


def search_building():
    latest_deal_subquery = (
        session.query(
            RealestateDeal.building_id,
            func.max(
                RealestateDeal.contract_year * 10000
                + RealestateDeal.contract_month * 100
                + RealestateDeal.contract_day
            ).label("max_date"),
        )
        .group_by(RealestateDeal.building_id)
        .subquery()
    )

    query = session.query(Building).join(RealestateDeal)

    query = query.join(
        latest_deal_subquery,
        (RealestateDeal.building_id == latest_deal_subquery.c.building_id)
        & (
            RealestateDeal.contract_year * 10000
            + RealestateDeal.contract_month * 100
            + RealestateDeal.contract_day
            == latest_deal_subquery.c.max_date
        ),
    )
    filters = st.session_state["filters"]
    new_building = filters.get("신축 여부")
    building_type = filters.get("건물 유형")
    tags = [
        tag
        for tag, boolean in zip(
            ["병세권", "역세권", "버세권"],
            [filters.get("병세권"), filters.get("역세권"), filters.get("버세권")],
        )
        if boolean
    ]
    size = [size * 3.3058 for size in filters.get("건물 면적")]
    price_range = get_price(filters.get("가격 범위"))
    floor = get_floor(filters.get("층"))

    if tags:
        for tag in tags:
            query = query.filter(
                session.query(Tag)
                .filter(Tag.building_id == Building.id, Tag.label == tag)
                .exists()
            )

    if new_building:
        query = query.filter(
            Building.construction_year > datetime.now().year - BUILDING_AGE_THRESHOLD
        )

    if building_type and building_type != "전체":
        query = query.filter(Building.purpose == building_type)

    query = query.filter(Building.area_sqm.between(size[0], size[1]))

    if price_range[1] is None:
        query = query.filter(RealestateDeal.transaction_price_million >= price_range[0])
    else:
        query = query.filter(
            RealestateDeal.transaction_price_million.between(
                price_range[0], price_range[1]
            )
        )

    query = query.group_by(Building.id)

    if floor:
        if floor[1] is None:
            query = query.filter(Building.floor >= floor[0])
        else:
            query = query.filter(Building.floor.between(floor[0], floor[1]))

    buildings = query.limit(50).all()
    st.session_state["buildings"] = buildings
    print(len(buildings))


def get_recommend():
    buildings = st.session_state["buildings"]
    data = [building.to_dict() for building in buildings]
    schemas = [
        ResponseSchema(
            name="ids", description="List of selected building IDs", type="list"
        )
    ]
    parser = StructuredOutputParser.from_response_schemas(schemas)
    template = PromptTemplate.from_template(
        "Here is the given dataset:\n{data}\n\n"
        "Select the 5 best entries and return only their IDs in a JSON list format.\n"
        'Example output: {{"ids": [14951, 14952, 14953, 14954, 14955]}}\n'
        f"Output format: {parser.get_format_instructions().replace('{', '{{').replace('}', '}}')}"
    )
    llm = ChatOpenAI(temperature=0)
    chain = template | llm | parser
    recommendations = chain.invoke({"data": data}).get("ids")
    st.session_state["recommendations"] = recommendations


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
