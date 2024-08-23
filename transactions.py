from user import User

user = User()


class Transaction:
    amount = 0
    des_address = "b0a537f4ebc1cebbf63c30caafb820ea313970882d6e848f7a41d7f8fc2fe6af"
    token_address = 0

    @classmethod
    def withdraw_validity_check(cls):
        if int(cls.amount) > user.balance:
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
        user.balance -= int(self.amount)
        self.amount = 0
