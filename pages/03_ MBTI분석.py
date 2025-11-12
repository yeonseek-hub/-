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
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 예시 데이터 (사용자 데이터로 교체 가능)
data = {
    'Country': ['South Korea', 'USA', 'Japan', 'Germany', 'France', 'UK', 'Canada', 'Brazil', 'India', 'Australia', 'Italy'],
    'INTJ': [8, 6, 7, 5, 6, 7, 6, 5, 4, 6, 5],
    'ENFP': [10, 12, 9, 8, 9, 10, 11, 7, 6, 9, 8],
    'ISTP': [7, 5, 8, 6, 7, 6, 5, 4, 6, 5, 7],
    'INFJ': [9, 8, 7, 6, 5, 6, 7, 5, 4, 5, 6],
}
df = pd.DataFrame(data)

st.title("🌍 MBTI 세계 비교 대시보드")

tab1, tab2 = st.tabs(["국가별 MBTI 비율", "MBTI별 국가 순위"])

# ------------------------------
# 📊 탭 1: 국가별 MBTI 비율
# ------------------------------
with tab1:
    st.subheader("국가별 MBTI 비율 비교")

    country = st.selectbox("국가를 선택하세요:", df['Country'].unique())

    # 해당 국가 데이터 추출
    row = df[df['Country'] == country].iloc[0]
    mbti_values = row[1:]
    mbti_df = pd.DataFrame({
        'MBTI': mbti_values.index,
        'Value': mbti_values.values
    }).sort_values('Value', ascending=False)

    # 색상 설정 (1등은 빨강, 나머지는 파랑 그라데이션 역방향)
    colors = ['red'] + px.colors.sequential.Blues[::-1][:len(mbti_df)-1]

    fig = px.bar(
        mbti_df,
        x='MBTI',
        y='Value',
        text='Value',
        color=mbti_df['MBTI'],
        color_discrete_sequence=colors
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(
        showlegend=False,
        yaxis_title="비율(%)",
        xaxis_title="MBTI 유형",
        title=f"{country}의 MBTI 비율",
    )

    st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# 📊 탭 2: MBTI별 국가 순위
# ------------------------------
with tab2:
    st.subheader("MBTI별 국가 비율 상위 10개")

    mbti_type = st.selectbox("MBTI 유형을 선택하세요:", df.columns[1:])

    sorted_df = df.sort_values(by=mbti_type, ascending=False)
    top10 = sorted_df.head(10)

    # South Korea 포함 확인
    if 'South Korea' not in top10['Country'].values:
        sk_row = df[df['Country'] == 'South Korea']
        top10 = pd.concat([top10, sk_row])

    # 색상 설정
    colors = []
    for country in top10['Country']:
        if country == 'South Korea':
            colors.append('rgb(180, 60, 180)')  # 보라톤 (빨+파 믹스)
        else:
            colors.append('rgb(0, 100, 255)')

    fig2 = px.bar(
        top10,
        x='Country',
        y=mbti_type,
        text=mbti_type,
        color='Country',
        color_discrete_sequence=colors
    )

    fig2.update_traces(textposition='outside')
    fig2.update_layout(
        showlegend=False,
        yaxis_title="비율(%)",
        xaxis_title="국가",
        title=f"{mbti_type} 유형 비율이 높은 국가 Top 10",
    )

    st.plotly_chart(fig2, use_container_width=True)
    import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------
# 🌏 MBTI 예시 데이터 생성
# ------------------------------

countries = [
    "Afghanistan","Albania","Algeria","Andorra","Angola","Antigua and Barbuda",
    "Argentina","Armenia","Australia","Austria","Azerbaijan","Bahamas","Bahrain",
    "Bangladesh","Barbados","Belarus","Belgium","Belize","Bhutan",
    "Bosnia and Herzegovina","Botswana","Brazil","Brunei","Bulgaria","Burkina Faso",
    "Cambodia","Cameroon","Canada","Chile","China","Colombia","Congo","Costa Rica",
    "Croatia","Cuba","Cyprus","Czech Republic","Congo (Kinshasa)","Denmark","Djibouti",
    "Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Estonia","Ethiopia",
    "Faroe Islands","Fiji","Finland","France","Georgia","Germany","Ghana","Greece",
    "Grenada","Guatemala","Guinea","Guyana","Haiti","Honduras","Hungary","Iceland",
    "India","Indonesia","Iraq","Ireland","Israel","Italy","Jamaica","Japan","Jordan",
    "Kazakhstan","Kenya","Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho",
    "Libya","Lithuania","Luxembourg","Madagascar","Malawi","Malaysia","Maldives","Mali",
    "Malta","Mauritius","Mexico","Monaco","Mongolia","Montenegro","Morocco","Mozambique",
    "Myanmar","Namibia","Nepal","Netherlands","New Zealand","Nicaragua","Niger","Nigeria",
    "Macedonia","Norway","Oman","Pakistan","Panama","Papua New Guinea","Paraguay","Peru",
    "Philippines","Poland","Portugal","Qatar","South Korea","Moldova","Romania","Russia",
    "Rwanda","Saint Kitts and Nevis","Saint Lucia","Saint Vincent and the Grenadines",
    "Saudi Arabia","Senegal","Serbia","Seychelles","Singapore","Slovakia","Slovenia",
    "Somalia","South Africa","Spain","Sri Lanka","Sudan","Suriname","Sweden","Switzerland",
    "Syria","Tajikistan","Thailand","Trinidad and Tobago","Tunisia","Turkey","Uganda",
    "Ukraine","United Arab Emirates","United Kingdom","Tanzania","United States","Uruguay",
    "Uzbekistan","Vanuatu","Vietnam","Yemen","Zambia","Zimbabwe"
]

# MBTI 유형 예시
mbti_types = ['INTJ','ENFP','ISTP','INFJ','ENTP','ISFJ','ESTJ','ESFP','ISTJ','INFP','ENFJ','ISFP','ESTP','ENTJ','ESFJ','INTP']

# 임의 데이터 생성 (실제 데이터로 교체 가능)
import numpy as np
np.random.seed(42)
data = {'Country': countries}
for mbti in mbti_types:
    data[mbti] = np.random.randint(1, 20, size=len(countries))

df = pd.DataFrame(data)

# ------------------------------
# 🌍 Streamlit 대시보드
# ------------------------------
st.title("🌍 MBTI 세계 비교 대시보드")

tab1, tab2 = st.tabs(["국가별 MBTI 비율", "MBTI별 국가 순위"])

# ------------------------------
# 📊 탭 1: 국가별 MBTI 비율
# ------------------------------
with tab1:
    st.subheader("국가별 MBTI 비율 비교")

    country = st.selectbox("국가를 선택하세요:", df['Country'].unique())
    row = df[df['Country'] == country].iloc[0]
    mbti_values = row[1:]
    mbti_df = pd.DataFrame({
        'MBTI': mbti_values.index,
        'Value': mbti_values.values
    }).sort_values('Value', ascending=False)

    # 색상 설정 (1등 빨강, 나머지 파랑 그라데이션 역방향)
    colors = ['red'] + px.colors.sequential.Blues[::-1][:len(mbti_df)-1]

    fig = px.bar(
        mbti_df,
        x='MBTI',
        y='Value',
        text='Value',
        color=mbti_df['MBTI'],
        color_discrete_sequence=colors
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(
        showlegend=False,
        yaxis_title="비율(%)",
        xaxis_title="MBTI 유형",
        title=f"{country}의 MBTI 비율",
    )

    st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# 📊 탭 2: MBTI별 국가 순위
# ------------------------------
with tab2:
    st.subheader("MBTI별 국가 비율 상위 10개")

    mbti_type = st.selectbox("MBTI 유형을 선택하세요:", mbti_types)

    sorted_df = df.sort_values(by=mbti_type, ascending=False)
    top10 = sorted_df.head(10)

    # South Korea 포함 확인
    if 'South Korea' not in top10['Country'].values:
        sk_row = df[df['Country'] == 'South Korea']
        top10 = pd.concat([top10, sk_row])

    # 파란색 그라데이션 (역방향)
    min_val, max_val = top10[mbti_type].min(), top10[mbti_type].max()
    def blue_gradient(value):
        norm = (max_val - value) / (max_val - min_val) if max_val != min_val else 0
        return f"rgba(0, 0, 255, {0.3 + 0.7*norm})"

    colors = top10[mbti_type].apply(blue_gradient).tolist()
    # South Korea는 보라색
    colors = [c if country != 'South Korea' else 'rgba(180,60,180,1)' for c, country in zip(colors, top10['Country'])]

    fig2 = px.bar(
        top10,
        x='Country',
        y=mbti_type,
        text=mbti_type,
        color=top10['Country'],
        color_discrete_sequence=colors
    )

    fig2.update_traces(textposition='outside')
    fig2.update_layout(
        showlegend=False,
        yaxis_title="비율(%)",
        xaxis_title="국가",
        title=f"{mbti_type} 유형 비율이 높은 국가 Top 10",
    )

    st.plotly_chart(fig2, use_container_width=True)

