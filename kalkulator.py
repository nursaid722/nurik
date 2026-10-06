def kalkulyator():
    print("=== SODDA KALKULYATOR ===")

    while True:
        try:
            num1 = float(input("\nBirinchi sonni kiriting: "))
            amal = input("Amalni kiriting (+, -, *, /): ").strip()
            num2 = float(input("Ikkinchi sonni kiriting: "))

            if amal == "+":
                natija = num1 + num2
            elif amal == "-":
                natija = num1 - num2
            elif amal == "*":
                natija = num1 * num2
            elif amal == "/":
                if num2 == 0:
                    print("Xatolik: Nolga bo'lish mumkin emas!")
                    continue
                natija = num1 / num2
            else:
                print("Noto'g'ri amal kiritildi!")
                continue

            # Agar natija butun son bo'lsa, .0 qismini olib tashlaymiz
            if natija.is_integer():
                natija = int(natija)

            print(f"Natija: {num1} {amal} {num2} = {natija}")

        except ValueError:
            print("Xatolik: Iltimos, faqat son kiriting!")

        davom = input("\nYana hisoblaysizmi? (ha/yo'q): ").lower()
        if davom != "ha":
            print("Dastur yakunlandi. Salomat bo'ling!")
            break


if __name__ == "__main__":
    kalkulyator()