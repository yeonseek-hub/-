import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. Streamlit 페이지 설정 및 데이터 로드 ---

st.set_page_config(layout="wide", page_title="지역별 범죄 발생 현황")
st.title("🚨 지역별 범죄 발생 현황 분석 (2023년)")
st.caption("👈 왼쪽 사이드바에서 분석할 지역(구)을 선택해주세요.")

# 데이터 로드 함수 (Streamlit 캐싱 적용)
@st.cache_data
def load_data(file_path):
    """CSV 파일을 로드하고 필요한 전처리를 수행합니다."""
    # 다양한 한글 인코딩 시도 (Streamlit Cloud 환경에서 인코딩 문제 방지)
    encodings = ['cp949', 'euc-kr', 'utf-8']
    for encoding in encodings:
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            break
        except:
            continue
    else:
        raise Exception("파일을 로드할 수 없습니다. 인코딩을 확인해주세요.")

    # '범죄대분류', '범죄중분류' 열을 제외한 나머지가 구 이름 열입니다.
    # 범죄 발생 건수 열을 정수로 변환 (NaN은 0으로 처리)
    col_to_convert = df.columns.drop(['범죄대분류', '범죄중분류'])
    df[col_to_convert] = df[col_to_convert].apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)
    
    return df

# 파일 경로 및 데이터 로드
FILE_PATH = "경찰청_범죄 발생 지역별 통계_20231231.csv"

try:
    data_df = load_data(FILE_PATH)
except FileNotFoundError:
    st.error(f"🚨 파일을 찾을 수 없습니다: **{FILE_PATH}**. 파일을 루트 폴더에 업로드했는지 확인해주세요.")
    st.stop()
except Exception as e:
    st.error(f"데이터 로드 및 처리 중 오류가 발생했습니다: {e}")
    st.stop()

# 구 이름 목록 추출 및 정리
all_districts = data_df.columns.drop(['범죄대분류', '범죄중분류']).tolist()
# '서울', '부산' 등 시/도 이름이 붙어있는 경우를 고려하여, 선택 시 표시될 이름과 실제 컬럼 이름을 매핑합니다.
district_mapping = {col: col for col in all_districts}


# --- 2. 사이드바 설정 (사용자 입력: 구 이름 선택) ---

st.sidebar.header("🗺️ 지역 선택")

# 구 이름 선택 드롭다운
# 사용자가 구 이름을 선택하는 부분입니다.
selected_district = st.sidebar.selectbox(
    "범죄 현황을 분석할 **구 이름**을 선택하세요.",
    options=all_districts
)

# TOP N 설정 슬라이더
top_n = st.sidebar.slider("표시할 범죄 유형 개수 (TOP N)", 5, 20, 10)


# --- 3. 데이터 분석 및 시각화 ---

if selected_district:
    
    st.subheader(f"📍 선택 지역: **{selected_district}**")
    
    # 선택된 지역의 범죄 데이터 추출 및 집계
    crime_data = data_df[['범죄중분류', selected_district]].copy()
    
    # '범죄중분류'별로 발생 건수 합산
    grouped_crime = crime_data.groupby('범죄중분류').sum().reset_index()
    
    # 발생 건수를 기준으로 내림차순 정렬
    sorted_crime = grouped_crime.sort_values(by=selected_district, ascending=False)
    
    # 총 범죄 발생 건수 계산
    total_crime_count = sorted_crime[selected_district].sum()
    
    # 요약 정보 표시
    st.metric(label="총 범죄 발생 건수 (2023년)", value=f"{total_crime_count:,} 건")

    # 상위 N개 범죄 유형 선택
    top_n_crime = sorted_crime.head(top_n)

    # 4. 막대 그래프 생성
    if not top_n_crime.empty:
        
        # Plotly를 사용하여 막대 그래프 생성
        fig = px.bar(
            top_n_crime,
            x=selected_district,
            y='범죄중분류',
            orientation='h',  # 수평 막대 그래프
            title=f"**{selected_district}** - 범죄 발생 건수 Top {top_n} 유형",
            labels={selected_district: '발생 건수 (건)', '범죄중분류': '범죄 유형'},
            color=selected_district, 
            color_continuous_scale=px.colors.sequential.Plotly3,
        )
        
        # 그래프 레이아웃 및 정렬 설정
        fig.update_layout(
            yaxis={'categoryorder': 'total ascending'}, # 건수가 많은 순으로 Y축 정렬
            margin=dict(l=20, r=20, t=50, b=20),
            height=600
        )
        
        # 그래프 출력
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.subheader(f"데이터 테이블 (Top {top_n})")
        st.dataframe(top_n_crime, use_container_width=True)
    else:
        st.warning("선택하신 지역에 대한 범죄 데이터가 없거나 0건입니다.")

# --- 5. 데이터 출처 및 정보 ---
st.sidebar.markdown("---")
st.sidebar.caption("데이터 출처: 경찰청 (2023년 범죄 발생 지역별 통계)")
st.sidebar.caption("개발: Gemini AI")
