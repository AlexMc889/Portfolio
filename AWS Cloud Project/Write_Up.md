# AWS Cloud Infrastructure Project

After obtaining my AWS Solutions Architect and Cloud Practitioner Certifications, I did this project to apply some of the concepts I learned in a hands-on way.  

## Network Diagram  
![VPC Layout](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/VPC_layout.png)

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
- ![Route Table 1](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/Public%20Route%20Table.png)
- ![Route Table 2](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/Public%20Route%20Table.png)
### ALB, ASG, and Launch Template Setup 
- To setup the ALB we must configure what AZs and subnets it will run on and give it a target group (Apache EC2 instances) and a listener to receive external connections.
- The Launch Template will be configured to launch a pre-configured AMI Ubuntu machine. Our AMI will be already connected to our splunk server so that all new EC2 instances are connected as well.
- In the ASG we will set max/min # of EC2 instances to scale up and what paremeter to scale on (we will use CPU usage).
- ![AZ/Subnet ASG](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/ALB%20setup.png)
- ![Listener](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/listener%20setup.png)
### Splunk Server Setup 
- After launching the EC2 instance in a private subnet, to connect to it we will use AWS Session Manager for a secure connection. To do this we will attach a IAM role to enable access.
- ![IAM Role](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/IAM%20role.png)
- Next we will install Splunk enterprise on it and allow data to be recieved on port 9997.
- We will also configure our security group, only allowing SSH from the bastion host, and allowing logs to be received from the bastion host and our Apache EC2 instances.
- We must also allow our bastion host to access the splunk webpage on port 8000.
- ![Splunk Security Group](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/splunksecuritygroup.png)
### Bastion Host Setup
- Our bastion host will allow us access to our splunk server outside of AWS. Although a Direct VPN into our VPC would be better, we will be using a bastion host.
- Since our bastion host is accessible to the internet, we will configure the security group to only allow our IP to SSH into it.
- ![Bastion Security Group](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/Bastion%20Security%20Group.png)
- We will also install a splunk forwarder on this machine, so we can monitor any activity on the EC2 instance.
- ![Splunk forwarder](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/splunk%20forwarder.png)
### Configuring SSH Tunnel to Splunk Server 
- To access our Splunk server from outside the VPC, we must SSH into the bastion host and then forward the Splunk webpage to our own machine.
- To do this we will use PuTTY.
- ![PuTTY Setup](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/PuTTY%20setup.png)
- Now from outside the VPC we can access our Splunk server.
- ![Splunk Logs](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/splunk%20logs.png)
### Monitoring Network for Attacks with Splunk
- Here we can see me attempting a directory brute force against the website.
- ![Splunk Directory Brute Force](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/Splunk%20bruteforce.png)
- We can see all SSH attempts into our Bastion Host to.
- ![SSH into Bastion Logs](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/SSH%20into%20bastion.png)
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
- ![NSLookup Query](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/NSlookup.png)
### Future Enhancements 
- Deploying a WAF for our Apache Website.
- Automating deployment with Terraform and IaC
