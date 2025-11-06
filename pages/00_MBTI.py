import streamlit as st

MBTI_LIST = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ",
]

# 각 유형별로 진로 2개, 적합 학과, 어떤 성격에 맞는지, 그리고 이모지 포함
MBTI_CAREERS = {
    "ISTJ": [
        {"career": "회계사/감사", "dept": "경영학과/회계학과", "personality": "정확하고 책임감 강함, 규칙과 절차를 잘 지키는 타입", "emoji": "📊"},
        {"career": "품질관리 엔지니어", "dept": "산업공학과/생산관리", "personality": "세부사항에 강하고 꾸준히 문제를 찾고 해결함", "emoji": "🔧"},
    ],
    "ISFJ": [
        {"career": "간호사/보건관리", "dept": "간호학과/보건학과", "personality": "다른 사람 돌보는 걸 좋아하고 신중한 스타일", "emoji": "🩺"},
        {"career": "교육 행정/사무", "dept": "교육학과/행정학과", "personality": "성실하고 맡은 일 끝까지 하는 타입", "emoji": "📚"},
    ],
    "INFJ": [
        {"career": "상담사/임상심리", "dept": "심리학과/상담심리학과", "personality": "타인의 감정 공감에 능하고 의미를 중시함", "emoji": "🧠"},
        {"career": "비영리 기획/콘텐츠", "dept": "사회복지학과/문화콘텐츠학과", "personality": "가치 중심으로 일하며 기획에 강함", "emoji": "🤝"},
    ],
    "INTJ": [
        {"career": "연구개발(R&D)", "dept": "화학/생명공학/전기전자 공학", "personality": "전략적 사고와 장기 계획에 능함", "emoji": "🔬"},
        {"career": "데이터 사이언티스트", "dept": "통계학과/컴퓨터공학과", "personality": "논리적 분석과 문제분해를 즐김", "emoji": "💻"},
    ],
    "ISTP": [
        {"career": "기계·설비 엔지니어", "dept": "기계공학과/메카트로닉스", "personality": "실무 중심, 손으로 해결하는 걸 좋아함", "emoji": "🛠️"},
        {"career": "제품 디자이너/테크니션", "dept": "산업디자인과/공학계열", "personality": "실용적이고 즉각적 문제해결 능력", "emoji": "🧩"},
    ],
    "ISFP": [
        {"career": "셰프/파티시에", "dept": "조리학과/제과제빵과", "personality": "감각적이고 손으로 만드는 작업에서 행복함", "emoji": "🍰"},
        {"career": "플로리스트/조경", "dept": "원예학과/조경학과", "personality": "시각적 감각과 세심함이 강함", "emoji": "🌿"},
    ],
    "INFP": [
        {"career": "작가/콘텐츠 크리에이터", "dept": "문예창작/미디어학과", "personality": "내면의 가치와 스토리텔링을 중시함", "emoji": "✍️"},
        {"career": "문화예술 기획", "dept": "문화콘텐츠학과/예술경영", "personality": "창의적 아이디어로 의미 있는 일을 하고 싶어함", "emoji": "🎭"},
    ],
    "INTP": [
        {"career": "소프트웨어 개발자", "dept": "컴퓨터공학과/소프트웨어학과", "personality": "이론적 분석을 즐기고 문제 해결을 좋아함", "emoji": "🧠"},
        {"career": "연구원/학자", "dept": "전공 관련 이론 연구 분야", "personality": "독립적 연구와 깊이 있는 탐구에 적합함", "emoji": "📐"},
    ],
    "ESTP": [
        {"career": "영업/마케팅", "dept": "경영학과/마케팅전공", "personality": "사교적이고 현장에서 기민하게 행동함", "emoji": "💼"},
        {"career": "이벤트 기획/운영", "dept": "관광경영/문화콘텐츠학과", "personality": "순간 판단과 사람 움직이는 걸 즐김", "emoji": "🎉"},
    ],
    "ESFP": [
        {"career": "연예·무대 예술", "dept": "공연예술학과/방송연예과", "personality": "무대에서 에너지를 발산하고 사람 좋아함", "emoji": "🎤"},
        {"career": "리테일 매니저", "dept": "유통관리/경영학과", "personality": "서비스 정신이 뛰어나고 사람을 기쁘게 함", "emoji": "🛍️"},
    ],
    "ENFP": [
        {"career": "브랜딩/크리에이티브", "dept": "광고홍보학과/디자인학과", "personality": "아이디어가 많고 사람을 이끄는 매력", "emoji": "✨"},
        {"career": "HR·조직문화 담당", "dept": "경영학과/심리학과", "personality": "사람 중심으로 분위기 만들기 좋아함", "emoji": "🤗"},
    ],
    "ENTP": [
        {"career": "스타트업 창업가", "dept": "경영학과/융합전공", "personality": "새로운 기회를 발견하고 실험을 즐김", "emoji": "🚀"},
        {"career": "제품 매니저", "dept": "산업공학과/경영학과", "personality": "아이디어를 실무로 전환하는 능력 보유", "emoji": "🧭"},
    ],
    "ESTJ": [
        {"career": "프로젝트 매니저", "dept": "경영학과/산업공학과", "personality": "조직 운영과 일정 관리에 능함", "emoji": "📅"},
        {"career": "공공 행정/관리", "dept": "행정학과/정책학과", "personality": "규율과 책임을 중요시함", "emoji": "🏛️"},
    ],
    "ESFJ": [
        {"career": "교사/교육 컨설턴트", "dept": "교육학과/상담교육과", "personality": "사람을 돕고 조율하는 걸 즐김", "emoji": "🧑‍🏫"},
        {"career": "고객관리(CS) 매니저", "dept": "경영학과/서비스경영", "personality": "친화력 높고 고객 만족을 중시함", "emoji": "🤝"},
    ],
    "ENFJ": [
        {"career": "HR 리더/교육 코치", "dept": "경영학과/심리학과", "personality": "사람을 성장시키는 걸 즐기고 리더십 있음", "emoji": "🌱"},
        {"career": "공공정책·사회복지 기획", "dept": "사회복지학과/정책학과", "personality": "사회적 영향력을 만들고 싶어함", "emoji": "🧭"},
    ],
    "ENTJ": [
        {"career": "경영진/전략 컨설턴트", "dept": "경영학과/경제학과", "personality": "목표지향적이고 리더십이 강함", "emoji": "🏆"},
        {"career": "VC/투자 심사역", "dept": "금융학과/경영학과", "personality": "사업성과 판단과 전략적 안목 보유", "emoji": "💡"},
    ],
}

