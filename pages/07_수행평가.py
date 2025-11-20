
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. Streamlit 페이지 설정 및 데이터 로드 ---

st.set_page_config(layout="wide", page_title="🕵️ 범죄 발생 현황 심층 분석 대시보드")
st.title("🚨 2023년 지역별 범죄 발생 심층 분석 🗺️")
st.caption("👈 분석을 시작하려면 왼쪽 사이드바에서 설정을 확인해주세요!")

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

# 구 이름 목록 추출
all_districts = data_df.columns.drop(['범죄대분류', '범죄중분류']).tolist()


# --- 2. 사이드바 설정 (사용자 입력) ---

with st.sidebar:
    st.header("⚙️ 분석 설정")
    
    # 1. 구 이름 선택 (Selectbox/Dropdown)
    selected_district = st.selectbox(
        "1️⃣ 분석할 **구 이름**을 선택하세요.",
        options=all_districts
    )

    # 2. TOP N 개수 선택 (버튼 형식 - st.radio 사용)
    st.subheader("2️⃣ 표시할 범죄 유형 개수 (TOP N)")
    top_n = st.radio(
        "선택",
        options=[5, 10, 15, 20],
        index=1, # 기본값 10
        horizontal=True
    )
    
    top_n = int(top_n) 
    
    st.markdown("---")
    st.caption("데이터 출처: 경찰청 (2023년 범죄 발생 지역별 통계)")


# --- 3. 데이터 분석 및 시각화 (선택 구역의 Top N) ---

if selected_district:
    
    st.header(f"✨ {selected_district} 분석 결과")
    
    # 총 범죄 건수 및 Top N 계산
    crime_data = data_df[['범죄중분류', '범죄대분류', selected_district]].copy()
    grouped_crime = crime_data.groupby('범죄중분류')[selected_district].sum().reset_index()
    sorted_crime = grouped_crime.sort_values(by=selected_district, ascending=False)
    total_crime_count = sorted_crime[selected_district].sum()
    top_n_crime = sorted_crime.head(top_n)

    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("총 발생 건수 🔢")
        st.metric(label=f"**{selected_district}** 총 범죄 건수 (2023년)", value=f"{total_crime_count:,} 건", delta="연간 합계")

    with col2:
        # Plotly 막대 그래프 생성 (Top N)
        if not top_n_crime.empty:
            fig_topn = px.bar(
                top_n_crime,
                x=selected_district,
                y='범죄중분류',
                orientation='h',
                title=f"🥇 **{selected_district}** 범죄 발생 건수 Top {top_n} 유형",
                labels={selected_district: '발생 건수 (건)', '범죄중분류': '범죄 유형'},
                color=selected_district, 
                color_continuous_scale=px.colors.sequential.Plotly3,
            )
            fig_topn.update_layout(yaxis={'categoryorder': 'total ascending'}, height=450)
            st.plotly_chart(fig_topn, use_container_width=True)
        else:
            st.warning("선택하신 지역에 대한 데이터가 부족합니다.")

st.markdown("---")

# --- 4. 추가 기능 1: 지역별 총 범죄 건수 비교 랭킹 (수정됨) ---

st.header("📈 지역별 범죄 발생량 비교 랭킹")

# 1. 지역별 총 범죄 건수 계산
total_crime_by_district = data_df[all_districts].sum().reset_index()
total_crime_by_district.columns = ['지역', '총_범죄_건수']
total_crime_by_district = total_crime_by_district.sort_values(by='총_범죄_건수', ascending=False).reset_index(drop=True)
total_crime_by_district['순위'] = total_crime_by_district.index + 1

# 2. 선택 지역의 순위 찾기
selected_rank = total_crime_by_district[total_crime_by_district['지역'] == selected_district]['순위'].iloc[0]

st.info(f"선택하신 **{selected_district}**의 총 범죄 발생 건수는 전체 지역 중 **{selected_rank}위** 입니다.")

# 3. 랭킹 시각화: 슬라이더 기본값을 10으로 설정
comparison_n = st.slider(
    "비교하여 보여줄 지역 개수", 
    min_value=10, # 최소값을 10으로 고정
    max_value=len(all_districts), 
    value=10, # 기본값을 10으로 설정
    step=5
)

fig_rank = px.bar(
    total_crime_by_district.head(comparison_n),
    x='총_범죄_건수',
    y='지역',
    orientation='h',
    title=f"전국 지역별 총 범죄 건수 Top {comparison_n} 순위",
    color='지역',
    color_discrete_map={selected_district: 'red'}, # 선택한 지역 강조
    labels={'총_범죄_건수': '총 범죄 건수 (건)', '지역': '지역'},
)
fig_rank.update_layout(yaxis={'categoryorder': 'total ascending'}, height=max(500, comparison_n * 30))
st.plotly_chart(fig_rank, use_container_width=True)

st.markdown("---")

# --- 5. 심층 분석: 탭을 이용한 세부 비교 기능 ---

st.header("🔎 범죄 유형별 심층 분석")
st.markdown("Top N 그래프에 표시된 범죄 유형 중 하나를 선택하여 **대분류 내 비교**를 하거나, **다른 지역과 직접 비교**할 수 있습니다.")

tabs = st.tabs(["📊 대분류 내 세부 비교", "🌎 유형별 지역 비교"])

with tabs[0]: # 📊 대분류 내 세부 비교
    
    st.subheader("1️⃣ 대분류 내 중분류별 건수 비교")
    
    selected_sub_crime = st.selectbox(
        "세부 분석을 원하는 범죄 유형 (중분류)을 선택하세요.",
        options=top_n_crime['범죄중분류'].tolist(),
        index=0 
    )

    if selected_sub_crime:
        major_category_row = data_df[data_df['범죄중분류'] == selected_sub_crime].head(1)
        if not major_category_row.empty:
            major_category = major_category_row['범죄대분류'].iloc[0]
            
            st.info(f"선택 유형 '**{selected_sub_crime}**'는 **'{major_category}'**에 속합니다.")

            detail_data = data_df[data_df['범죄대분류'] == major_category].copy()
            detail_grouped = detail_data.groupby('범죄중분류')[selected_district].sum().reset_index()
            detail_grouped = detail_grouped.sort_values(by=selected_district, ascending=False)
            
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


with tabs[1]: # 🌎 유형별 지역 비교
    
    st.subheader("2️⃣ 특정 범죄 유형의 지역별 비교")

    all_crime_types = data_df['범죄중분류'].unique()

    compare_crime = st.selectbox(
        "비교할 **범죄 유형 (중분류)**을 선택하세요.",
        options=all_crime_types,
        index=0 
    )

    if compare_crime:
        compare_data_row = data_df[data_df['범죄중분류'] == compare_crime].copy()
        
        compare_df = compare_data_row[all_districts].T.sum(axis=1).reset_index()
        compare_df.columns = ['지역', '발생_건수']
        compare_df = compare_df.sort_values(by='발생_건수', ascending=False)

        # Top 20만 표시
        fig_comp = px.bar(
            compare_df.head(20), 
            x='발생_건수',
            y='지역',
            orientation='h',
            title=f"**{compare_crime}** 발생 건수 지역별 비교 (Top 20)",
            color='지역',
            color_discrete_map={selected_district: '#0077b6'}, 
            labels={'발생_건수': '발생 건수 (건)', '지역': '지역'},
        )
        fig_comp.update_layout(yaxis={'categoryorder': 'total ascending'}, height=600)
        st.plotly_chart(fig_comp, use_container_width=True)
