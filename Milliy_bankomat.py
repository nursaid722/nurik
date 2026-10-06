balans = 5000000.0
PAROL = 7777
telefon_raqam = "+998901234567"
KOMISSIYA_FOIZI = 1.0


def balansni_korish():
    print(f"\n[BALANS]: Hozirgi kartangiz balansi: {balans:,.2f} so'm")


def naqd_yechish():
    global balans
    try:
        summa = float(input("\nYechiladigan summani kiriting (so'm): "))
        if summa <= 0:
            print("Noto'g'ri summa kiritildi.")
        elif summa > balans:
            print("Xatolik: Kartada mablag' yetarli emas!")
        else:
            balans -= summa
            print(f"Muvaffaqiyatli! {summa:,.2f} so'm berildi.")
            print(f"Qolgan balans: {balans:,.2f} so'm")
    except ValueError:
        print("Xatolik: Faqat son kiritishingiz kerak!")


def pul_kiritish():
    global balans
    try:
        summa = float(input("\nKiritilayotgan naqd pul summasini kiriting: "))
        if summa > 0:
            balans += summa
            print(f"Kartangizga {summa:,.2f} so'm muvaffaqiyatli qo'shildi.")
            print(f"Yangi balans: {balans:,.2f} so'm")
        else:
            print("Noto'g'ri summa kiritildi.")
    except ValueError:
        print("Xatolik: Faqat son kiritishingiz kerak!")


def pul_otkazish():
    global balans
    karta_raqam = input("\nQabul qiluvchi karta raqamini kiriting (16 xona): ")

    if len(karta_raqam) != 16 or not karta_raqam.isdigit():
        print("Xatolik: Karta raqami 16 xonali raqam bo'lishi kerak!")
        return

    try:
        summa = float(input("O'tkazma summasini kiriting: "))
        komissiya = summa * (KOMISSIYA_FOIZI / 100)
        umumiy_summa = summa + komissiya

        if umumiy_summa > balans:
            print(f"Xatolik: Mablag' yetarli emas! Komissiya (1%): {komissiya:,.2f} so'm")
        else:
            balans -= umumiy_summa
            print(f"Muvaffaqiyatli! {summa:,.2f} so'm {karta_raqam} kartasiga o'tkazildi.")
            print(f"Komissiya: {komissiya:,.2f} so'm | Qolgan balans: {balans:,.2f} so'm")
    except ValueError:
        print("Xatolik: Faqat son kiritishingiz kerak!")


def sms_boshqarish():
    global telefon_raqam
    print(f"\n[SMS-XABARNOMA]: BIRIKTIRILGAN RAQAM: {telefon_raqam}")
    yangi_raqam = input("Yangi telefon raqamini kiriting (+998...): ")
    telefon_raqam = yangi_raqam
    print(f"SMS-xabarnoma xizmati {telefon_raqam} raqamiga qayta ulandi.")


def pin_ozgartirish():
    global PAROL
    try:
        yangi_pin = int(input("\nYangi 4 xonali PIN-kodni kiriting: "))
        if 1000 <= yangi_pin <= 9999:
            PAROL = yangi_pin
            print("PIN-kod muvaffaqiyatli o'zgartirildi!")
        else:
            print("Xatolik: PIN-kod 4 xonali son bo'lishi kerak!")
    except ValueError:
        print("Xatolik: Faqat raqam kiriting!")


def tolovlar():
    global balans
