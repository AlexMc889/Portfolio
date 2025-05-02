# AWS Cloud Infrastructure Project

After obtaining my AWS Solutions Architect and Cloud Practitioner Certifications, I did this project to apply some of the concepts I learned in a hands-on way.  

## Network Diagram  
![VPC Layout](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/layout.drawio.png)

## Overview  
The goal of the project was to set up a secure, scalable, and available infrastructure to host a website and a Splunk server.  

Security will be implemented through segmenting each part of the network into its own subnet. Certain subnets will be private, and external access will only be provisioned through a bastion host. 

Security groups will also be configured for all EC2 instances.

Scalability and availability will be implemented by using an Application Load Balancer and an Auto Scaling Group.  

Lastly, our Splunk server will monitor our bastion host and any EC2 instance started by the ASG.  

## VPC Setup  
First, we must set up our subnets and then route tables for each subnet.  

![Subnets](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/subnets.png)
### Subnets  
- **10.0.1.0/24 & 10.0.5.0/24 (Public)** - These will be used by our Application Load Balancer as access to our website. AWS requires 2 subnets in 2 different AZs for an ALB, increasing availability.
- **10.0.3.0/24 (Public)** - This subnet will be for our NAT gateway, enabling our Splunk server and Apache EC2 instance to access the internet while still in a private subnet for patches/updates. Our bastion host will also be here for external acccess to our Splunk server.
- **10.0.4.0/24 (Private)** - This subnet will host our Splunk server in a private subnet, so it is not directly accessible on the internet.
- **10.0.2.0/24 (Private)** - This subnet will host our Apache Website EC2 instances in a ASG group behind our ALB. They will be in a private subnet, so they are only accessible through the ALB.
### Route Tables 
- We will need to configure route tables for each of these subnets.
- Public subnets will point towards a Internet Gateway and private subnets will point towards a NAT gateway
![Route Table 1](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/Public%20Route%20Table.png)
![Route Table 2](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/Public%20Route%20Table.png)
### ALB, ASG, and Launch Template Setup 
- To setup the ALB we must configure what AZs and subnets it will run on and give it a target group (Apache EC2 instances) and a listener to receive external connections.
- The Launch Template will be configured to launch a pre-configured AMI Ubuntu machine. Our AMI will be already connected to our splunk server so that all new EC2 instances are connected as well.
- In the ASG we will set max/min # of EC2 instances to scale up and what paremeter to scale on (we will use CPU usage).
![AZ/Subnet ASG](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/ALB%20setup.png)
![Listener](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/listener%20setup.png)
### Splunk Server Setup 
- After launching the EC2 instance in a private subnet, to connect to it we will use AWS Session Manager for a secure connection. To do this we will attach a IAM role to enable access.
![IAM Role](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/IAM%20role.png)
- Next we will install Splunk enterprise on it and allow data to be recieved on port 9997.
- We will also configure our security group, only allowing SSH from the bastion host, and allowing logs to be received from the bastion host and our Apache EC2 instances.
- We must also allow our bastion host to access the splunk webpage on port 8000.
![Splunk Security Group](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/splunksecuritygroup.png)
### Bastion Host Setup
- Our bastion host will allow us access to our splunk server outside of AWS. Although a Direct VPN into our VPC would be better, we will be using a bastion host.
- Since our bastion host is accessible to the internet, we will configure the security group to only allow our IP to SSH into it.
![Bastion Security Group](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/Bastion%20Security%20Group.png)
- We will also install a splunk forwarder on this machine, so we can monitor any activity on the EC2 instance.
![Splunk forwarder](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/splunk%20forwarder.png)
### Configuring SSH Tunnel to Splunk Server 
- To access our Splunk server from outside the VPC, we must SSH into the bastion host and then forward the Splunk webpage to our own machine.
- To do this we will use PuTTY.
- ![PuTTY Setup](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/PuTTY%20setup.png)
- Now from outside the VPC we can access our Splunk server.
![Splunk Logs](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/splunk%20logs.png)
### Monitoring Network for Attacks with Splunk
- Here we can see me attempting a directory brute force against the website.
![Splunk Directory Brute Force](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/Splunk%20bruteforce.png)
- We can see all SSH attempts into our Bastion Host to.
![SSH into Bastion Logs](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/SSH%20into%20bastion.png)
### Setting Up DNS Server
- We will also launch a internal DNS server so it is easier to resolve our machines.
- We will set this up on a Ubuntu server running BIND, with the following security group.
- ![Security Groups](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/DNS-security-group.png)
- We will setup the DNS server BIND config file
- ![DNS Server Config](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/DNS-server-config.png)
- We will define the zone
- ![Zone Files](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/defining-DNS-zone.png)
- Then we can defined the records for our web server and our bastion host.
- ![DNS Records](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/DNS-records.png)
- Now we can use the internal DNS server on our other devices.
 ![NSLookup Query](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/NSlookup.png)
### Using Ansible for Automation 
- We can use Ansible to automate and easily run a set of tasks for all of our machines.
- We will setup ansible on our splunk server and have it run a script to automatically update & upgrade our machines, and retrieve syslog from all the machines.
- First we installed ansible and setup our hosts and ansible.cfg file
- ![Ansible Script](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/ansible%20script.png)
- The results of running the script:
![Ansible Result](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/runningansible%20script.png)
- As we can see the DNS server needed to be updated, and all syslog files were retrieved.
## Deploying AD Environment
- Now in another private subnet we will deploy a domain controller and a windows server
- First we must setup a SSH tunnel through the bastion host to access the server, because it is in a private subnet
![SSH Tunnel](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/sshtunnel.png)
- Now we can RDP into the Domain Controller
- First we must setup the IP address and the DNS server of the domain controller.
- The DNS server will be itself (127.0.0.1)
![DNS](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/configuring%20dns%20and%20IP.png)
- Now lets install AD components
![AD install](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/installingad.png)
- Lets make the name of our domain corp.local
![Domain Name](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/creatingdomain.png)
- Lets setup the domain controller's security group
![domain controller](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/securitygroup.png)
### Setup Client Windows Server
- The client windows server will have its DNS set to the domain controller
![DNS domain](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/client%20computer.png)
![test DNS](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/ensure%20dns%20is%20working.png)
- Join the windows server to the domain
![join domain](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/join%20domain.png)
### Setup Users and OUs
- Lets create a OU for users instead of using the default container. Also we will create a user named john.
![john](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/moveusertoOU.png)
- We will apply a GPO to the All Users OU, enabling a password protected screensaver.
![screensaver](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/createsceensavergpo.png)
- Lets force the update and see if it applied
![Update](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/forcegpuupdate.png)
![Seegpo](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/gpuresult.png)
- Now lets create a new Administrator account instead of using the default one, using powershell.
![create user](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/createnewadmin.png)
![add group](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/movealexandertoadmin.png)
- Lets setup the OU structure to accomdate for admins and users, all under one OU.
![OU setup](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/createnewOUusers.png)
- Now we will create a GPO and apply it to the Admin OU to enable account lockout after 5 attempts.
![account lockout](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/accountlockoutadmin.png)
### Enable Remote Access and Connect to Splunk
- Lets enable remote access through WinRM
![remote access](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/remoteaccess%20for%20computers.png)
- Lastly we will install a splunk forwarder to forward logs to our splunk server
![splunk](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/install%20splunk.png)
### Future Enhancements 
- Deploying a WAF for our Apache Website.
- Automating deployment with Terraform and IaC
