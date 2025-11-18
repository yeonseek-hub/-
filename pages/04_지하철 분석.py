import streamlit as st
import pandas as pd
import plotly.express as px
import itertools

st.set_page_config(page_title="지하철 승하차 분석", layout="wide")

# 데이터 불러오기
df = pd.read_csv("jijonsik.csv", encoding="cp949")

st.title("🚇 2025년 10월 지하철 승하차 분석")
st.write("날짜와 호선을 선택하면, 승·하차 총합이 가장 많은 역을 순위별로 시각화합니다.")

# 날짜 필터 (10월만 선택)
df['사용일자'] = df['사용일자'].astype(str)
october_dates = sorted(df[df['사용일자'].str.startswith("202510")]['사용일자'].unique())

selected_date = st.selectbox("📅 날짜를 선택하세요", october_dates)

# 노선 필터
selected_line = st.selectbox("🚈 호선을 선택하세요", sorted(df['노선명'].unique()))

# 필터링
filtered = df[(df['사용일자'] == selected_date) & (df['노선명'] == selected_line)].copy()

if filtered.empty:
    st.warning("선택한 날짜와 호선에 데이터가 없습니다.")
else:
    # 합산 컬럼 추가
    filtered["총승객"] = filtered["승차총승객수"] + filtered["하차총승객수"]

    # 정렬
    filtered = filtered.sort_values("총승객", ascending=False)

    # 색상 설정 (1등 = 빨강, 나머지 = 파랑 계열 반복)
    base_colors = px.colors.sequential.Blues
    colors = ["red"] + list(itertools.islice(itertools.cycle(base_colors), len(filtered)-1))

    # 그래프
    fig = px.bar(
        filtered,
        x="역명",
        y="총승객",
        title=f"📊 {selected_date} / {selected_line} 승하차 총합 순위",
        color_discrete_sequence=colors
    )

    fig.update_layout(
        xaxis_title="역명",
        yaxis_title="승차+하차 총합",
        template="simple_white"
    )

    st.plotly_chart(fig, use_container_width=True)
    st.write(f"🔍 총 {len(filtered)}개 역이 검색되었습니다.")
