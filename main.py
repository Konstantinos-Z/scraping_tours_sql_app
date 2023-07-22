import requests
import selectorlib
import smtplib, ssl
from email.message import EmailMessage
import os
import time

URL = "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def scrape(url):
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def send_email(tour_info):
    host = "smtp.gmail.com"
    port = 465

    password = os.getenv("scraping_tours_sql_pass")

    msg = EmailMessage()
    msg["Subject"] = "New tour"
    msg["From"] = "zigouris.konstantinos@gmail.com"
    msg["To"] = "zigouris.konstantinos@gmail.com"
    msg.set_content(f"Hey, new tour available: {tour_info}")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login("zigouris.konstantinos@gmail.com", password)
        server.send_message(msg)
    print("Email was sent!")


def store(extracted):
    with open("data.txt", 'a') as file:
        file.write(extracted + "\n")


def read(extracted):
    with open("data.txt", 'r') as file:
        return file.read()


if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)
        content = read(extracted)
        if extracted != "No upcoming tours":
            if extracted not in content:
                store(extracted)
                send_email(extracted)
        time.sleep(3600)
