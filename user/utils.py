import email
from django.db import models
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import smtplib,ssl
from email.message import EmailMessage


class SoftDeleteManager(models.Manager):
	''' Use this manager to get objects that have a isDeleted field '''
	def get_queryset(self):
		return super(SoftDeleteManager, self).get_queryset().filter(is_deleted=False)
	def all_with_deleted(self):
		return super(SoftDeleteManager, self).get_queryset()
	def deleted_set(self):
		return super(SoftDeleteManager, self).get_queryset().filter(is_deleted=True)

from django.core.mail import EmailMessage
class Util:
	@staticmethod
	def send_email(data):
		email = EmailMessage(subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
		email.send()

		# msg['Subject'] = data['email_subject']
		# msg['From'] = "naresh11021@gmail.com" 
		# msg['To'] = data['to_email']
		# msg.set_content(data['email_body'])
		# # s = smtplib.SMTP('587') 
		# s=smtplib.SMTP('smtp.gmail.com',587)
		# s.starttls()
		# s.login("naresh11021@gmail.com","7026677055")
		# s.sendmail("naresh11021@gmail.com", msg['To'], msg.as_string())
	



# '''
# 	def send_email(data):
# 		email = EmailMessage(
# 			subject = data['email_subject'],body=data['email_body'], to=[data['to_email']])
# 		email.send()
# 	'''


