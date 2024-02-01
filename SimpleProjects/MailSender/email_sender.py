import os
err_msg = "Something went wrong"
sender_email = "msp.intern5@market-securities.com"
receiver_email = "frederic.miekisiak@market-securities.com"
smtp_server = "mail.market-securities.com"
import smtplib, ssl
port = 587 
password = input("Type your password and press enter:")
subject = input('Subject:')
body = input ('What is your message?')

message = """\
subject:{}

{}
This message is sent from Python.""".format(subject,body)

context = ssl.create_default_context()
try:
    smtp = smtplib.SMTP('mail.market-securities.com')
    #smtp.connect()
    #smtp.login('msp.system','xxxxx')
    print( "Sent")
    smtp.sendmail(sender_email,receiver_email,message)
    smtp.close()
    #with smtplib.SMTP(smtp_server) as server:
    #    server.ehlo()  # Can be omitted
    #    server.starttls(context=context)
    #   server.ehlo()  # Can be omitted
    #  server.login(sender_email, password)
    #  server.sendmail(sender_email, receiver_email, message)
    #  server.quit()
except Exception as e:
    # Print any error messages to stdout
    print(e)
    print(err_msg)
