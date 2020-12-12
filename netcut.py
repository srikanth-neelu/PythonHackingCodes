import netfilterqueue as nf
import scapy.all as scapy

def process_packet(packet):
    # scapy_packet=scapy.IP(packet.get_payload())
    # if scapy_packet.haslayer(scapy.DNS):
    #     print(scapy_packet[scapy.DNSQR].qname)
    # packet.set_payload(bytes(scapy_packet))
    packet.accept()#forward the packets to gateway so the website can load in victims computer
    # packet.drop()#these function drops every packet it recieves and cut internet connection


queue=nf.NetfilterQueue()
queue.bind(0,process_packet)#these method is used to combine the queue i.e nfqueue with queue object of netfilterqueue
queue.run()#these function start executing the queue functionality
