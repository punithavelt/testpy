import imaplib
from email.header import decode_header
from jenkinsapi.jenkins import Jenkins

# Email settings
EMAIL = 'tech@thestagings.com'
PASSWORD = 'v52V9f4cD'
IMAP_SERVER = 'imap.marissa.metanet.ch'

# Jenkins settings
JENKINS_URL = 'http://www1.jenkins.com:32769/'
JENKINS_USERNAME = 'admin'
JENKINS_PASSWORD = 'admin@123'
SPECIFIC_SUBJECT = 'Approval Granted test-pipeline'

def get_subjects():
    # Connect to the mail server
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select('inbox')

    # Search for emails with a specific subject
    #result, data = mail.search(None, '(SUBJECT "test mail")')
    result, data = mail.search(None, '(UNSEEN SUBJECT "{}")'.format(SPECIFIC_SUBJECT))
    subjects = []

    if result == 'OK':
        for num in data[0].split():
            result, raw_email = mail.fetch(num, '(RFC822)')
            if result == 'OK':
                try:
                    subject = decode_header(raw_email[0][1].decode('utf-8'))[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode('utf-8')
                    subjects.append(subject)
                except Exception as e:
                    print(f"Error decoding subject: {e}")

    mail.close()
    mail.logout()
    return subjects

 
if __name__ == "__main__":
    subjects = get_subjects()
    if subjects:
      print('OK')
       
    else:
        print('ERROR')
