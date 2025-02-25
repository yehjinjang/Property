## SeSAC Mini Project1

## 📌 Overview

이 프로젝트는 서울시 부동산 실거래가 정보와 공공 데이터를 활용하여, 사용자의 라이프스타일에 맞춘 서울의 최적의 거주지를 추천합니다.  
지도 기반 시각화를 제공하여, 직관적인 UI로 살기 좋은 동네를 확인할 수 있는 웹 서비스입니다.

## 📅 Period

2025.02.20 ~ 2025.02.26

## 👥 Team

|                                                 권다현                                                  |                                                 박병준                                                  |                                                 장예진                                                  |
| :-----------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------: |
| <img src="https://github.com/user-attachments/assets/517ac756-27a4-4df0-8307-bd87632eca74" width="180"> | <img src="https://github.com/user-attachments/assets/120e9b3a-ff8c-4c3e-a4f3-7745f470bbc8" width="180"> | <img src="https://github.com/user-attachments/assets/3540f397-6882-4572-a337-635db4621087" width="180"> |
|                    [@danidanicarrotcarrot](https://github.com/danidanicarrotcarrot)                     |                              [@AlpacaMale](https://github.com/AlpacaMale)                               |                              [@yehjinjang](https://github.com/yehjinjang)                               |

## 🛠️ Skills

- **Web Framework**: Streamlit
- **EDA**: JupyterNotebook, Pandas
- **Visualization**: Pyplot
- **DataBase**: MySQL, SQLAlchemy
- **Recommendation**: LangChain, GPT-3.5

## 🪄 Features

- 사용자에게 정보를 제공받아 LLM을 이용해 부동산을 추천합니다.
- 추천한 부동산의 이름, 연 평균 가격, 거래량, 거래내역, 면적, 위치를 제공합니다.
- 건물의 메타데이터와 건물 가격의 상관관계에 대한 EDA & 시각화를 제공합니다.

## 🚀 Installation & Execution

1. **Clone repository**

```bash
git clone https://github.com/yehjinjang/real-estate-mate
```

2. **Change directory**

```bash
cd real-estate-mate
```

3. **Install package dependency**

```bash
pip install -r requirements.txt
```

4. **Set up environment**

```.env
KAKAO_API_KEY='your-api-key'
DATABASE_URL='mysql+pymysql://user:passwd@host/realestate'
OPENAI_API_KEY="your-api-key"
```

5. **Create Database & Tables**

[View the sql script][1]

6. **Insert datas into database using jupyternotebooks**

   6-1. Execute database.ipynb
   6-2. tag.ipynb

7. **Run Streamlit**

```bash
streamlit run app.py
```

## 📂 Package Structure

```
📂 Data/                   # 데이터 파일 저장 디렉토리
📂 notebooks/              # Jupyter Notebook 저장 디렉토리
📂 pages/                  # Streamlit 페이지 디렉토리
📄 app.py                  # Streamlit 메인 애플리케이션 파일
📄 models.py               # ORM 모델 정의 파일
📄 requirements.txt        # 프로젝트 의존성 패키지 목록
📄 README.md               # 프로젝트 설명 문서
```

## Troubleshooting

- **병준**: ORM을 사용할 때 building의 tag를 가져오기 위해 tag의 building_id가 building.id인 모든 태그를 검색하는 방법을 사용해서 속도도 느리고 코드도 지저분 했었는데, ORM의 relation 기능을 이용해서 쿼리성능과 가독성을 개선했습니다. 또, 여러 조건을 이용해 쿼리할 때, 서브쿼리 exists를 이용해서 필요 없는 데이터 조회를 줄여서 쿼리의 속도를 높였습니다.

## 📊 데이터 출처

- **부동산 가격**: [서울시 부동산 실거래가 정보 (2022~2025)](https://www.data.go.kr/)
- **응급실 위치 데이터**: [공공 데이터](https://www.data.go.kr/data/15088910/fileData.do)
- **범죄율 데이터**: [공공 데이터](https://www.data.go.kr/data/3074462/fileData.do)
- **버스 정류장 좌표**: [서울 열린 데이터](https://data.seoul.go.kr/dataList/OA-15067/S/1/datasetView.do)
- **지하철 정류장 좌표**: [공공 데이터](https://www.data.go.kr/data/15099316/fileData.do?recommendDataYn=Y)

[1]: https://www.notion.so/Database-1a2d988766cd80778097d647fb276f16?pvs=4
