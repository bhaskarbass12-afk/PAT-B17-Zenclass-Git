"""Create base class BankAccount with attributes like account number and balance and method
like deposit() and withdrawl. Inherit from this class to create subclasses savingsaccount and currentaccount. The savings account should have
an intrest rate and a method to calculate intrest. The currentaccount should have a minimum balance requirement. Implement encapsulation to protect the account balance
and ensure that withdrawl cannot exceed the balance or minimum balance requirement"""

class BankAccount:
    """Base class for all bank accounts."""

    def __init__(self, account_number, balance=0):
        self._account_number = account_number  # Protected attribute
        self.__balance = balance                # Private attribute (encapsulation)

    # Getter for balance (read-only access)
    @property
    def balance(self):
        return self.__balance

    # Getter for account number
    @property
    def account_number(self):
        return self._account_number

    # Protected setter - only accessible within class and subclasses
    def _set_balance(self, amount):
        """Protected method to modify balance internally."""
        self.__balance = amount

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"✅ Deposited ₹{amount}. New balance: ₹{self.__balance}")
        else:
            print("❌ Invalid deposit amount. Must be greater than 0.")

    def withdraw(self, amount):
        if amount <= 0:
            print("❌ Invalid withdrawal amount. Must be greater than 0.")
        elif amount > self.__balance:
            print(f"❌ Insufficient balance! Available: ₹{self.__balance}, Requested: ₹{amount}")
        else:
            self.__balance -= amount
            print(f"✅ Withdrew ₹{amount}. New balance: ₹{self.__balance}")

    def display_account(self):
        print(f"Account No: {self._account_number} | Balance: ₹{self.__balance}")

    def __str__(self):
        return f"Account No: {self._account_number} | Balance: ₹{self.__balance}"


class SavingsAccount(BankAccount):
    """Savings account with interest rate and interest calculation."""

    def __init__(self, account_number, balance=0, interest_rate=4.0):
        super().__init__(account_number, balance)
        self.__interest_rate = interest_rate  # Private - encapsulated

    @property
    def interest_rate(self):
        return self.__interest_rate

    @interest_rate.setter
    def interest_rate(self, rate):
        if 0 < rate < 15:
            self.__interest_rate = rate
            print(f"✅ Interest rate updated to {rate}%")
        else:
            print("❌ Invalid interest rate. Must be between 0 and 15%.")

    def calculate_interest(self):
        """Calculate annual interest on current balance."""
        interest = self.balance * (self.__interest_rate / 100)
        print(f"💰 Annual Interest at {self.__interest_rate}%: ₹{interest:.2f}")
        return interest

    def apply_interest(self):
        """Apply calculated interest to the balance."""
        interest = self.balance * (self.__interest_rate / 100)
        self._set_balance(self.balance + interest)
        print(f"✅ Interest ₹{interest:.2f} applied. New balance: ₹{self.balance:.2f}")

    def __str__(self):
        return (f"[Savings Account] Account No: {self.account_number} | "
                f"Balance: ₹{self.balance} | Interest Rate: {self.__interest_rate}%")


class CurrentAccount(BankAccount):
    """Current account with minimum balance requirement."""

    def __init__(self, account_number, balance=0, min_balance=5000):
        super().__init__(account_number, balance)
        self.__min_balance = min_balance  # Private - encapsulated

    @property
    def min_balance(self):
        return self.__min_balance

    def withdraw(self, amount):
        """Override: Ensure withdrawal doesn't go below minimum balance."""
        if amount <= 0:
            print("❌ Invalid withdrawal amount. Must be greater than 0.")
        elif amount > self.balance:
            print(f"❌ Insufficient balance! Available: ₹{self.balance}, Requested: ₹{amount}")
        elif (self.balance - amount) < self.__min_balance:
            print(f"❌ Cannot withdraw ₹{amount}! Minimum balance of ₹{self.__min_balance} must be maintained.")
            print(f"   Maximum you can withdraw: ₹{self.balance - self.__min_balance}")
        else:
            self._set_balance(self.balance - amount)
            print(f"✅ Withdrew ₹{amount}. New balance: ₹{self.balance}")

    def __str__(self):
        return (f"[Current Account] Account No: {self.account_number} | "
                f"Balance: ₹{self.balance} | Min Balance: ₹{self.__min_balance}")


# ==================== DEMONSTRATION ====================
if __name__ == "__main__":

    print("=" * 60)
    print("        BANK ACCOUNT SYSTEM - OOP WITH ENCAPSULATION")
    print("=" * 60)

    # --- Savings Account Demo ---
    print("\n" + "─" * 60)
    print("  SAVINGS ACCOUNT OPERATIONS")
    print("─" * 60)

    savings = SavingsAccount("SAV-1001", balance=10000, interest_rate=6.5)
    print(savings)

    print("\n>> Depositing ₹5000:")
    savings.deposit(5000)

    print("\n>> Withdrawing ₹3000:")
    savings.withdraw(3000)

    print("\n>> Withdrawing ₹15000 (exceeds balance):")
    savings.withdraw(15000)

    print("\n>> Calculating Interest:")
    savings.calculate_interest()

    print("\n>> Applying Interest:")
    savings.apply_interest()

    # --- Current Account Demo ---
    print("\n" + "─" * 60)
    print("  CURRENT ACCOUNT OPERATIONS")
    print("─" * 60)

    current = CurrentAccount("CUR-2001", balance=20000, min_balance=5000)
    print(current)

    print("\n>> Depositing ₹10000:")
    current.deposit(10000)

    print("\n>> Withdrawing ₹8000:")
    current.withdraw(8000)

    print("\n>> Withdrawing ₹20000 (violates min balance):")
    current.withdraw(20000)

    print("\n>> Withdrawing ₹50000 (exceeds balance):")
    current.withdraw(50000)

    # --- Encapsulation Demo ---
    print("\n" + "─" * 60)
    print("  ENCAPSULATION DEMONSTRATION")
    print("─" * 60)

    print("\n>> Trying to access private balance directly:")
    try:
        print(savings.__balance)  # This will raise AttributeError
    except AttributeError as e:
        print(f"   ❌ Access Denied! Error: {e}")
        print("   ✅ Balance is protected via encapsulation (private attribute)")

    print("\n>> Accessing balance through property (getter):")
    print(f"   Savings Balance: ₹{savings.balance}")
    print(f"   Current Balance: ₹{current.balance}")

    print("\n>> Trying to set balance directly:")
    try:
        savings.balance = 999999  # This will raise AttributeError
    except AttributeError:
        print("   ❌ Cannot set balance directly! It's read-only.")
        print("   ✅ Balance can only be modified through deposit/withdraw methods.")

    # --- Final Summary ---
    print("\n" + "=" * 60)
    print("              FINAL ACCOUNT SUMMARY")
    print("=" * 60)
    print(f"  {savings}")
    print(f"  {current}")
    print("=" * 60)