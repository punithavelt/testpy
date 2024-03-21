import sys
import email
import imaplib
from email.header import decode_header

# Email settings test
EMAIL = 'tech@thestagings.com'
PASSWORD = 'v52V9f4cD'
IMAP_SERVER = 'imap.marissa.metanet.ch'

SPECIFIC_SUBJECT = ''

def get_subjects():
    # Connect to the mail server
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select('inbox')

    # Search for emails with a specific subject
    #result, data = mail.search(None, '(SUBJECT "test mail")')
    
    search_criteria = '(FROM "{}" SUBJECT "{}")'
    #result, data = mail.search(None, '(SUBJECT "{}")'.format(SPECIFIC_SUBJECT))
    # result, data = mail.search(None, '(FROM "{}" SUBJECT "{}")'.format(SPECIFIC_RECEIVER, SPECIFIC_SUBJECT))
    result, data = mail.search(None, '(UNSEEN FROM "{}")'.format(SPECIFIC_RECEIVER))
    subjects = []
    
    if result == 'OK':
         for num in data[0].split():
            # Fetch the email with the specified ID
            _, messages = mail.fetch(num, '(RFC822)')
            # Parse the email message
            msg = email.message_from_bytes(messages[0][1])
            # Check if the email contains the specific text in the body
          #  if SPECIFIC_TEXT in msg.get_payload():
            subtext = msg.get('Subject')
             
            if SPECIFIC_SUBJECT in subtext:
              return 'OK'
            if REJECT_SUBJECT in subtext:
              return 'REJECT'
            try:
                subject = decode_header(messages[0][1].decode('utf-8'))[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode('utf-8')
                subjects.append(subject)
                
            except Exception as e:
                print(f"ERROR")
    mail.close()
    mail.logout()
    return 'LOOP'

 
if __name__ == "__main__":
   if len(sys.argv) != 3:
       print(sys.argv)
       print("Usage: python validate_email <subject> <receiver_email>")
       sys.exit(1)
    
   SPECIFIC_SUBJECT = "Approved test-pipeline 140 BUILD"
   SPECIFIC_RECEIVER = "punithavel@thestagings.com"
   SPECIFIC_SUBJECT = sys.argv[1]
   SPECIFIC_RECEIVER = sys.argv[2]
   REPLY_SUBJECT = sys.argv[1]
   print(sys.argv)
   
