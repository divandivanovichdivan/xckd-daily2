import requests
import os
import argparse
import telegram
from dotenv import load_dotenv
import random


def download_image(url, path, file_name):
    response = requests.get(url)
    response.raise_for_status()
    with open(os.path.join(path, file_name), "wb") as out:
        out.write(response.content)


def publish_photo_to_tg(image_name, telegram_token, chat_id, path, text):
    bot = telegram.Bot(token=telegram_token)
    with open(os.path.join(path, image_name), 'rb') as file:
        bot.send_photo(chat_id=chat_id, photo=file, caption=text)


def get_img_quantity():
    json_response = requests.get(f"https://xkcd.com/info.0.json")
    json_response.raise_for_status()
    response = json_response.json()
    return response["num"]


def main():
    load_dotenv()
    telegram_token = os.environ["TG_TOKEN"]
    chat_id = os.environ["TG_CHAT_ID"]
    path = "images"
    img_quantity = get_img_quantity()
    img_number = random.randint(0, img_quantity)
    response = requests.get(f"https://xkcd.com/{img_number}/info.0.json")
    response.raise_for_status()
    response = response.json()
    img_url = response["img"]
    img_note = response["alt"]
    try:
        os.makedirs(path, exist_ok=True)
        download_image(img_url, path, f"{img_number}.png")
        publish_photo_to_tg(f"{img_number}.png", telegram_token, chat_id, path, img_note)
    finally:
        os.remove(os.path.join(path, f"{img_number}.png"))


if __name__ == '__main__':
    main()
