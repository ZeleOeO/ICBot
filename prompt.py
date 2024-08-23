from helper import global_user as user


def get_prompt(prompt: str, username: str | None = None) -> str:
    global user

    value = ""
    match prompt:
        case "ICP-Start":
            value = f"""Welcome to ICPBot 🚀Your one-stop destination for managing your ICP wallet and seamlessly trading DFINITY's ICP tokens right from Telegram!
  Currently, your ICP wallet shows a balance of 0 ICP. To kickstart your trading journey, deposit some ICP into your CryptoSphere wallet address:

  `{user.wallet_address}` (click to copy)

  After completing the deposit, simply tap on the refresh button, and voila! Your updated ICP balance will be displayed right here.

  To initiate a trade, just input the token's address or drop the canister link of the specific ICP token you're eyeing.

  For a comprehensive overview of your wallet, including options to manage and safeguard your assets, tap on the wallet icon below. Remember, while CryptoSphere ensures the utmost security, safeguarding your private key is paramount for asset protection.
                                                      Check the Menu Below
      """
        case "Wallet-Menu":
            value = f"""
    *Your Wallet:*
    Address: `{user.wallet_address}`
    Balance: *${user.balance:.2f}*

    Click to copy Wallet Address
      """
        case "Buy-Menu":
            value = """Buy Token:

To buy a token, enter a token address:"""
        case "Sell-Menu":
            value = "No open positions"
        case "Help-Menu":
            value = """
**Welcome to ICPBot Help!**

Here are some common questions and answers:

- **Which tokens can I trade?**
  You can trade any SPL token that is a Sol pair on Raydium, Orca, and Jupiter. Raydium pairs are picked up instantly, and Jupiter will pick up non-SOL pairs within approximately 15 minutes.

- **How can I see my referral earnings?**
  Check the "Referrals" button or type `/referrals` to see your earnings in Bonk!

- **Creating a new wallet on BONKbot:**
  Click the Wallet button or type `/wallet` to configure a new wallet.

- **Is BONKbot free? Transaction fees?**
  BONKbot is completely free! We charge a 1% fee on transactions to keep the bot accessible to everyone.

- **Why is my net profit lower than expected?**
  Net profit is calculated after deducting all associated costs, including Price Impact, Transfer Tax, Dex Fees, and a 1% BONKbot fee.

For any further questions, feel free to join our Telegram Group Chat.
    """
        case "Refer-Menu":
            value = f"""
**Referrals:**

Your reflink: [https://t.me/IC_Deca_Bot?start={user.refer_link}](https://t.me/IC_Deca_Bot?start={user.refer_link})

Referrals: 0
Lifetime Bonk earned: 0.00 BONK ($0.00)

Rewards are updated at least every 24 hours, and rewards are automatically deposited to your BONK balance.

Refer your friends and earn:

- 30% of their fees in the first month.
- 20% in the second month.
- 10% forever!

Encourage your friends to join and start trading with BONKbot. You'll earn a percentage of their transaction fees, providing a passive income stream. Share your reflink and watch your earnings grow!

Remember, the more friends you refer, the more you earn. Happy trading!
    """

    return value
