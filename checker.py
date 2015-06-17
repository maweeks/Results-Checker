from twilio.rest import TwilioRestClient
import requests
import smtplib
import time
import urllib


login_user = ''
login_pass = ''
message_email = ''
message_number_from = ''
message_number_to = ''

account_sid = ""
auth_token  = ""


check_result = True
check_count = 0
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
		if (check_count >= 3):
		# if (check_count >= 72):

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
	# send email
	send_email(message, subject)

	# sent text
	send_text(message)


def send_text(message):
	message = client.messages.create(
		body=message,
	    to=message_number_to,    # Replace with your phone number
	    from_=message_number_from) # Replace with your Twilio number
	print "Text ID:"+message.sid


def send_email(message, subject):
	print "Email coming soon..."


while (check_result is True):
	check_site()
	time.sleep(3)
	# time.sleep(300)