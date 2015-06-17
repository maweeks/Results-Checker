from twilio.rest import TwilioRestClient
import requests
import smtplib
import subprocess
import time
import urllib

from email.mime.text import MIMEText
from datetime import date
import smtplib

import config

account_sid = config.c_account_sid
auth_token  = config.c_auth_token
login_user = config.c_login_user
login_pass = config.c_login_pass
message_email = config.c_message_email
message_email_password = config.c_message_email_password
message_number_from = config.c_message_number_from
message_number_to = config.c_message_number_to
success_subject = config.c_success_subject
system_run_count = config.c_system_run_count
time_sleep = config.c_time_sleep

check_result = True
check_count = config.c_system_run_count # to send email on first check, set to 0 if unwanted
total_checks = -1

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
		if (check_count >= system_run_count):

			# send message
			send_messages("System is still running.", "", "UoK Checking")
			check_count = 0

	# else
	else:
		print "RESULTS ARE OUT, GOOD LUCK!! Time is "+time.ctime()

		# send message
		send_messages("Hey, results might be out. Good luck!", r.text, success_subject)

		print r.text

		global check_result
		check_result = False


def send_messages(message, page, subject):
	print message
	print subject

	# sent text
	send_text(message)

	# send email
	send_email(message+" "+page, subject)


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
	time.sleep(config.c_time_sleep)