st.set_page_config(page_title="MBTI 진로 추천 (대장 전용)", layout="centered")

st.title("🔎 MBTI로 보는 진로 추천")
st.markdown("친구, 안녕! 아래에서 MBTI 유형을 선택하면 해당 유형에 어울리는 **진로 2가지**, **추천 학과**, 그리고 **어떤 성격**이 잘 맞는지 보여줄게. 이걸로 진로 아이디어를 얻어봐~ 😄")

mbti = st.selectbox("MBTI 유형을 골라줘 (예: ISFP)", MBTI_LIST)

if st.button("추천 보기 👍"):
    careers = MBTI_CAREERS.get(mbti)
    if careers:
        st.subheader(f"{mbti} 유형 추천 진로 2가지")
        for i, item in enumerate(careers, start=1):
            st.markdown(f"### {i}. {item['emoji']} {item['career']}")
            st.write(f"**추천 학과:** {item['dept']}")
            st.write(f"**어떤 성격이 잘 맞을까?** {item['personality']}")
            st.write("---")
    else:
        st.info("해당 유형 정보가 아직 없어요. 다음 업데이트에 추가할게요!")

st.caption("※ 이 추천은 성향 기반의 일반적 제안이야. 진로 결정은 실습・체험・멘토링을 통해 확인하길 권해.")

st.write("\n")

