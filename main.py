import streamlit as st
st.title('나의 첫 웹 서비스 만들기!')
a=st.text_input('이름을 입력해 주세요')
if st.button('인사말 생성'):
  st. wirte(a+'님 안녕 반갑습니다!')
