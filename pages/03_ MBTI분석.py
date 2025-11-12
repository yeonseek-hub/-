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

# ===== 리콰이어먼트 파일 내용 안내 =====
st.markdown("---")
st.markdown("### 📦 requirements.txt")
st.code("""streamlit==1.40.0\npandas==2.2.3\nplotly==5.24.1""")
import streamlit as st

st.title("국가 선택 버튼 🌏")
st.write("버튼을 눌러 국가를 선택하세요.")

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

# 버튼 생성
for country in countries:
    if st.button(country):
        st.write(f"{country} 선택됨")
