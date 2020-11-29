    # creating a network scanner to get mac address of the devices in the same network
    import scapy.all as scapy
    import optparse as op
     
    parser = op.OptionParser()
    parser.add_option("-t","--target", dest="target_ip_range", help="set the range of the ip's")
    options = parser.parse_args()[0]
     
    target_ips = options.target_ip_range
     
     
     
    def targetclients(targets):
        print("IP\t\t\tMAC ADDRESS\n----------------------------------------------------------")
        for clients in targets:
            print(clients["ip"]+"\t\t"+clients["mac"])
     
     
     
    def scan(ip):
        # arp=scapy.arping(ip)
        arp_request=scapy.ARP(pdst=ip)
        # print(arp_request.summary())
        broadcast=scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
        # print(broadcast.summary())
        # scapy.ls(scapy.Ether())
        arp_broadcast_request=broadcast/arp_request
        # arp_broadcast_request=arp_request/broadcast ##these will not work
        # print(arp_broadcast_request.summary())
        # print(arp_broadcast_request.show())
        answered_list=scapy.srp(arp_broadcast_request,timeout=1,verbose=False)[0]
     
        target_client_list=[]
     
        # print("IP\t\t\tMAC ADDRESS\n----------------------------------------------------------")
        # print(answered_list.summary())
        # print(answered_list.show())
        for element in answered_list:
            # print(element[1].show()) to see the fields of the element[1] object so that it can be accessed
            # print(element[1].psrc + "\t\t" + element[1].hwsrc) #accessing the fields using dot of the the element[1] object
            # print("----------------------------------------------------------")
            target_client_dict={"ip":element[1].psrc,"mac":element[1].hwsrc}
            target_client_list.append(target_client_dict)
        return target_client_list
     
    clients_list_found=scan(target_ips)
    targetclients(clients_list_found)
