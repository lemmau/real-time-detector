import os
import json
import smtplib, ssl
import base64
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename

class SendMail():

	def __init__(self):
		config = os.path.abspath(os.getcwd()) + '/config/config.json'

		with open(config) as file:
			configFile = json.load(file)
			
		self.config = configFile
		self.context = ssl.create_default_context()
		self.smtpServer = configFile['email']['smptServer']
		self.smtpPort = configFile['email']['smptPort']

		self.server = smtplib.SMTP(self.smtpServer,self.smtpPort)

	def login(self):
		self.mailSender = self.config['email']['senderMail']

		self.server.ehlo()
		self.server.starttls(context=self.context)
		self.server.ehlo()
		decryptedPassword = base64.b64decode(self.config['email']['senderPassword']).decode('utf-8')
		self.server.login(self.mailSender, decryptedPassword)

	def send(self, listMails: list, subject: str, message: str, attachments: list):
		msg = MIMEMultipart()
		msg['From'] = self.mailSender
		msg['To'] = ",".join(listMails)
		msg['Subject'] = subject

		msg.attach(MIMEText(message))

		for file in attachments:
			with open(file, "rb") as openFile:
				part = MIMEApplication(openFile.read(), Name=basename(file))
	        
			part['Content-Disposition'] = 'attachment; filename="{fileName}"'.format(fileName=basename(file))
			msg.attach(part)

		self.server.sendmail(self.mailSender, listMails, msg.as_string())

	@staticmethod
	def sendMailTo(listMails: list, subject: str, message: str, attachments=[]):
		mailer = SendMail()
		mailer.login()
		mailer.send(listMails, subject, message, attachments)
		print('Email sent')
