import requests
import ipaddress
givenip = input('What IP would you like to check? ')
api = input('Enter your VirusTotal API key: ')

def checklocation(ip): 
    iprequest = requests.get(f'https://ipinfo.io/{givenip}')
    # initial request to scrap web contents
    ipinfo = iprequest.text
# function to check location
    indexofcountry = ipinfo.index("country")
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


def repcheck(ip): 
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
    headers = {
        "accept": "application/json",
        "x-apikey": f"{api}"
        # Enter your own virustotal API key
    }
# request virus total scan using API key
    response = requests.get(url,headers=headers)
    rep = response.text
    indexofmal = rep.index('stats": {"malicious":')
    repscore = rep[indexofmal+22]
# parse out malicious detection count
    return repscore

print(f"Country of origin: {checklocation(givenip)}")
print(f"Is a tor node: {checktornodes(givenip)}")
print(f"Is a VPN: {checkVPN(givenip)}")
print(f"VirtusTotal reputation score: {repcheck(givenip)}")

