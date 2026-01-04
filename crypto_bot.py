import requests
import time

# ================= CONFIG =================
BOT_TOKEN = "PASTE_YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "PASTE_YOUR_CHAT_ID"
CMC_API_KEY = "PASTE_YOUR_CMC_API_KEY"

CMC_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"
# =========================================


def get_top_10_prices():
    headers = {
        "X-CMC_PRO_API_KEY": CMC_API_KEY
    }
    params = {
        "start": 1,
        "limit": 10,
        "convert": "USD"
    }

    response = requests.get(CMC_URL, headers=headers, params=params)
    data = response.json()

    message = "📊 *Top 10 Cryptocurrencies (Live)*\n\n"

    for coin in data["data"]:
        name = coin["name"]
        symbol = coin["symbol"]
        price = coin["quote"]["USD"]["price"]
        message += f"• {name} ({symbol}): ${price:,.2f}\n"

    return message


def send_message(text):
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(f"{TELEGRAM_API}/sendMessage", json=payload)


def get_updates(offset=None):
    params = {"timeout": 100, "offset": offset}
    response = requests.get(f"{TELEGRAM_API}/getUpdates", params=params)
    return response.json()


def main():
    send_message("🤖 Crypto Bot is online!\n\nCommands:\n/prices – Get top 10 crypto prices")

    last_update_id = None

    while True:
        updates = get_updates(last_update_id)

        for update in updates["result"]:
            last_update_id = update["update_id"] + 1

            if "message" not in update:
                continue

            text = update["message"].get("text", "")

            if text == "/start":
                send_message("✅ Bot is running.\nUse /prices to get live prices.")

            elif text == "/prices":
                prices = get_top_10_prices()
                send_message(prices)

        time.sleep(1)


if __name__ == "__main__":
    main()
