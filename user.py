import uuid


class User:

    def __init__(self):
        self.user_id = str(uuid.uuid4())
        self.balance = 0
        self.wallet_address = 0
        self.refer_link = self.create_referral_link()
        self.referrals = 0
        self.users_refered = []

    def create_referral_link(self):
        return f"ref_{self.user_id[:5]}"

    def refer_user(self, referred_user):
        self.users_refered.append(referred_user)
        self.referrals += 1

    def get_referral_count(self):
        return self.referrals

    def get_referred_users(self):
        return self.users_refered
