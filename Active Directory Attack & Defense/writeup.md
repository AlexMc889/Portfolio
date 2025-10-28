# Active Directory Attack & Defense

The objective of this project is to learn how to execute and detect common attacks in a typical AD setup. We will be using tools such as Mimikatz, Bloodhound, Sharphound, and Rubeus for our attacks. We will detecting attacks using Sysmon and Event Logs all forwarded to Splunk. 

## Network Diagram 
![diagram](https://github.com/AlexMc889/Portfolio/blob/main/Active%20Directory%20Attack%20%26%20Defense/Images/Setup/AD%20setup.png)

Using AWS we will deploy a domain controller, a windows server, and a splunk server in a private subnet. 

A bastion host is deployed in a public subnet for access to our domain controller from outside the VPC. 

A NAT gateway will allow the private subnet to access the internet for updates.

## Attack and Detection Write Ups 
[Kerberoasting](https://github.com/AlexMc889/Portfolio/blob/main/Active%20Directory%20Attack%20%26%20Defense/Images/kerberoast/kerberoast%20writeup)
[Pass The Hash](https://github.com/AlexMc889/Portfolio/blob/main/Active%20Directory%20Attack%20%26%20Defense/Images/pass%20the%20hash/pass%20the%20hash%20writeup.md)
[Golden Ticket](https://github.com/AlexMc889/Portfolio/blob/main/Active%20Directory%20Attack%20%26%20Defense/Images/golden%20ticket/golden%20ticket%20writeup.md)
[Bloodhound Mapping](https://github.com/AlexMc889/Portfolio/blob/main/Active%20Directory%20Attack%20%26%20Defense/Images/Bloodhound/bloodhound%20writeup.md)
