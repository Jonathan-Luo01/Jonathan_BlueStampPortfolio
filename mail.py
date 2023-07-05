#import libraries
import smtplib
from email.mime.Multipart import MIMEMultipart
from email.mime.Text import MIMEText
from email.mime.base import MIMEBase
from email.mime.Image import MIMEImage
from email.mime.application import MIMEApplication
from email import encoders

# Email you want to send the update from (only works with gmail)
fromEmail = 'email@gmail.com'
# You have to generate an app password since Gmail does not allow less secure apps anymore
# https://support.google.com/accounts/answer/185833?hl=en
fromEmailPassword = 'password'

# Email you want to send the update to
toEmail = 'email2@gmail.com'

def sendEmail(image):
  video_file = MIMEBase('application', 'octet-stream')
  video_file.set_payload(open('output.avi', 'rb').read()) #read from file

  encoders.encode_base64(video_file)
  video_file.add_header('Content-Disposition', 'attachment: filename = {}'.format("output.avi")) #add a header
  
	msgRoot = MIMEMultipart('related')
	msgRoot['Subject'] = 'Security Update'
	msgRoot['From'] = fromEmail
	msgRoot['To'] = toEmail
	msgRoot.preamble = 'Raspberry pi security camera update'

	msgAlternative = MIMEMultipart('alternative')
	msgRoot.attach(msgAlternative)
	msgText = MIMEText('Smart security cam found object') #add description
	msgAlternative.attach(msgText) 

	msgText = MIMEText('<img src="cid:image1">', 'html')
	msgAlternative.attach(msgText)

	msgImage = MIMEImage(image)
	msgImage.add_header('Content-ID', '<image1>')
	msgRoot.attach(msgImage) #add the image taken 
  msgRoot.attach(video_file)

	smtp = smtplib.SMTP('smtp.gmail.com', 587)
	smtp.starttls()
	smtp.login(fromEmail, fromEmailPassword) #access gmail
	smtp.sendmail(fromEmail, toEmail, msgRoot.as_string())
	smtp.quit()
