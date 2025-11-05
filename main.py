import streamlit as st
st.title('나의 첫 웹 서비스 만들기!')
a=st.text_input('이름을 입력해 주세요')
b=st.selectbox('좋아하는 음식을 선택하시오!',['이차현의 다태운 바게트','쌉뚱땡이 몽블랑','현우의 검은 마음'])
if st.button('인사말 생성'):
  st. info(a+'님 안녕하세요 반갑습니다!')
  st.warring(b+'를 좋아하는구나! 저도 좋아해요!')
  st.error('반가워요!!')
