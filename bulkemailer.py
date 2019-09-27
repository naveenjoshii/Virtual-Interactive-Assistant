import smtplib
import openpyxl as xl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

username = str(input('Your Username:' ))
password = str(input('Your Password:' ))
From = username
Subject = 'Test'

wb = xl.load_workbook(r'C:\Users\skt\Documents\emailer.xlsx')
sheet1 = wb.get_sheet_by_name('Sheet1')

names = []
emails = []

for cell in sheet1['A']:
    emails.append(cell.value)

for cell in sheet1['B']:
    names.append(cell.value)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(username, password)

for i in range(len(emails)):
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = names[i]
    msg['Subject'] = Subject
    text = '''
Hello {},
    This is bulk mailing test!
'''.format(names[i])
    msg.attach(MIMEText(text, 'plain'))
    message = msg.as_string()
    server.sendmail(username, emails[i], message)
    print('Mail sent to', emails[i])

server.quit()
print('All emails sent successfully!')
