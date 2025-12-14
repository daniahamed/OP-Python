class InvalidValue(Exception):
    pass

class Wallet:
    def __init__(self, owner_id: str, balance: float):
        self.owner_id = owner_id
        self._balance = self.validate_amount(balance)
        self._transaction_history = []

    @property
    def balance(self) -> float:
        return self._balance 

    @staticmethod
    def validate_amount(amount: float) -> float:
        if amount < 0:
            raise InvalidValue("Amount must not be negative")
        else : 
            return amount

    def deposit(self, amount: float) -> None:
        amount = self.validate_amount(amount)
        self._balance += amount
        self._transaction_history.append(f"Added: {amount}, current Balance : {self._balance}")

    def withdraw(self, amount:float) -> None:
        amount = self.validate_amount(amount)
        if amount > self._balance:
            raise InvalidValue("Not enough balance")
        else :
            self._balance -= amount
            self._transaction_history.append(f"Withdrew: {amount}, current Balance : {self._balance}")

    def transfer(self, target_wallet : 'Wallet', amount: float) -> None:
        balance_before = self.balance
        amount = self.validate_amount(amount)
        self.withdraw(amount)  
        target_wallet.deposit(amount)
        print(f"Wallet Transfer: ID: {self.owner_id} -> ID: {target_wallet.owner_id} | {amount} (balance before: {balance_before}, balance after: {self.balance})")

    def show_transactions(self) -> None:
        print(self._transaction_history)

