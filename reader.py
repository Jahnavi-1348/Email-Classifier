import imaplib
import email
from email.header import decode_header
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def fetch_latest_emails(email_user, email_pass, limit=10):
    logging.info(f"Connecting to IMAP for user {email_user}")
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_user, email_pass)
        mail.select("inbox")

        status, messages = mail.search(None, "ALL")
        if status != "OK":
            raise Exception("Failed to retrieve emails")

        email_ids = messages[0].split()[-limit:]
        emails = []

        for eid in email_ids:
            status, msg_data = mail.fetch(eid, "(RFC822)")
            if status != "OK":
                logging.warning(f"Failed to fetch email id {eid}")
                continue

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg.get("Subject", ""))[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding or "utf-8", errors="ignore")

                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            ctype = part.get_content_type()
                            disp = str(part.get("Content-Disposition"))
                            if ctype == "text/plain" and "attachment" not in disp:
                                body = part.get_payload(decode=True).decode(errors="ignore")
                                break
                            elif ctype == "text/html" and "attachment" not in disp:
                                html_body = part.get_payload(decode=True).decode(errors="ignore")
                                body = BeautifulSoup(html_body, "html.parser").get_text()
                                break
                    else:
                        body = msg.get_payload(decode=True).decode(errors="ignore")

                    full_text = (subject + " " + body).strip()
                    emails.append({"subject": subject, "text": full_text})
        mail.logout()
        logging.info(f"Fetched {len(emails)} emails successfully.")
        return emails

    except imaplib.IMAP4.error as e:
        logging.error(f"IMAP error: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error fetching emails: {e}")
        raise

