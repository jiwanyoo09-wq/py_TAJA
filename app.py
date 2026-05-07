import streamlit as st
import random
import time
from difflib import SequenceMatcher

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="Python 코드 타자 연습",
    page_icon="⌨️",
    layout="wide"
)

# -----------------------------
# 난이도별 문제
# -----------------------------
QUESTIONS = {
    "초급": [
        "print('Hello World')",
        "x = 10",
        "name = input('이름 입력: ')",
        "for i in range(5):\n    print(i)",
        "if x > 0:\n    print('양수')",
    ],

    "중급": [
        "numbers = [x for x in range(10)]",
        "def add(a, b):\n    return a + b",
        "for i in range(3):\n    for j in range(2):\n        print(i, j)",
        "try:\n    x = int(input())\nexcept ValueError:\n    print('숫자 입력')",
        "with open('data.txt', 'r') as file:\n    data = file.read()",
    ],

    "고급": [
        "class Person:\n    def __init__(self, name):\n        self.name = name\n\n    def greet(self):\n        return f'Hello {self.name}'",
        
        "@staticmethod\ndef multiply(a, b):\n    return a * b",

        "result = list(map(lambda x: x**2, range(10)))",

        "async def fetch_data():\n    await asyncio.sleep(1)\n    return '완료'",

        "from collections import Counter\n\ntext = 'banana'\ncount = Counter(text)\nprint(count)",
    ]
}

# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "초급"

if "question" not in st.session_state:
    st.session_state.question = random.choice(
        QUESTIONS[st.session_state.difficulty]
    )

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# -----------------------------
# 사이드바
# -----------------------------
st.sidebar.title("⚙️ 설정")

difficulty = st.sidebar.selectbox(
    "난이도 선택",
    ["초급", "중급", "고급"]
)

# 난이도 변경 시 문제 초기화
if difficulty != st.session_state.difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.question = random.choice(
        QUESTIONS[difficulty]
    )
    st.session_state.user_input = ""
    st.session_state.start_time = None

# -----------------------------
# 제목
# -----------------------------
st.title("⌨️ Python 코드 타자 연습")
st.markdown("Python 코드를 정확하게 입력해보세요.")

# -----------------------------
# 문제 표시
# -----------------------------
st.subheader("📌 제시 코드")

st.code(
    st.session_state.question,
    language="python"
)

# -----------------------------
# 코드 입력창
# -----------------------------
st.subheader("💻 코드 입력")

user_input = st.text_area(
    "아래 코드 입력",
    value=st.session_state.user_input,
    height=250,
    placeholder="여기에 Python 코드를 입력하세요...",
)

# 입력 시작 시간 기록
if user_input and st.session_state.start_time is None:
    st.session_state.start_time = time.time()

st.session_state.user_input = user_input

# -----------------------------
# 결과 계산
# -----------------------------
if user_input.strip() == st.session_state.question.strip():

    elapsed = time.time() - st.session_state.start_time

    # 정확도
    accuracy = SequenceMatcher(
        None,
        user_input,
        st.session_state.question
    ).ratio() * 100

    # WPM 계산
    words = len(user_input) / 5
    wpm = words / (elapsed / 60)

    st.success("🎉 정답입니다!")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("⏱ 시간", f"{elapsed:.2f}초")

    with col2:
        st.metric("⚡ 속도", f"{wpm:.2f} WPM")

    with col3:
        st.metric("🎯 정확도", f"{accuracy:.2f}%")

# -----------------------------
# 새 문제 버튼
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 새 문제"):
        st.session_state.question = random.choice(
            QUESTIONS[st.session_state.difficulty]
        )
        st.session_state.user_input = ""
        st.session_state.start_time = None
        st.rerun()

with col2:
    if st.button("🧹 초기화"):
        st.session_state.user_input = ""
        st.session_state.start_time = None
        st.rerun()

# -----------------------------
# 하단 설명
# -----------------------------
st.markdown("---")
st.caption("Python 문법 타자 연습용 Streamlit 앱")
