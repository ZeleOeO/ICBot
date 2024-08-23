import uuid


class User:

    def __init__(self):
        self.username = ""
        self.user_id = str(uuid.uuid4())
        self.balance = 0
        self.wallet_address = "Set Wallet Phrase"
        self.refer_link = self.create_referral_link()
        self.referrals = 0
        self.users_refered = []

    def set_username(self, username: str):
        self.wallet_address = "61835ae0dae6bd1e4ad2a4d902e81b19121ed467e78f03fc99bea93a152e4411"
        self.username = username

    def set_balance(self, balance: float):
        self.balance = balance

    def create_referral_link(self):
        return f"ref_{self.user_id[:5]}"

    def refer_user(self, referred_user):
        self.users_refered.append(referred_user)
        self.referrals += 1

    def get_referral_count(self):
        return self.referrals

    def get_referred_users(self):
        return self.users_refered
