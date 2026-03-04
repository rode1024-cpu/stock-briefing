import os

def setup():
    print("==========================================")
    print("   미국 증시 브리핑 로봇 설정 도우미")
    print("==========================================")
    print("이 프로그램이 작동하려면 '두 가지 열쇠'가 필요합니다.")
    print("\n1. Gemini API 키 (AI가 글을 쓸 때 사용)")
    print("2. G메일 앱 비밀번호 (이메일을 보낼 때 사용)")
    print("==========================================")

    gemini_key = input("\n[1/4] Gemini API 키를 입력해 주세요: ").strip()
    email_addr = input("[2/4] 본인의 G메일 주소를 입력해 주세요: ").strip()
    email_pass = input("[3/4] G메일 '앱 비밀번호'(16자리)를 입력해 주세요: ").strip()
    recipient = input("[4/4] 브리핑을 받을 이메일 주소를 입력해 주세요: ").strip()

    with open(".env", "w", encoding="utf-8") as f:
        f.write(f"GEMINI_API_KEY={gemini_key}\n")
        f.write(f"EMAIL_ADDRESS={email_addr}\n")
        f.write(f"EMAIL_PASSWORD={email_pass}\n")
        f.write(f"RECIPIENT_EMAIL={recipient}\n")

    print("\n==========================================")
    print("설정이 완료되었습니다! 이제 'run_now.bat'을 실행하면")
    print("즉시 브리핑 이메일이 발송됩니다.")
    print("==========================================")

if __name__ == "__main__":
    setup()
