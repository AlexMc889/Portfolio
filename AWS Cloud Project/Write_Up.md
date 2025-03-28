# AWS Cloud Infrastructure Project 
After obtaining my AWS Solutions Architect and Cloud Practioner Certifications, I did this project to apply some of the concepts I learned in a hands-on way.  
## Network Diagram 
<img src="https://github.com/AlexMc889/Portfolio/blob/main/AWS%20Cloud%20Project/Images/VPC%20layout%20.png">
## Overview
The goal of the project was to setup a secure, scalable, and available infrastructure to host a website and a splunk server. 
Security will be implemented through segmenting each part of the network into its own subnet. Certain subnets will be private and external access will only be provisioned through a bastion host. 
Scalability and Availability will be implemented by using an Application Load Balancer and a Auto Scaling Group. 
Laslty, our Splunk server will monitor our bastion host and any EC2 instance started by the ASG. 
## VPC Setup 
First we must setup our subnets and then route tables for each subnet. 
### Subnets
#### 10.0.1.0/24 & 10.0.5.0/24 (public) - These will be used by our Application Load Balancer as access to our website. AWS requires 2 subnets in 2 different AZs for a ALB, increasing availabilty. 
#### 10.0.3.0/24 - 
