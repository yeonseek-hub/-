
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 페이지 설정
st.set_page_config(page_title="🚇 2025년 10월 지하철 승하차 분석", layout="wide")

# 제목
st.title("🚇 2025년 10월 지하철 승하차 분석")
st.write("날짜와 호선을 선택하면, 승·하차 총합 기준으로 역 순위를 시각화합니다.")

# 데이터 불러오기
df = pd.read_csv("jijonsik.csv", encoding="cp949")
df['사용일자'] = df['사용일자'].astype(str)

# 날짜 선택 (10월만)
october_dates = sorted(df[df['사용일자'].str.startswith("202510")]['사용일자'].unique())
selected_date = st.selectbox("📅 날짜를 선택하세요", october_dates)

# 호선 선택
selected_line = st.selectbox("🚈 호선을 선택하세요", sorted(df['노선명'].unique()))

# 필터링
filtered = df[(df['사용일자'] == selected_date) & (df['노선명'] == selected_line)].copy()

if filtered.empty:
    st.warning("선택한 날짜와 호선에 데이터가 없습니다.")
else:
    # 승·하차 합산
    filtered["총승객"] = filtered["승차총승객수"] + filtered["하차총승객수"]

    # 총승객 기준 내림차순 정렬
    filtered = filtered.sort_values("총승객", ascending=False).reset_index(drop=True)

    # 색상 설정: 1등 빨강, 나머지는 파란색 그라데이션
    n = len(filtered)
    colors = ["red"]
    if n > 1:
        blue_colors = px.colors.sequential.Blues  # Plotly 기본 블루 계열
        # n-1개에 맞춰 균등 분할
        indices = np.linspace(0, len(blue_colors)-1, n-1, dtype=int)
        colors += [blue_colors[i] for i in indices]

    # 그래프
    fig = px.bar(
        filtered,
        x="역명",
        y="총승객",
        title=f"📊 {selected_date} / {selected_line} 승하차 총합 순위",
        color_discrete_sequence=colors,
        text="총승객"  # 막대 위 숫자 표시
    )

    fig.update_layout(
        xaxis_title="역명",
        yaxis_title="승차+하차 총합",
        template="plotly_white",
        title_font=dict(size=24, family="Arial Black"),
        xaxis_tickangle=-45
    )

    st.plotly_chart(fig, use_container_width=True)

    # 상위 5개 역 테이블 표시
    st.subheader("🏆 상위 5개 역")
    st.table(filtered.head(5)[["역명", "승차총승객수", "하차총승객수", "총승객"]])

    st.write(f"🔍 총 {len(filtered)}개 역이 검색되었습니다.")
