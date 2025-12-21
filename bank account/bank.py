class InvalidValue(Exception):
    pass


class BankAccount:
    def __init__(self, account_holder: str, balance: float, pin_code : int):
        if not account_holder.strip():
            raise InvalidValue("Account holder must not be empty")

        self.account_holder = account_holder
        self.balance = self.validate_amount(balance)
        self._transaction_history = []
        self.set_pin_code(pin_code)

    def set_pin_code(self, pin_code):
        if not isinstance(pin_code, (int)):
            raise InvalidValue("Pin is Invalid")
        else:
            self.__pin_code = pin_code

    @staticmethod
    def validate_amount(amount):
        if amount <= 0:
            raise InvalidValue("Amount must be greater than zero")
        else : 
            return amount

    def deposit(self, amount):
        amount = self.validate_amount(amount)
        self.balance += amount
        self._transaction_history.append(f"Added: {amount}, current Balance : {self.balance}")

    def withdraw(self, amount, pin):
        amount = self.validate_amount(amount)
        if pin != self.__pin_code:
            raise InvalidValue("Pin is Incorrect")
        if amount > self.balance:
            raise InvalidValue("Not enough balance")
        else :
            self.balance -= amount
            self._transaction_history.append(f"Withdrew: {amount}, current Balance : {self.balance}")

    def show_balance(self, pin):
        if pin != self.__pin_code:
            raise InvalidValue("Pin is Incorrect")
        else:
            print(f"Balance : {self.balance}")

    def show_transactions(self):
        print(self._transaction_history)

    @classmethod
    def from_string(cls, string_data: str) :
        try:
            account_holder, balance, pin = string_data.split(',')
            balance = float(balance)
            pin = int(pin)
            return cls(account_holder, balance, pin)
        except ValueError:
            raise InvalidValue("Input string must be: 'name,balance,pin'")
    
    

acc1 = BankAccount("Rana", 1790 , 2324)
acc2 = BankAccount.from_string("Rana,1790,2324")

acc1.deposit(10)
acc1.withdraw(100, 2324)
acc1.show_transactions()
acc1.show_balance(2324)

acc2.deposit(10)
acc2.withdraw(100, 2324)
acc2.show_transactions()
acc2.show_balance(2324)