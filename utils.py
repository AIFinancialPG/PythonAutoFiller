import yaml
import logging
import email
import aioimaplib
import asyncio

def load_credentials(filepath: str) -> tuple[str, str]:
    try:
        with open(filepath, 'r') as file:
            credentials = yaml.safe_load(file)
            user = credentials['user']
            password = credentials['password']
            print(user, password)
            return user, password
    except Exception as e:
        logging.error("Failed to load credentials: {}".format(e))
        raise

async def get_verification_mail() -> str:
    imap_client = aioimaplib.IMAP4_SSL(host='imap.gmail.com', timeout=30)
    await imap_client.wait_hello_from_server()

    await imap_client.login(*load_credentials("credentials.yaml"))
    await imap_client.select('INBOX')
    
    idle = await imap_client.idle_start(timeout=60)
    msg = await imap_client.wait_server_push()
    imap_client.idle_done()
    await asyncio.wait_for(idle, 30)

    print(msg, str(int(msg[0].split()[0])))
    _, data = await imap_client.fetch(str(int(msg[0].split()[0])), '(RFC822)')
    email_message = email.message_from_bytes(data[1])

    print(email_message.get_payload().split("Use verification code ")[1][0:6])

    await imap_client.logout()

    if email_message:
        return email_message.get_payload().split("Use verification code ")[1][0:6]
    return ""