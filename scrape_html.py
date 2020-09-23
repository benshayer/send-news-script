from bs4 import BeautifulSoup
import requests
import os
import smtplib
from email.message import EmailMessage
import datetime
import schedule
import time

EMAIL_ADDRESS=os.environ.get('EMAIL_USER2')
EMAIL_PASSWORD=os.environ.get('EMAIL_PASS2')
def send_news():
	source = requests.get('https://www.jpost.com/Breaking-News').text

	tday=datetime.datetime.now()
	tdelta = datetime.timedelta(hours=12)

	soup=BeautifulSoup(source, 'lxml')
	breaking_news="""<!DOCTYPE html>
	<html>
	<head>
		<title></title>
	</head>
	<body>"""
	for news in soup.find_all('div', class_="breaking-news-link-container"):
		time=news.find_all('li')[1].text
		day=int(time.split(' ')[0].split('/')[1])
		month=int(time.split(' ')[0].split('/')[0])
		year=int(time.split(' ')[0].split('/')[2])
		if time.split(' ')[2]=='AM':
			if time.split(' ')[1].split(':')[0]=='12':
				hour=0
			else:
				hour=int(time.split(' ')[1].split(':')[0])
		elif time.split(' ')[1].split(':')[0]=='12':
			hour=12
		else:
			hour=int(time.split(' ')[1].split(':')[0])+12
		minute=int(time.split(' ')[1].split(':')[1])
		news_date=datetime.datetime(year, month, day,hour,minute)
		if tday <= news_date+tdelta:
			title = news.a.span.text
			link=link =news.a.get('href')
			breaking_news+="\n"+"""<a href="{link}">{title}</a>""".format(link=link,title=title)+"\n"
			#author=news.find_all('li')[0].text
			breaking_news+=str(news.find_all('li')[0])+"\n"
			breaking_news+=str(news.find_all('li')[1])

		#time=news.find_all('li')[1].text
		#print(time)
		#print()
	breaking_news+="\n"+"""</body>
	</html>

		"""
	#print(breaking_news)

	msg=EmailMessage()
	msg['Subject'] = 'Breaking News from the Jerusalem Post'
	msg['From'] = EMAIL_ADDRESS
	msg['To'] = 'shayerb5@gmail.com'
	msg.set_content('This is plain HTML news')

	msg.add_alternative(breaking_news, subtype='html')

	with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
		smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
		smtp.send_message(msg)

schedule.every().day.at('18:15').do(send_news)

while True:
	schedule.run_pending()
	time.sleep(60)