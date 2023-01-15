import requests

def send_simple_message():
    	return requests.post(
		"https://api.mailgun.net/v3/sandbox6b8a4c9313d6403e931ebc7ece91e40f.mailgun.org/messages",
		auth=("api", "389ee4059b667aeab8c5405a3c7d86fb-4c2b2223-3bbc6a59"),
		data={"from": "Mailgun Sandbox <postmaster@sandbox6b8a4c9313d6403e931ebc7ece91e40f.mailgun.org>",
			"to": "Vinay Kumar <vinaykumar.main@gmail.com>",
			"subject": "Hello Vinay Kumar",
			"text": "Congratulations Vinay Kumar, you just sent an email with Mailgun!  You are truly awesome!"})

send_simple_message()