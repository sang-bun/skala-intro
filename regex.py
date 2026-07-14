import re


def main():
    # 사용자로부터 비밀번호를 입력받는다.
    password = input("비밀번호를 입력하세요: ")

    # 각 조건을 정규 표현식으로 검사한다.
    has_lower = re.search(r"[a-z]", password)
    has_upper = re.search(r"[A-Z]", password)
    has_number = re.search(r"\d", password)
    has_symbol = re.search(r"[^A-Za-z0-9]", password)

    # 모든 조건을 만족하는지 확인한다.
    if has_lower and has_upper and has_number and has_symbol:
        print("사용 가능한 비밀번호입니다.")
    else:
        print("사용할 수 없는 비밀번호입니다.")

        # 만족하지 않는 조건을 출력한다.
        if not has_lower:
            print("- 영문 소문자가 포함되어야 합니다.")
        if not has_upper:
            print("- 영문 대문자가 포함되어야 합니다.")
        if not has_number:
            print("- 숫자가 포함되어야 합니다.")
        if not has_symbol:
            print("- 기호가 포함되어야 합니다.")


# 프로그램의 시작점
if __name__ == "__main__":
    main()