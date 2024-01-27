from user import User


class Transaction:
    amount = 0
    des_address = 0
    token_address = 0

    @classmethod
    def withdraw_validity_check(cls):
        if int(cls.amount) > User.balance:
            return False
        return True

    @classmethod
    def withdraw_address_validity_check(cls):
        t = [999]
        if cls.des_address not in t:
            return False
        return True

    @classmethod
    def token_address_validity_check(cls):
        t = []
        if cls.token_address not in t:
            return False
        return True

    def withdraw(self):
        User.balance -= int(self.amount)
        self.amount = 0
