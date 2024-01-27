class LeaderBoard:
    def __init__(self, database):
        self.database = database

    def sort_leaderboard(self):
        self.database.sort(key=lambda x: x.referrals, reverse=True)
        return "Database Sorted"

    def get_leaderboard(self):
        self.sort_leaderboard()
        for user in self.database:
            print(f"User {user.name}    Referrals: {user.referrals}")
