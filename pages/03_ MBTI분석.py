import streamlit as st
import pandas as pd
import plotly.express as px

# ===== 데이터 불러오기 =====
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

# ===== 기본 설정 =====
st.set_page_config(page_title="세계 MBTI 비율 대시보드", page_icon="🌍", layout="wide")
st.title("🌍 세계 MBTI 비율 대시보드")

st.markdown("#### 국가를 선택하면 각 MBTI 유형의 비율을 확인할 수 있습니다.")

# ===== 데이터 로드 =====
df = load_data()

# ===== 사이드바 =====
st.sidebar.header("국가 선택")
selected_country = st.sidebar.selectbox("국가를 선택하세요", df['Country'].unique())

# ===== 선택한 국가 데이터 가공 =====
country_data = df[df['Country'] == selected_country].melt(id_vars='Country', var_name='MBTI', value_name='비율')
country_data = country_data.sort_values('비율', ascending=False)

# ===== 색상 설정 =====
top_type = country_data.iloc[0]['MBTI']
colors = ['#FF4C4C' if mbti == top_type else f'rgba(0, 123, 255, {0.4 + 0.6*(1 - i/len(country_data))})' for i, mbti in enumerate(country_data['MBTI'])]

# ===== 그래프 =====
fig = px.bar(
    country_data,
    x='MBTI',
    y='비율',
    text='비율',
    title=f"{selected_country}의 MBTI 비율",
)

fig.update_traces(
    texttemplate='%{text:.2%}',
    textposition='outside',
    marker_color=colors
)
fig.update_layout(
    yaxis_tickformat='.0%',
    template='plotly_white',
    xaxis_title='MBTI 유형',
    yaxis_title='비율',
    showlegend=False
)

# ===== 출력 =====
st.plotly_chart(fig, use_container_width=True)

# ===== 데이터 보기 =====
with st.expander("📄 원본 데이터 보기"):
    st.dataframe(df)
