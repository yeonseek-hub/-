import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from itertools import permutations
import math

# ---------------------------
# 관광지 데이터 (이모지 포함)
# ---------------------------
places = [
    {"이름": "경복궁", "위도": 37.579617, "경도": 126.977041, "설명": "조선의 정궁", "역": "경복궁역(3호선)", "이모지": "🏛️"},
    {"이름": "명동", "위도": 37.563757, "경도": 126.982682, "설명": "쇼핑과 먹거리 중심", "역": "명동역(4호선)", "이모지": "🛍️"},
    {"이름": "남산타워", "위도": 37.551169, "경도": 126.988227, "설명": "서울 전망 명소", "역": "충무로역(3,4호선)", "이모지": "🌉"},
    {"이름": "북촌한옥마을", "위도": 37.582604, "경도": 126.983998, "설명": "전통과 현대 공존", "역": "안국역(3호선)", "이모지": "🏘️"},
    {"이름": "홍대거리", "위도": 37.555226, "경도": 126.923943, "설명": "젊음과 예술 거리", "역": "홍대입구역(2호선)", "이모지": "🎨"},
    {"이름": "DDP", "위도": 37.566478, "경도": 127.009041, "설명": "미래적 건축과 전시 공간", "역": "동대문역사문화공원역(2,4,5호선)", "이모지": "🏢"},
    {"이름": "한강공원", "위도": 37.528708, "경도": 126.934889, "설명": "서울 시민 휴식 명소", "역": "여의나루역(5호선)", "이모지": "🌊"},
    {"이름": "인사동", "위도": 37.574009, "경도": 126.984913, "설명": "전통 문화 거리", "역": "종로3가역(1,3,5호선)", "이모지": "🎎"},
    {"이름": "롯데월드", "위도": 37.511000, "경도": 127.098000, "설명": "도심 테마파크", "역": "잠실역(2,8호선)", "이모지": "🎡"},
    {"이름": "잠실 롯데타워", "위도": 37.513068, "경도": 127.102538, "설명": "최고층 빌딩과 전망대", "역": "잠실역(2,8호선)", "이모지": "🏙️"}
]

df = pd.DataFrame(places)

# ---------------------------
# 페이지 설정
# ---------------------------
st.set_page_config(page_title="서울 관광 여행 플래너", layout="wide")
st.markdown("<h1 style='text-align:center;color:#e63946;'>🗺️ 서울 Top10 여행 플래너 ✈️</h1>", unsafe_allow_html=True)

# ---------------------------
# 지도 표시
# ---------------------------
seoul_map = folium.Map(location=[37.5665, 126.9780], zoom_start=12)
for _, row in df.iterrows():
    popup_html = f"<div style='white-space:nowrap;font-weight:bold'>{row['이모지']} {row['이름']} - {row['설명']} / {row['역']}</div>"
    folium.Marker(location=[row["위도"], row["경도"]],
                  popup=popup_html,
                  tooltip=row["이름"],
                  icon=folium.Icon(color="red", icon="info-sign")).add_to(seoul_map)

st.subheader("📍 서울 지도")
st_folium(seoul_map, width=490, height=350)

# ---------------------------
# 일정 생성 함수
# ---------------------------
def euclidean_distance(p1, p2):
    return math.sqrt((p1['위도'] - p2['위도'])**2 + (p1['경도'] - p2['경도'])**2)

def optimize_route(day_places):
    best_order = day_places
    min_dist = float('inf')
    for perm in permutations(day_places):
        dist = sum(euclidean_distance(perm[i], perm[i+1]) for i in range(len(perm)-1))
        if dist < min_dist:
            min_dist = dist
            best_order = perm
    return best_order

# ---------------------------
# 여행 일정 생성
# ---------------------------
st.subheader("🗓️ 여행 일정 만들기")
days = st.radio("여행 기간 선택:", [1,2,3], index=0, horizontal=True)

if st.button("최적 일정 생성"):
    num_days = int(days)
    per_day = len(df) // num_days
    extra = len(df) % num_days
    idx = 0
    schedule = []

    for d in range(1, num_days+1):
        day_places = df.iloc[idx:idx+per_day].to_dict('records')
        if extra > 0:
            day_places.append(df.iloc[idx+per_day].to_dict())
            extra -= 1
            idx += 1
        idx += per_day

        # 최적 순서
        day_places = optimize_route(day_places)
        schedule.append((d, day_places))

    # ---------------------------
    # 시간 배정 + 점심 포함 + 이모지 표시
    # ---------------------------
    st.markdown("### 📅 추천 일정 (오전/오후 + 점심 포함)")
    for day, day_places in schedule:
        st.markdown(f"#### Day {day}")
        for i, place in enumerate(day_places):
            if i == len(day_places)//2:
                st.markdown("🍽️ 12:00~13:00 점심")
            if i % 2 == 0:
                time = "☀️ 09:00~12:00 (오전)"
            else:
                time = "🌤️ 13:00~17:00 (오후)"
            st.markdown(f"{time} 🚶‍♂️ {place['이모지']} **{place['이름']}** ({place['설명']}, {place['역']})")
