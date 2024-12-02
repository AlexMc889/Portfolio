import requests
import ipaddress
import subprocess
iplist = open("listactiveips.txt")
iplist = iplist.read()
iplist = iplist.split("\n")


def checklocation(ip): 
    iprequest = requests.get(f'https://ipinfo.io/{i}')
    # initial request to scrap web contents
    ipinfo = iprequest.text
# function to check location
    try:
        indexofcountry = ipinfo.index("country")
    except: 
        return "This is a local or unknown address"
    linewithcountry = ipinfo[indexofcountry+11:]
    indexofparenth = linewithcountry.index('"')
# finding indexes to parse out country 
    country =linewithcountry[:indexofparenth]
    return country


def checktornodes(ip):
# function to check if IP is a tornode
    requestornodes = requests.get("https://raw.githubusercontent.com/7c/torfilter/refs/heads/main/lists/txt/torfilter-12h-flat.txt")
# function that requests IPs known as tor nodes from last 12 hours
    tornodes = requestornodes.text
    if ip in tornodes:
        return "True"
    else:
        return "False"


def checkVPN(ip): 
# check if IP is a VPN
    requestvpnsubnets = requests.get("https://raw.githubusercontent.com/X4BNet/lists_vpn/refs/heads/main/ipv4.txt")
# list of subnets that are associated with VPNs
    vpnsubnets = requestvpnsubnets.text
    lastdotindex = ip.rfind('.')
    cutip = ip[:lastdotindex+1]
    newip = cutip + '0'
# parse IP to check for subnets and not individual IPs
    if newip in vpnsubnets:
        return "True"
    else:
        return "False"

def is_bogon(ip):
    try:
       
        ip_obj = ipaddress.ip_address(ip)
        
      
        if ip_obj.is_private:
            return True 
        elif ip_obj.is_loopback:
            return True  
        elif ip_obj.is_link_local:
            return True
        elif ip_obj.is_multicast:
            return True 
        elif ip_obj.is_reserved:
            return True  
        elif ip_obj == ipaddress.IPv4Address('0.0.0.0'):
            return True
        else:
            return False
    except ValueError:
        # If the IP address is not valid, return False
        print(f"{ip} is not a valid IP address.")
        return False

def repcheck(ip): 
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
    headers = {
        "accept": "application/json",
        "x-apikey": "5e716cfcf41e2b837a1ffaa2077f051af5f94a0cf40dc469b31ed524840de6ea"
        # Enter your own virustotal API key
    }
# request virus total scan using API key
    response = requests.get(url,headers=headers)
    rep = response.text
    indexofmal = rep.index('stats": {"malicious":')
    repscore = rep[indexofmal+22]
# parse out malicious detection count
    return repscore
iplist.pop(0)
iplist.pop()
for i in iplist:
    if is_bogon(i) == True: 
        print(f'{i} is a local IP address')
    elif is_bogon(i) == False:
        print(f"Now checking {i}")
        print(f"Country of origin: {checklocation(i)}")
        print(f"Is a tor node: {checktornodes(i)}")
        print(f"Is a VPN: {checkVPN(i)}")
        print(f"VirtusTotal reputation score: {repcheck(i)}")

