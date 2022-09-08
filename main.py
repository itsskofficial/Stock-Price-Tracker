import requests
import datetime
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "tesla"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_KEY = "JAQE3711NMRDGSZ0"
NEWS_KEY = "73e578b61013435695c39c8fe69cef04"
SMS_SID = "ACa0989588c68a49c8a2751da99be3c2b1"
SMS_TOKEN = "5f60f7bd753f783480ac00129cb173a6"
SMS_SENDER = "+19594568893"
SMS_RECEIVER = "+918408849900"
YESTERDAY = datetime.date.today() - datetime.timedelta(days=1)
DAYBFRYES = datetime.date.today() - datetime.timedelta(days=2)

stock_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK_NAME}&apikey={STOCK_KEY}"
req1 = requests.get(stock_url)
data1 = req1.json()

close1 = float(data1["Time Series (Daily)"][f"{YESTERDAY}"]["4. close"])
close2 = float(data1["Time Series (Daily)"][f"{DAYBFRYES}"]["4. close"])
diff = round(close1 - close2, 2)

if diff<0:
    arrow="down"
else:
    arrow="up"
percent_diff = round((abs(diff) / close1) * 100, 2)
if percent_diff > 5:
    news_url = f"https://newsapi.org/v2/top-headlines?q={COMPANY_NAME}&apiKey={NEWS_KEY}"
    req2 = requests.get(news_url)
    data2 = req2.json()
    descriptons = [i["description"] for i in data2["articles"]]
    titles = [i["title"] for i in data2["articles"]]
    news=[[titles[i],descriptons[i]] for i in range(len(titles))]
    client = Client(SMS_SID,SMS_TOKEN)

    for i in (news):
        if arrow=="up":
            message = message = client.messages.create(
                    body=f"{STOCK_NAME}: 🔻 {percent_diff} %\nHeadline: {i[0]}\nDescription: {i[1]}", from_="+19594568893", to="+918408849900"
                )
        else:
            message = message = client.messages.create(
                    body=f"{STOCK_NAME}: 🔺 {percent_diff} %\nHeadline: {i[0]}\nDescription: {i[1]}", from_="+19594568893", to="+918408849900"
                )


