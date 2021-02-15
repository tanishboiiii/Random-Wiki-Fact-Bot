import requests
from bs4 import BeautifulSoup
import wikipedia
import smtplib
import time
import schedule


#function to get random article name using wikipedia's special:random link
def getRandArticleName(): 
    page = requests.get("https://en.wikipedia.org/wiki/Special:Random")
    soup = BeautifulSoup(page.content, "html.parser")
    articleName = soup.find(class_ = "firstHeading").text

    return articleName


#generating article url based on article name
def getArticleUrl(articleName):
    urlArticleName = "_".join(articleName.split(" "))
    url = f"https://en.wikipedia.org/wiki/{urlArticleName}"

    return url


#getting article summary using wikipedia api and article name
def getSummary(articleName):
    summary = wikipedia.summary(articleName)

    return summary


#generating email message template
def generateMessage(articleName, articleURL, summary):

    message = f"""
    Subject: Random Fact of the Day
    
    Article Name: {articleName.encode("utf-8")}

    Hi User,

    {summary.encode("utf-8")}

    Find out more at: {articleURL.encode("utf-8")}

    See You Tommorrow!

    Random Fact Bot
    """

    return message


#sending email
def sendEmail(message):
    EMAIL_ADDR = "" #email goes here
    PSWRD = "" #password goes here

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp: #starting connection with gmail server
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_ADDR, PSWRD) #logging ito gmail account with credentials

        smtp.sendmail(EMAIL_ADDR, EMAIL_ADDR, message) #sending email with message


def execute(): #execute function that ties together all the functions above
    articleName = getRandArticleName() #and sends email based on information generated
    articleURL = getArticleUrl(articleName)
    summary = getSummary(articleName)
    message = generateMessage(articleName, articleURL, summary)

    sendEmail(message)



if __name__ == "__main__":
    schedule.every().day.at("7:30").do(execute) #setting up scheduler

    while True: 
        schedule.run_pending() #run pending tasks
        time.sleep(1)