import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO

# Streamlit 페이지 설정
st.set_page_config(layout="wide", page_title="지역별 범죄 발생 현황")
st.title("🚨 지역별 범죄 발생 현황 분석 (2023년)")

# 1. 데이터 로드 및 전처리
@st.cache_data
def load_data(file_path):
    """CSV 파일을 로드하고 필요한 전처리를 수행합니다."""
    # 한글 인코딩 문제 방지를 위해 'cp949' 또는 'euc-kr' 시도
    try:
        df = pd.read_csv(file_path, encoding='cp949')
    except:
        try:
            df = pd.read_csv(file_path, encoding='euc-kr')
        except:
            # 기본 utf-8 시도 (사용자가 변환했을 수도 있음)
            df = pd.read_csv(file_path, encoding='utf-8')
    
    # '범죄대분류', '범죄중분류' 열을 제외한 나머지 열이 구 이름 열입니다.
    # 구 이름 열의 데이터 타입을 정수로 변환 시도 (범죄 발생 건수)
    col_to_convert = df.columns.drop(['범죄대분류', '범죄중분류'])
    df[col_to_convert] = df[col_to_convert].apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)
    
    return df

# 파일 경로 (루트 폴더에 있다고 가정)
FILE_PATH = "경찰청_범죄 발생 지역별 통계_20231231.csv"

try:
    data_df = load_data(FILE_PATH)
except FileNotFoundError:
    st.error(f"🚨 파일을 찾을 수 없습니다: **{FILE_PATH}**. 파일을 루트 폴더에 업로드했는지 확인해주세요.")
    st.stop()
except Exception as e:
    st.error(f"데이터 로드 및 처리 중 오류가 발생했습니다: {e}")
    st.stop()

# 구 이름 목록 추출 (서울/부산/대구 등 시/도 정보 제거)
all_districts = data_df.columns.drop(['범죄대분류', '범죄중분류']).tolist()

# '서울', '부산' 등 시/도 이름이 포함된 구 이름에서 시/도 제거하여 고유 구 이름 목록 생성
# 예: '서울종로구' -> '종로구'
district_names = [col.replace('서울', '').replace('부산', '').replace('대구', '').replace('인천', '').replace('광주', '').replace('대전', '').replace('울산', '').replace('세종', '').replace('경기', '').replace('강원', '').replace('충북', '').replace('충남', '').replace('전북', '').replace('전남', '').replace('경북', '').replace('경남', '').replace('제주', '') for col in all_districts]
# 다시 시/도 정보를 붙여 원래 이름을 유지하며 선택 목록 생성
display_names = all_districts
district_mapping = dict(zip(display_names, all_districts))

# 2. 사이드바 설정 (사용자 입력)
st.sidebar.header("🗺️ 지역 선택")

# 구 이름 선택 드롭다운
selected_display_name = st.sidebar.selectbox(
    "범죄 현황을 분석할 지역(구)을 선택하세요.",
    options=display_names
)

# 실제 데이터프레임 컬럼 이름 가져오기
selected_district = district_mapping.get(selected_display_name)

# 3. 데이터 분석 및 시각화
if selected_district:
    
    st.subheader(f"선택 지역: **{selected_display_name}**")
    
    # 선택된 지역의 범죄 데이터 추출 및 집계
    # 범죄 중분류를 기준으로 선택된 구의 범죄 발생 건수를 집계합니다.
    crime_data = data_df[['범죄중분류', selected_district]].copy()
    
    # 같은 '범죄중분류'를 가진 행들을 합산 (예: 폭행-가정폭력, 폭행-일반폭행 등을 '폭행'으로 합칠 필요가 있다면)
    # 현재 데이터셋은 중분류가 충분히 상세하므로, 중분류 기준으로 그룹화합니다.
    grouped_crime = crime_data.groupby('범죄중분류').sum().reset_index()
    
    # 발생 건수를 기준으로 내림차순 정렬
    sorted_crime = grouped_crime.sort_values(by=selected_district, ascending=False)
    
    # 총 범죄 발생 건수 계산
    total_crime_count = sorted_crime[selected_district].sum()
    
    # 요약 정보 표시
    st.info(f"선택된 지역 **{selected_display_name}**의 **총 범죄 발생 건수** (2023년): **{total_crime_count:,} 건**")

    # 4. 막대 그래프 생성 (가장 많이 발생한 범죄 유형 TOP N)
    
    # TOP N 설정
    top_n = st.sidebar.slider("표시할 범죄 유형 개수 (TOP N)", 5, len(sorted_crime), 10)
    
    top_n_crime = sorted_crime.head(top_n)

    if not top_n_crime.empty:
        # Plotly를 사용하여 막대 그래프 생성
        fig = px.bar(
            top_n_crime,
            x=selected_district,
            y='범죄중분류',
            orientation='h',  # 수평 막대 그래프
            title=f"**{selected_display_name}** - 범죄 발생 건수 Top {top_n} (범죄중분류 기준)",
            labels={selected_district: '발생 건수 (건)', '범죄중분류': '범죄 유형'},
            color=selected_district, # 건수에 따라 색상 변화
            color_continuous_scale=px.colors.sequential.Sunset,
        )
        
        # 레이아웃 조정
        fig.update_layout(
            yaxis={'categoryorder': 'total ascending'}, # Y축 순서를 건수에 따라 정렬
            margin=dict(l=20, r=20, t=50, b=20),
            height=600
        )
        
        # 그래프 출력
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.subheader("📊 원본 데이터 테이블 (TOP N)")
        st.dataframe(top_n_crime, use_container_width=True)
    else:
        st.warning("선택하신 지역에 대한 범죄 데이터가 없거나 0건입니다.")

# 5. 데이터 출처 및 정보
st.sidebar.markdown("---")
st.sidebar.caption("데이터 출처: 경찰청 (2023년 범죄 발생 지역별 통계)")
st.sidebar.caption("개발: Gemini AI")

# --- Streamlit 코드 끝 ---
