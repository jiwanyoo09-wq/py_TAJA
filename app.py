import streamlit as st
import random
import time
from difflib import SequenceMatcher

st.set_page_config(
    page_title="Python 타자 연습",
    page_icon="⌨️",
    layout="centered"
)

# 연습 문장
sentences = [
    "print('Hello World')",
    "for i in range(10):",
    "if x == 10:",
    "def add(a, b):",
    "return a + b",
    "import random",
    "while True:",
    "class Person:",
    "try:",
    "except Exception as e:",
    "list_comprehension = [x for x in range(5)]",
    "with open('file.txt', 'r') as f:",
]

# 세션 상태 초기화
if "target_text" not in st.session_state:
    st.session_state.target_text = random.choice(sentences)

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "finished" not in st.session_state:
    st.session_state.finished = False

st.title("⌨️ Python 타자 연습")
st.write("Python 코드를 그대로 입력해보세요.")

# 목표 문장 표시
st.code(st.session_state.target_text, language="python")

# 입력 시작 시 시간 기록
user_input = st.text_input("여기에 입력하세요")

if user_input and st.session_state.start_time is None:
    st.session_state.start_time = time.time()

# 결과 계산
if user_input == st.session_state.target_text:
    end_time = time.time()
    elapsed_time = end_time - st.session_state.start_time

    # WPM 계산
    words = len(user_input) / 5
    wpm = words / (elapsed_time / 60)

    # 정확도 계산
    accuracy = SequenceMatcher(
        None,
        user_input,
        st.session_state.target_text
    ).ratio() * 100

    st.success("정답입니다!")

    st.metric("⏱ 걸린 시간", f"{elapsed_time:.2f} 초")
    st.metric("⚡ 타자 속도", f"{wpm:.2f} WPM")
    st.metric("🎯 정확도", f"{accuracy:.2f}%")

    st.session_state.finished = True

# 새 문제 버튼
if st.button("새 문제"):
    st.session_state.target_text = random.choice(sentences)
    st.session_state.start_time = None
    st.session_state.finished = False
    st.rerun()
