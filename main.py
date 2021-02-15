import requests
import wikipedia
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
import schedule
import time

def getRandWikiArticle():
    page = requests.get("https://en.wikipedia.org/wiki/Special:Random")
    soup = BeautifulSoup(page.content, "html.parser")
    articleName = soup.find(class_ = "firstHeading").text

    return articleName

def generateArticleLink(articleName):
    urlArticleName = "_".join(articleName.split())

    return f"https://en.wikipedia.org/wiki/{urlArticleName}"

def getArticleSummary(articleName):
    summary = wikipedia.summary(articleName)

    return summary

def generateMessage(articleName, articleUrl, summary):

    message = f"""\
    Subject: Random Fact of the Day

    Article Title: {articleName.encode('utf-8')}

    Hi User,

    {summary.encode('utf-8')}

    Find out more at {articleUrl.encode('utf-8')} 

    See you tommorow!

    Random Fact Bot

    """

    return message

def sendEmail(sender, reciever, message):
    EMAIL_ADDR = "tanishtesting@gmail.com"
    EMAIL_PSWRD = "Staticbird18#"

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_ADDR, EMAIL_PSWRD)

        smtp.sendmail(EMAIL_ADDR, EMAIL_ADDR, message)

def execute():
    sender = "tanishtesting@gmail.com"
    reciever = ["tanishtesting@gmail.com"]


    articleName = getRandWikiArticle()
    url = generateArticleLink(articleName)
    summary = getArticleSummary(articleName)
    message = generateMessage(articleName, url, summary)

    sendEmail(sender, reciever, message)


if __name__ == "__main__":
    schedule.every().day.at("10:30").do(execute)
    
    while True:
        schedule.run_pending()
        time.sleep(1)