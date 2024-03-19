import sys
import imaplib
from email.header import decode_header

# Email settings
EMAIL = 'tech@thestagings.com'
PASSWORD = 'v52V9f4cD'
IMAP_SERVER = 'imap.marissa.metanet.ch'

SPECIFIC_SUBJECT = ''

def validate_email(subject, receiver_email):
    return True
    

def get_subjects():
    # Connect to the mail server
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select('inbox')

    # Search for emails with a specific subject
    #result, data = mail.search(None, '(SUBJECT "test mail")')

    search_criteria = '(FROM "{}" SUBJECT "{}")'.format(SPECIFIC_RECEIVER, SPECIFIC_SUBJECT)
    result, data = mail.search(None, search_criteria)
    subjects = []

    if result == 'OK':
        for num in data[0].split():
            result, raw_email = mail.fetch(num, '(RFC822)')
            if result == 'OK':
                for num in messages[0].split():
                    # Fetch the email with the specified ID
                    _, data = mail.fetch(num, '(RFC822)')
                    # Parse the email message
                    msg = email.message_from_bytes(data[0][1])
                    # Check if the email contains the specific text in the body
                  #  if SPECIFIC_TEXT in msg.get_payload():
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
    if len(sys.argv) != 3:
        print("Usage: python validate_email <subject> <receiver_email>")
        sys.exit(1)
    SPECIFIC_SUBJECT = sys.argv[1]
    SPECIFIC_RECEIVER = sys.argv[2]
    subjects = get_subjects()
    valid = validate_email(SPECIFIC_SUBJECT, SPECIFIC_RECEIVER)
    if valid:
        if subjects:
            print(subjects)
        else:
            print('ERROR')
    else:
        print('ERROR')
