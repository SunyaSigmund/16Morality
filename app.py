from flask import Flask, render_template, request, redirect
import os
import re  # ✅ 정규 표현식 사용 (굵은 글씨 부분만 변환)
import html  # ✅ HTML 엔터티 변환 라이브러리 추가

app = Flask(__name__)

# 📌 현재 파일(app.py)이 위치한 디렉토리 기준으로 data 폴더 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
EMAIL_FILE = os.path.join(DATA_DIR, "emails.txt")  # ✅ 이메일 저장 파일 추가

# 📌 질문 파일 목록 (경로 수정)
QUESTION_FILES = [
    os.path.join(DATA_DIR, "1. D & U question.txt"),
    os.path.join(DATA_DIR, "2. I & M question.txt"),
    os.path.join(DATA_DIR, "3. H & C question.txt"),
    os.path.join(DATA_DIR, "4. A & P question.txt")
]

# 📌 질문을 불러오는 함수
def load_questions():
    questions = []
    for file_path in QUESTION_FILES:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                file_questions = [line.strip() for line in file.readlines()]
                questions.extend(file_questions)  
    return questions  

# 📌 성격 유형 설명 파일 경로 수정
PERSONALITY_FILES = {key: os.path.join(DATA_DIR, f"{key}.txt") for key in [
    "DICA", "DICP", "DIHA", "DIHP", "DMCA", "DMCP", "DMHA", "DMHP",
    "UIHA", "UIHP", "UICA", "UICP", "UMHA", "UMHP", "UMCA", "UMCP"
]}

# 📌 성격 유형 설명을 불러오는 함수 (정확한 굵은 글씨 적용 + 줄바꿈 유지)
def load_personality_description(personality_code):
    file_path = PERSONALITY_FILES.get(personality_code, None)
    if file_path and os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read().strip()

        # ✅ "<DICA가 선호하는 환경>" 같은 부분이 사라지지 않도록 변환
        content = html.escape(content)  # `<` 와 `>` 기호를 `&lt;` 와 `&gt;` 로 변환
        content = content.replace("&lt;b&gt;", "<b>").replace("&lt;/b&gt;", "</b>")  # 굵은 글씨 복구

        # ✅ **이 안에 있는 글씨**만 굵게 변환 (이중 변환 방지)
        content = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", content)

        # ✅ 줄바꿈 유지 (중복 변환 방지)
        content = content.replace("\n", "<br>")

        return content  # ✅ 결과를 한 번만 반환 (중복 방지)
    return "설명 파일을 찾을 수 없습니다."


# 📌 사용자의 점수를 바탕으로 성격 유형을 결정하는 함수
def determine_personality(scores):
    traits = [
        ("D", "U"),
        ("I", "M"),
        ("H", "C"),
        ("A", "P")
    ]
    personality = "".join(max(trait, key=lambda x: scores[x]) for trait in traits)
    return personality

# 📌 이메일을 파일에 저장하는 함수
def save_email(email):
    with open(EMAIL_FILE, "a", encoding="utf-8") as file:
        file.write(email + "\n")

# 📌 메인 페이지 (설문조사 페이지)
@app.route('/')
def index():
    questions = load_questions()
    return render_template('index.html', questions=questions)

# 📌 설문조사 제출 후 결과 계산
@app.route('/submit', methods=['POST'])
def submit():
    try:
        questions = load_questions()
        total_scores = {trait: 0 for trait in "DUIMHCAP"}

        for i, question in enumerate(questions):
            score = request.form.get(f'q{i+1}', None)

            if score is None or score == "":
                return render_template("error.html", message="⚠ 질문 사항을 모두 체크해주세요. ⚠")

            score = int(score)

            if i < len(questions) / 4:
                total_scores["D"] += score
                total_scores["U"] += 8 - score
            elif i < len(questions) / 2:
                total_scores["I"] += score
                total_scores["M"] += 8 - score
            elif i < 3 * len(questions) / 4:
                total_scores["H"] += score
                total_scores["C"] += 8 - score
            else:
                total_scores["A"] += score
                total_scores["P"] += 8 - score

        # 📌 성격 유형 결정
        personality_code = determine_personality(total_scores)
        personality_description = load_personality_description(personality_code)

        return render_template('result.html', personality=personality_code, description=personality_description)
    except Exception as e:
        return render_template("error.html", message=f"오류 발생: {e}")

# 📌 이메일 수집 처리 라우트
@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    if email:
        save_email(email)
        return redirect('/')  
    return "이메일을 입력해주세요.", 400

# 📌 Flask 실행
if __name__ == "__main__":
    app.run(debug=True)
