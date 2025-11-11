import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터: 외국인이 좋아하는 서울 주요 관광지 TOP10
places = {
    "관광지": [
        "경복궁", "명동", "남산타워(N서울타워)", "북촌한옥마을", "홍대거리",
        "동대문디자인플라자(DDP)", "한강공원", "인사동", "롯데월드", "잠실 롯데타워"
    ],
    "인기도 점수": [98, 96, 94, 92, 90, 88, 86, 84, 82, 80],
    "음계": ["도", "레", "미", "파", "솔", "라", "시", "도", "레", "미"]
}

df = pd.DataFrame(places)

# 제목
st.title("🎵 외국인이 사랑한 서울 관광지 Top10 (Polyphonic Style)")

# 표 표시
st.dataframe(df, use_container_width=True)

# 폴리음 느낌의 시각화 (Plotly로 멜로디 높이처럼)
fig = px.bar(
    df,
    x="관광지",
    y="인기도 점수",
    color="음계",
    text="음계",
    color_discrete_sequence=px.colors.qualitative.Pastel,
    title="서울 관광지의 '음'으로 표현한 인기"
)
fig.update_traces(textposition="outside")
st.plotly_chart(fig, use_container_width=True)

# 추가 설명
st.markdown("""
### 🎶 폴리음(Polyphonic) 효과란?
- 여러 소리가 동시에 울리는 음악적 조화를 뜻합니다.  
- 여기선 각 관광지를 하나의 ‘음’으로 표현해 서울이 만들어내는 조화로운 소리를 시각화했습니다.
""")
