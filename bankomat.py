import sys


def bankomat_dasturi():
    # Boshlang'ich ma'lumotlar
    haqiqiy_pin = "1234"
    balans = 500000  # so'm
    urinishlar = 3

    print("=== BANKOMAT TIZIMIGA XUSH KELIBSIZ ===")

    # PIN-kodni tekshirish
    while urinishlar > 0:
        kiritilgan_pin = input("PIN-kodni kiriting (4 xonali): ")

        if kiritilgan_pin == haqiqiy_pin:
            print("\nPIN-kod to'g'ri kiritildi!\n")
            break
        else:
            urinishlar -= 1
            if urinishlar > 0:
                print(f"Xato PIN! Qolgan urinishlar soni: {urinishlar}\n")
            else:
                print("PIN-kod 3 marta xato kiritildi. Kartangiz bloklandi!")
                sys.exit()

    # Bankomat menyusi
    while True:
        print("--- MENYU ---")
        print("1. Balansni tekshirish")
        print("2. Pul yechish")
        print("3. Pul kiritish (Balansni to'ldirish)")
        print("4. Chiqish")

        tanlov = input("Bajariladigan amalni tanlang (1-4): ")

        if tanlov == "1":
            print(f"\nJoriy balans: {balans:,} so'm\n")

        elif tanlov == "2":
            summa = int(input("\nYechib olmoqchi bo'lgan summani kiriting: "))
            if summa <= 0:
                print("Noto'g'ri summa kiritildi!\n")
            elif summa > balans:
                print("Hisobingizda yetarli mablag' mavjud emas!\n")
            else:
                balans -= summa
                print(f"Muvaffaqiyatli! {summa:,} so'm berildi.")
                print(f"Qolgan balans: {balans:,} so'm\n")

        elif tanlov == "3":
            summa = int(input("\nKiritmoqchi bo'lgan summani kiriting: "))
            if summa <= 0:
                print("Noto'g'ri summa kiritildi!\n")
            else:
                balans += summa
                print(f"Muvaffaqiyatli! Hisobingizga {summa:,} so'm qo'shildi.")
                print(f"Yangi balans: {balans:,} so'm\n")

        elif tanlov == "4":
            print("\nXizmatingizdan mamnunmiz! Kartangizni olishni unutmang.")
            break
        else:
            print("\nNoto'g'ri tanlov kiritildi, qaytadan urinib ko'ring.\n")


# Dasturni ishga tushirish
if __name__ == "__main__":
    bankomat_dasturi()
