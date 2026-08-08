import os
import smtplib
from email.message import EmailMessage
import requests
from dotenv import load_dotenv

load_dotenv()
# 1. Preluăm cursul valutar gratuit
url="https://open.er-api.com/v6/latest/EUR"
response=requests.get(url)
data=response.json()

eur_to_ron=data['rates']['RON']
# 2. Pregatim mesajul
msg=EmailMessage()
print(msg)
msg['Subject']=f'Curs Valutar azi: 1 EUR={eur_to_ron:.4f} RON'
msg['From']=os.environ.get('EMAIL_USER')
msg['To']=os.environ.get('EMAIL_USER')
msg.set_content(f'Azi,1 EUR este echivalent cu {eur_to_ron:.4f} RON')

# 3. Trimitem e-mailul
try:
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
        smtp.login(os.environ.get('EMAIL_USER'),os.environ.get('EMAIL_PASS'))
        smtp.send_message(msg)
    print("email trimis cu succes")
except Exception as e:
    print(f'a aparut o eroare la trimitere:{e}')
