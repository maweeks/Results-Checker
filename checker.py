from twilio.rest import TwilioRestClient
import requests
import smtplib
import subprocess
import time
import urllib

from email.mime.text import MIMEText
from datetime import date
import smtplib

login_user = ''
login_pass = ''
message_email = ''
message_number_from = ''
message_number_to = ''

account_sid = ""
auth_token  = ""


login_user = 'mjw59'
login_pass = 'University332211'
message_email = 'matt.weeks93@gmail.com'
message_email_password = 'J6w-7S4-VR6-BV7'
message_number_from = '+441613751697'
message_number_to = '+447515772568'

account_sid = "AC267641869b15bc21014a23663fd9ff49"
auth_token  = "de6c9f1d79439f714d0b7979a4aa8f1b"


check_result = True
check_count = 12
total_checks = 0

client = TwilioRestClient(account_sid, auth_token)


def check_site():
	# log in to web site
	r = requests.get('https://results.kent.ac.uk', auth=(login_user, login_pass))

	# if site contains x
	if ("Sorry, your result is not available at this time. Please try again later." in r.text):

		# print results not up
		global check_count, total_checks
		print "Results are not up, time is {} checks: {} total_checks: {}".format(time.ctime(), check_count, total_checks)

		check_count = check_count + 1
		total_checks = total_checks + 1

		# send messages every 6 hours
		# if (check_count >= 3):
		if (check_count >= 12):

			# send message
			send_messages("System is still running.", "UoK Checking")
			check_count = 0

	# else
	else:
		print "RESULTS ARE OUT, GOOD LUCK!! Time is "+time.ctime()

		# send message
		send_messages("Hey, results might be out. Good luck!", "UoK Results")
		global check_result
		check_result = False


def send_messages(message, subject):
	print message
	print subject

	# sent text
	send_text(message)

	# send email
	send_email(message, subject)


def send_text(message):
	message = client.messages.create(
		body=message,
		to=message_number_to,    # Replace with your phone number
		from_=message_number_from) # Replace with your Twilio number
	print "Text ID:"+message.sid


def send_email(message, subject):
	SMTP_SERVER = "smtp.gmail.com"
	SMTP_PORT = 587
	SMTP_USERNAME = message_email
	SMTP_PASSWORD = message_email_password

	EMAIL_TO = [message_email]
	EMAIL_FROM = message_email
	EMAIL_SUBJECT = subject

	DATE_FORMAT = "%d/%m/%Y"
	EMAIL_SPACE = ", "

	DATA=message


	msg = MIMEText(DATA)
	msg['Subject'] = EMAIL_SUBJECT
	msg['To'] = EMAIL_SPACE.join(EMAIL_TO)
	msg['From'] = EMAIL_FROM
	mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
	mail.ehlo()
	mail.starttls()
	mail.login(SMTP_USERNAME, SMTP_PASSWORD)
	mail.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
	mail.quit()

while (check_result is True):
	check_site()
	# time.sleep(3)
	time.sleep(300)