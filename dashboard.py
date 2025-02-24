import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from folium.plugins import MarkerCluster
from geopy.geocoders import Nominatim
from streamlit_folium import folium_static
import statsmodels.api as sm


# 데이터 로드
file_path1 = "./Data/refined-real-estate.csv"
file_path2 = "./Data/real-estate-prophet.csv"  
file_path3 = './Data/forecast_2025.csv'
df1 = pd.read_csv(file_path1)
df2 = pd.read_csv(file_path2)
df3 = pd.read_csv(file_path3, encoding='utf-8')

# # 거래일을 datetime 형식으로 변환
# df['거래일'] = pd.to_datetime(df['거래일'])

# Streamlit 페이지 설정
st.set_page_config(page_title="부동산 데이터 대시보드", layout="wide")

# 제목
st.title("🏡 부동산 데이터 대시보드")

# 탭 메뉴
tab1, tab2, tab3, tab4 = st.tabs(["📈 실거래가 시계열 분석", "🏙 거래가(물건금액) 분석", "🗺️ 거래량 Top30 지역", "🏢 층별 가격 분석"])

# **실거래가 시계열 분석**
with tab1:
    st.subheader("📈 거래가 시계열 분석")
    
    building_list = df2['지역+건물명+건물용도'].value_counts().head(30).index
    selected_building = st.selectbox("🔍 분석할 건물 선택", building_list)
    df_filtered = df2[df2['지역+건물명+건물용도'] == selected_building]
    fig = px.line(df_filtered, x='거래일', y='물건금액', title=f"{selected_building} 실거래가 변화 추이", markers=True)
    fig.update_layout(width=1200, height=600)
    st.plotly_chart(fig, use_container_width=True)

    # 예측 데이터 추가한 그래프
    df2 = df2[['거래일', '지역+건물명+건물용도', '물건금액']]
    df2['거래일'] = pd.to_datetime(df2['거래일']).dt.date
    df3 = df3[['거래일', '지역+건물명+건물용도', '물건금액(만원)']]
    df3['물건금액'] = df3['물건금액(만원)']*10000
    df3['거래일'] = pd.to_datetime(df3['거래일']).dt.date

    join_df = pd.concat([df2, df3], ignore_index=True, axis=0)
    df_filtered = join_df[join_df['지역+건물명+건물용도'] == selected_building].sort_values(by='거래일')
    fig9 = px.line(df_filtered, x='거래일', y='물건금액', title=f"{selected_building} 실거래가 변화 추이, 예측 데이터 추가", markers=True)
    fig9.update_layout(width=1200, height=600)
    st.plotly_chart(fig9, use_container_width=True)    


# **거래가(물건금액) 분석**
with tab2:
    st.subheader("🏙 거래 평균가 Top30 지역")
    
    df1['지역'] = df1['자치구명'] + ' ' + df1['법정동명']
    df1['물건금액'] = df1['물건금액(만원)'] * 10000
    df_price_avg = df1.groupby('지역')['물건금액'].mean().reset_index()
    df_price_avg.columns = ['지역', '평균 금액']
    df_top30_price = df_price_avg.sort_values(by='평균 금액', ascending=False).head(30)
    
    fig2 = px.bar(df_top30_price, x='지역', y='평균 금액', title='매물 평균가 상위 30개 지역', color='평균 금액')
    fig2.update_layout(width=1200, height=600, xaxis_tickangle=-45)
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("🏙 건물면적이 넓을수록 거래가가 높을까?")
    fig6 = px.scatter(df1, x='건물면적(㎡)', y='물건금액', trendline='ols', title='건물면적 vs 물건금액', opacity=0.6)
    fig6.update_layout(width=1200, height=600)
    st.plotly_chart(fig6, use_container_width=True)
    st.markdown("""
    #### ✅ 건물면적과 물건금액의 상관관계 분석
    - **상관계수**: `0.72` → 강한 양의 상관관계  
    - **p-value**: `0.00000` → 통계적으로 유의미한 결과
    """)

    st.subheader("🏙 오래된 건물이면 저렴할까?")
    df1['건축년도'] = df1.apply(lambda row: row['계약연도'] if row['건축년도'] == 0 else row['건축년도'], axis=1)
    fig7 = px.scatter(df1, x='건축년도', y='물건금액', trendline='ols', title='건축년도 vs 물건금액', opacity=0.6)
    fig7.update_layout(width=1200, height=600)
    st.plotly_chart(fig7, use_container_width=True)
    st.markdown("""
    #### ✅ 건축년도와 물건금액의 상관관계 분석
    - **상관계수**: `-0.11` → 건축년도가 오래될수록 가격이 낮아지는 경향  
    - **p-value**: `0.00000` → 통계적으로 유의미한 결과  
    """)

