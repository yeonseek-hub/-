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
    encodings = ['cp949', 'euc-kr', 'utf-8']
    df = None
    for encoding in encodings:
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            break
        except:
            continue
    
    if df is None:
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


# --- 2. 사이드바 설정 (사용자 입력: 구 이름 선택) ---

st.sidebar.header("🗺️ 지역 선택")

# **핵심: 구 이름 선택 드롭다운**
selected_district = st.sidebar.selectbox(
    "범죄 현황을 분석할 **구 이름**을 선택하세요.",
    options=all_districts
)

# TOP N 설정 슬라이더
top_n = st.sidebar.slider("표시할 범죄 유형 개수 (TOP N)", 5, 20, 10)


# --- 3. 데이터 분석 및 시각화 (기본 막대 그래프) ---

if selected_district:
    
    st.subheader(f"📍 선택 지역: **{selected_district}**")
    
    # 선택된 지역의 범죄 데이터 추출 및 집계
    crime_data = data_df[['범죄중분류', '범죄대분류', selected_district]].copy()
    grouped_crime = crime_data.groupby('범죄중분류')[selected_district].sum().reset_index()
    sorted_crime = grouped_crime.sort_values(by=selected_district, ascending=False)
    
    total_crime_count = sorted_crime[selected_district].sum()
    st.metric(label="총 범죄 발생 건수 (2023년)", value=f"{total_crime_count:,} 건")

    top_n_crime = sorted_crime.head(top_n)

    if not top_n_crime.empty:
        # Plotly 막대 그래프 생성
        fig = px.bar(
            top_n_crime,
            x=selected_district,
            y='범죄중분류',
            orientation='h',
            title=f"**{selected_district}** - 범죄 발생 건수 Top {top_n} 유형 (클릭 대신 선택 기능)",
            labels={selected_district: '발생 건수 (건)', '범죄중분류': '범죄 유형'},
            color=selected_district, 
            color_continuous_scale=px.colors.sequential.Plotly3,
        )
        
        fig.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            margin=dict(l=20, r=20, t=50, b=20),
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.warning("선택하신 지역에 대한 범죄 데이터가 없거나 0건입니다.")


# --- 4. 심층 분석 (Drill-Down) 기능 구현 ---

if not top_n_crime.empty:
    st.markdown("---")
    st.subheader("🔍 선택한 범죄 유형의 **대분류 기준** 세부 분석")
    st.markdown("Top N 그래프에 표시된 범죄 유형 중 하나를 선택하면, 그 범죄가 속한 **대분류**의 모든 세부 유형(중분류)을 분석합니다.")

    # 1. 사용자가 Top N에 포함된 범죄 유형을 선택
    selected_sub_crime = st.selectbox(
        "세부 분석을 원하는 범죄 유형 (중분류)을 선택하세요.",
        options=top_n_crime['범죄중분류'].tolist(),
        index=0 # 기본값으로 가장 많이 발생한 범죄 선택
    )

    # 2. 선택된 '범죄중분류'가 속한 '범죄대분류' 찾기
    # data_df에서 해당 '범죄중분류'의 '범죄대분류'를 찾습니다.
    major_category_row = data_df[data_df['범죄중분류'] == selected_sub_crime].head(1)
    if not major_category_row.empty:
        major_category = major_category_row['범죄대분류'].iloc[0]
        
        st.info(f"선택 유형 '**{selected_sub_crime}**'는 **'{major_category}'**에 속하며, 같은 대분류의 다른 세부 유형을 확인합니다.")

        # 3. 해당 '범죄대분류'에 속하는 모든 '범죄중분류' 데이터를 필터링 및 집계
        detail_data = data_df[data_df['범죄대분류'] == major_category].copy()
        detail_grouped = detail_data.groupby('범죄중분류')[selected_district].sum().reset_index()
        detail_grouped = detail_grouped.sort_values(by=selected_district, ascending=False)
        
        st.subheader(f"'{major_category}' 대분류의 모든 세부 유형 ({selected_district})")
        
        # 4. 결과 데이터프레임 표시
        st.dataframe(
            detail_grouped, 
            column_order=['범죄중분류', selected_district],
            hide_index=True,
            use_container_width=True
        )
        
        # 5. 세부 막대 그래프 표시
        fig_detail = px.bar(
            detail_grouped,
            x=selected_district,
            y='범죄중분류',
            orientation='h',
            title=f"'{major_category}' 대분류 내 중분류별 건수 비교",
            labels={selected_district: '발생 건수 (건)', '범죄중분류': '범죄 유형'},
            color=selected_district, 
            color_continuous_scale=px.colors.sequential.Agsunset,
        )
        
        fig_detail.update_layout(yaxis={'categoryorder': 'total ascending'}, height=max(400, len(detail_grouped) * 35))
        st.plotly_chart(fig_detail, use_container_width=True)


# --- 5. 데이터 출처 및 정보 ---
st.sidebar.markdown("---")
st.sidebar.caption("데이터 출처: 경찰청 (2023년 범죄 발생 지역별 통계)")
st.sidebar.caption("개발: Gemini AI")
