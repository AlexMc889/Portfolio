# AWS Cloud Infrastructure Project

After obtaining my AWS Solutions Architect and Cloud Practitioner Certifications, I did this project to apply some of the concepts I learned in a hands-on way.  

## Network Diagram  
![VPC Layout](https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/VPC%20layout%20.png)

## Overview  
The goal of the project was to set up a secure, scalable, and available infrastructure to host a website and a Splunk server.  
Security will be implemented through segmenting each part of the network into its own subnet. Certain subnets will be private, and external access will only be provisioned through a bastion host.  
Scalability and availability will be implemented by using an Application Load Balancer and an Auto Scaling Group.  
Lastly, our Splunk server will monitor our bastion host and any EC2 instance started by the ASG.  

## VPC Setup  
First, we must set up our subnets and then route tables for each subnet.  

### Subnets  
- **10.0.1.0/24 & 10.0.5.0/24 (Public)** - These will be used by our Application Load Balancer as access to our website. AWS requires 2 subnets in 2 different AZs for an ALB, increasing availability. 
