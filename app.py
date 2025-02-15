from flask import Flask, render_template, request
import os

app = Flask(__name__)

# 📌 현재 파일(app.py)이 위치한 디렉토리 기준으로 data 폴더 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# 📌 질문 파일 목록 (경로 수정)
QUESTION_FILES = [
    os.path.join(DATA_DIR, "1. D & U question.txt"),
    os.path.join(DATA_DIR, "2. I & M question.txt"),
    os.path.join(DATA_DIR, "3. H & C question.txt"),
    os.path.join(DATA_DIR, "4. A & P question.txt")
]

# 📌 질문을 불러오는 함수 (문제 해결)
def load_questions():
    questions = []
    for file_path in QUESTION_FILES:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                file_questions = [line.strip() for line in file.readlines()]
                questions.extend(file_questions)  # ✅ 단순 리스트로 추가
    return questions  # ✅ 리스트 반환

# 📌 성격 유형 설명 파일 경로 수정
PERSONALITY_FILES = {
    "DICA": os.path.join(DATA_DIR, "DICA.txt"),
    "DICP": os.path.join(DATA_DIR, "DICP.txt"),
    "DIHA": os.path.join(DATA_DIR, "DIHA.txt"),
    "DIHP": os.path.join(DATA_DIR, "DIHP.txt"),
    "DMCA": os.path.join(DATA_DIR, "DMCA.txt"),
    "DMCP": os.path.join(DATA_DIR, "DMCP.txt"),
    "DMHA": os.path.join(DATA_DIR, "DMHA.txt"),
    "DMHP": os.path.join(DATA_DIR, "DMHP.txt"),
    "UIHA": os.path.join(DATA_DIR, "UIHA.txt"),
    "UIHP": os.path.join(DATA_DIR, "UIHP.txt"),
    "UICA": os.path.join(DATA_DIR, "UICA.txt"),
    "UICP": os.path.join(DATA_DIR, "UICP.txt"),
    "UMHA": os.path.join(DATA_DIR, "UMHA.txt"),
    "UMHP": os.path.join(DATA_DIR, "UMHP.txt"),
    "UMCA": os.path.join(DATA_DIR, "UMCA.txt"),
    "UMCP": os.path.join(DATA_DIR, "UMCP.txt")
}

# 📌 성격 유형 설명을 불러오는 함수 (줄바꿈 문제 해결)
def load_personality_description(personality_code):
    file_path = PERSONALITY_FILES.get(personality_code, None)
    if file_path and os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip().replace("\n", "<br>")  # ✅ 줄바꿈 유지
    return "설명 파일을 찾을 수 없습니다."

# 📌 사용자의 점수를 바탕으로 성격 유형을 결정하는 함수
def determine_personality(scores):
    personality = ""
    personality += "D" if scores["D"] > scores["U"] else "U"
    personality += "I" if scores["I"] > scores["M"] else "M"
    personality += "H" if scores["H"] > scores["C"] else "C"
    personality += "A" if scores["A"] > scores["P"] else "P"
    return personality

# 📌 메인 페이지 (설문조사 페이지)
@app.route('/')
def index():
    questions = load_questions()  
    return render_template('index.html', questions=questions)  # ✅ 리스트만 전달

# 📌 설문조사 제출 후 결과 계산
@app.route('/submit', methods=['POST'])
def submit():
    try:
        questions = load_questions()
        total_scores = {"D": 0, "U": 0, "I": 0, "M": 0, "H": 0, "C": 0, "A": 0, "P": 0}

        for i, question in enumerate(questions):
            score = request.form.get(f'q{i+1}', None)

            if score is None or score == "":  # ✅ 체크 안 한 경우 에러 페이지로 이동
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

# 📌 Flask 실행
if __name__ == '__main__':
    app.run(debug=True)
