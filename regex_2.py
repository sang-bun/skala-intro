import re


# 비밀번호가 조건을 만족하는지 검사하는 함수
def check_password(password):
    has_lower = re.search(r"[a-z]", password)
    has_upper = re.search(r"[A-Z]", password)
    has_number = re.search(r"\d", password)
    has_symbol = re.search(r"[^A-Za-z0-9]", password)

    return has_lower and has_upper and has_number and has_symbol


def main():
    # 사용자가 종료를 입력할 때까지 반복한다.
    while True:
        # 사용자로부터 비밀번호를 입력받는다.
        password = input("비밀번호를 입력하세요 (!quit 입력 시 종료): ")

        # 종료 명령을 입력하면 프로그램을 종료한다.
        if password == "!quit":
            print("프로그램을 종료합니다.")
            break

        # 입력한 비밀번호를 그대로 출력한다. (echo)
        print("입력한 비밀번호:", password)

        # 비밀번호의 유효성을 검사한다.
        if check_password(password):
            print("→ 사용 가능한 비밀번호입니다.")
        else:
            print("→ 사용할 수 없는 비밀번호입니다.")
            print("  - 영문 소문자, 영문 대문자, 숫자, 기호를 각각 최소 1개 이상 포함해야 합니다.")

        print()  # 보기 좋게 한 줄 띄우기


# 프로그램의 시작점
if __name__ == "__main__":
    main()