# 탭3: 거래량 top30
with tab3:
    st.subheader("🗺️ 지역별 거래량 Top 30")

    df1['지역'] = df1['자치구명'] + ' ' + df1['법정동명']
    df_grouped = df1['지역'].value_counts().reset_index()
    df_grouped.columns = ['지역', '거래량']
    df_top30 = df_grouped.head(30)
    
    # 막대 그래프 그리기
    fig4 = px.bar(df_top30, x='지역', y='거래량', title='지역별 거래량', color='거래량')
    fig4.update_layout(xaxis_tickangle=-45)
    fig4.update_layout(width=1200, height=600)
    st.plotly_chart(fig4, use_container_width=True)

    # 트리맵
    fig5 = px.treemap(df_top30, path=['지역'], values='거래량', title='지역별 거래 분포')
    fig5.update_layout(width=1200, height=600)
    st.plotly_chart(fig5, use_container_width=True)

    st.subheader("🗺️ Top 30지역의 건물별 거래량 집계")
    df_filtered = df1[df1['지역'].isin(df_top30['지역'])]
    df_building_count = df_filtered.groupby(['지역', '본번', '부번', '건물명', '위도', '경도']).size().reset_index(name='거래량')

    # 지도 생성 (중심 좌표 설정)
    center = [df_building_count["위도"].mean(), df_building_count["경도"].mean()]
    m = folium.Map(location=center, zoom_start=12)

    # 색상 지정 함수 (거래량에 따라 색상 변경)
    def get_color(value, max_value):
        colors = ['green', 'blue', 'purple', 'orange', 'red']  # 낮은 값 > 높은 값
        idx = int((value / max_value) * (len(colors) - 1))
        return colors[idx]

    max_count = df_building_count['거래량'].max()

    # 마커 클러스터 추가
    marker_cluster = MarkerCluster().add_to(m)

    for _, row in df_building_count.iterrows():
        folium.CircleMarker(
            location=[row["위도"], row["경도"]],
            radius=row["거래량"] / max_count * 15,  # 거래량 비례 크기
            color=get_color(row["거래량"], max_count),
            fill=True,
            fill_color=get_color(row["거래량"], max_count),
            fill_opacity=0.6,
            popup=f"건물명: {row['건물명']}<br>거래량: {row['거래량']}회",
        ).add_to(marker_cluster)

    # 지도 출력
    folium_static(m, width=1650, height=800)

# 탭 4: 층별 가격 분석**
with tab4:
    df2 = pd.read_csv(file_path2)
    st.subheader("🏢 층별 평균 거래 금액 분석")
    df_floor = df2.groupby('층')['물건금액'].mean().astype(int).reset_index()
    fig3 = px.bar(df_floor, x='층', y='물건금액', color='물건금액', title="층별 평균 거래 금액")
    fig3.update_layout(width=1200, height=600)
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("🏢 고층일수록 거래가가 높을까?")
    df1['물건금액'] = df1['물건금액(만원)'] * 10000
    fig8 = px.scatter(df1, x='층', y='물건금액', trendline='ols', title='층 vs 물건금액', opacity=0.6)
    fig8.update_layout(width=1200, height=600)
    st.plotly_chart(fig8, use_container_width=True)
    st.markdown("""
    #### ✅ 층과 물건금액의 상관관계 분석
    - **상관계수**: `0.34` → 층이 높을수록 가격이 오르는 경향  
    - **p-value**: `0.00000` → 통계적으로 유의미한 결과  
    """)

# # 실행 방법 안내
# st.markdown("🚀 **Streamlit 실행 방법:**")
# st.code("streamlit run app.py", language="bash")