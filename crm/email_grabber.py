import email
import imaplib
from email.header import decode_header
from .models import emailInbox
from datetime  import datetime
EMAIL = 'austin@horizon-development.com'
PASSWORD = 'a$gF233hD9@n'
SERVER = 'mail.privateemail.com'
def get_inbox():
    mail = imaplib.IMAP4_SSL(SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select('inbox')
    status, data = mail.search(None, 'ALL')
    mail_ids = []

    email_list = []
    print(email_list)
    for block in data:
        mail_ids += block.split()
    for i in mail_ids:
        status, data = mail.fetch(i, '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                message = email.message_from_bytes(response_part[1])
                date = decode_header(message["Date"])[0][0]
                example = "Fri, 11 Mar 2022 19:23:45 +0000"
                # delete last 9 charicters of date
                date = date[:-9]
                # convert example to datetime object
                date = datetime.strptime(date, '%a, %d %b %Y %H:%M')

                mail_from = message['from']
                mail_subject = message['subject']
                if message.is_multipart():
                    mail_content = ''
                    for part in message.get_payload():
                        if part.get_content_type() == 'text/plain':
                            mail_content += part.get_payload()
                else:
                    mail_content = message.get_payload()
                if not emailInbox.objects.filter(subject=emailInbox.subject).exists():
                    # add to database
                    print(mail_subject)
                    new_email = emailInbox(
                        current_inbox="austin@horizon-development.com",
                        subject=mail_subject,
                        message=message,
                        sender= mail_from,
                        recieved_time= date,
                        is_read=False,
                    )
                    new_email.save()
                else:
                    pass
                
    return True