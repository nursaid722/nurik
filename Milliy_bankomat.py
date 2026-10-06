from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class TransactionType(Enum):
    WITHDRAW = auto()
    DEPOSIT = auto()
    TRANSFER = auto()
    PAYMENT = auto()


class ATMError(Exception):
    """Bankomat operatsiyalari uchun bazaviy xatolik classi."""
    pass


class InsufficientFundsError(ATMError):
    pass


class InvalidPinError(ATMError):
    pass


class AccountCardBlockedError(ATMError):
    pass


@dataclass
class BankAccount:
    card_number: str
    pin: str
    balance: float
    phone_number: str
    is_blocked: bool = False

    def validate_pin(self, pin_input: str) -> bool:
        if self.is_blocked:
            raise AccountCardBlockedError("Karta bloklangan!")
        return self.pin == pin_input


class ATMService:
    TRANSFER_FEE_PERCENT: float = 0.01

    def __init__(self, account: BankAccount) -> None:
        self.account = account

    def get_balance(self) -> float:
        return self.account.balance

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ATMError("Summa musbat bo'lishi kerak.")
        if amount > self.account.balance:
            raise InsufficientFundsError("Mablag' yetarli emas.")
        self.account.balance -= amount
        return self.account.balance

    def deposit(self, amount: float) -> float:
        if amount <= 0:
            raise ATMError("Summa musbat bo'lishi kerak.")
        self.account.balance += amount
        return self.account.balance

    def transfer(self, target_card: str, amount: float) -> tuple[float, float]:
        if len(target_card) != 16 or not target_card.isdigit():
            raise ATMError("Karta raqami 16 xonali raqam bo'lishi kerak.")
        if amount <= 0:
            raise ATMError("Summa musbat bo'lishi kerak.")

        fee = amount * self.TRANSFER_FEE_PERCENT
        total_deduction = amount + fee

        if total_deduction > self.account.balance:
            raise InsufficientFundsError(f"Mablag' yetarli emas (Komissiya: {fee:,.2f} UZS).")

        self.account.balance -= total_deduction
        return amount, fee

    def update_phone_number(self, new_phone: str) -> str:
        if not new_phone.startswith("+998") or len(new_phone) != 13:
            raise ATMError("Raqam formati noto'g'ri (+998XXXXXXXXX).")
        self.account.phone_number = new_phone
        return self.account.phone_number

    def change_pin(self, current_pin: str, new_pin: str) -> None:
        if not self.account.validate_pin(current_pin):
            raise InvalidPinError("Joriy PIN-kod noto'g'ri.")
        if len(new_pin) != 4 or not new_pin.isdigit():
            raise ATMError("Yangi PIN 4 ta raqamdan iborat bo'lishi kerak.")
        self.account.pin = new_pin

    def pay_service(self, service_name: str, amount: float) -> float:
        if amount <= 0:
            raise ATMError("Summa musbat bo'lishi kerak.")
        if amount > self.account.balance:
            raise InsufficientFundsError("Mablag' yetarli emas.")
        self.account.balance -= amount
        return self.account.balance


class ATMController:
    MAX_ATTEMPTS: int = 3

    def __init__(self, service: ATMService) -> None:
        self.service = service

    def authenticate(self) -> bool:
        attempts = 0
        while attempts < self.MAX_ATTEMPTS:
            pin_input = input("PIN-kodni kiriting: ").strip()
            try:
                if self.service.account.validate_pin(pin_input):
                    print("Xush kelibsiz!")
                    return True
                else:
                    attempts += 1
                    print(f"PIN xato. Qolgan urinishlar: {self.MAX_ATTEMPTS - attempts}")
            except AccountCardBlockedError as e:
                print(e)
                return False

        self.service.account.is_blocked = True
        print("Urinishlar soni tugadi. Karta bloklandi!")
        return False

    def run(self) -> None:
        if not self.authenticate():
            return

        actions = {
            "1": self._handle_balance,
            "2": self._handle_withdraw,
            "3": self._handle_deposit,
            "4": self._handle_transfer,
            "5": self._handle_sms_update,
            "6": self._handle_pin_change,
            "7": self._handle_payment,
        }

        while True:
            self._display_menu()
            choice = input("\nTanlovingiz (0-7): ").strip()

            if choice == "0":
                print("Operatsiya yakunlandi. Kartangizni oling!")
                break

            action = actions.get(choice)
            if action:
                try:
                    action()
                except ATMError as e:
                    print(f"\n[XATOLIK]: {e}")
                except ValueError:
                    print("\n[XATOLIK]: Faqat son kiriting!")
            else:
                print("\nNoto'g'ri tanlov!")

    @staticmethod
    def _display_menu() -> None:
        print("\n" + "=" * 40)
        print("MILLIY BANKOMAT SERVICES".center(40))
        print("=" * 40)
        print("1. Balansni ko'rish")
        print("2. Naqd pul yechish")
        print("3. Depozit (Pul kiritish)")
        print("4. P2P Pul o'tkazish")
        print("5. SMS-xabarnoma ulash/o'zgartirish")
        print("6. PIN-kodni o'zgartirish")
        print("7. Kommunal va mobil to'lovlar")
        print("0. Chiqish")
        print("=" * 40)

    def _handle_balance(self) -> None:
        print(f"\nJoriy balans: {self.service.get_balance():,.2f} UZS")

    def _handle_withdraw(self) -> None:
        amount = float(input("Yechiladigan summa: "))
        new_balance = self.service.withdraw(amount)
        print(f"Muvaffaqiyatli! Qolgan balans: {new_balance:,.2f} UZS")

    def _handle_deposit(self) -> None:
        amount = float(input("Kiritiladigan summa: "))
        new_balance = self.service.deposit(amount)
        print(f"Muvaffaqiyatli! Yangi balans: {new_balance:,.2f} UZS")

    def _handle_transfer(self) -> None:
        card = input("Qabul qiluvchi karta (16 xona): ").strip()
        amount = float(input("O'tkazma summasi: "))
        sent, fee = self.service.transfer(card, amount)
        print(f"Muvaffaqiyatli o'tkazildi: {sent:,.2f} UZS (Komissiya: {fee:,.2f} UZS)")

    def _handle_sms_update(self) -> None:
        phone = input("Yangi raqam (+998XXXXXXXXX): ").strip()
        updated = self.service.update_phone_number(phone)
        print(f"SMS-xabarnoma {updated} raqamiga ulandi.")

    def _handle_pin_change(self) -> None:
        current_pin = input("Joriy PIN: ").strip()
        new_pin = input("Yangi PIN: ").strip()
        self.service.change_pin(current_pin, new_pin)
        print("PIN-kod muvaffaqiyatli o'zgartirildi!")

    def _handle_payment(self) -> None:
        service_name = input("Xizmat nomi (Masalan: Paynet / Gaz): ").strip()
        amount = float(input("To'lov summasi: "))
        new_balance = self.service.pay_service(service_name, amount)
        print(f"To'lov bajarildi! Qolgan balans: {new_balance:,.2f} UZS")


if __name__ == "__main__":
    card_account = BankAccount(
        card_number="8600123456789012",
        pin="7777",
        balance=5000000.0,
        phone_number="+998901234567"
    )

    atm_service = ATMService(account=card_account)
    app = ATMController(service=atm_service)
    app.run()
