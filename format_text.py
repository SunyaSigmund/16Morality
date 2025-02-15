import os

# 📌 파일이 저장된 폴더 설정 (현재 'data' 폴더 사용)
DATA_DIR = "data"

# 📌 모든 텍스트 파일을 가져옴
text_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".txt")]

# 📌 파일별로 굵은 텍스트 적용하여 다시 저장
for file_name in text_files:
    file_path = os.path.join(DATA_DIR, file_name)
    
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    formatted_lines = []
    for line in lines:
        if "   " in line:  # 띄어쓰기 3개 이상 포함된 줄만 굵게 처리
            formatted_lines.append(f"**{line.strip()}**\n")  # Markdown 형식
        else:
            formatted_lines.append(line)

    # 📌 변환된 파일을 새 파일로 저장
    new_file_path = os.path.join(DATA_DIR, file_name)
    with open(new_file_path, "w", encoding="utf-8") as file:
        file.writelines(formatted_lines)

print("✅ 모든 텍스트 파일이 변환되었습니다!")
