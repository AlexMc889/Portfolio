# Kubernetes Project 

I decided to do this project to learn the funadmentals of kubernetes by building  my own kubernetes cluster. 

## Layout 


## Overview 

The goal of this project is to: 
- Set up a kuberentes cluster using kubeadm on EC2 with a control plane and one worker node
- Deploy a nginx web server running ModSecurity as a WAF
- Use Falco to secure containersdoes it

## Setup Cluster
- Lets install kubeadm
- ![install masternode](https://github.com/AlexMc889/Portfolio/blob/main/Kubernetes%20Project/Images/install%20kubeadm%201%20.png)
- ![install kubeadm](https://github.com/AlexMc889/Portfolio/blob/main/Kubernetes%20Project/Images/install%20kubeadm%202%20.png)
- Kubernetes requires for swap to be turned off 
- ![turnoffswap](https://github.com/AlexMc889/Portfolio/blob/main/Kubernetes%20Project/Images/turnoffswap.png)
- We will be using containerd as our runtime
- ![containderd install](https://github.com/AlexMc889/Portfolio/blob/main/Kubernetes%20Project/Images/install%20containerd.png)
- Lets intialize our cluster
- ![start cluster](https://github.com/AlexMc889/Portfolio/blob/main/Kubernetes%20Project/Images/inialize%20master%20node.png)
- Now lets connect the worker node
- ![connect worker](https://github.com/AlexMc889/Portfolio/blob/main/Kubernetes%20Project/Images/join%20the%20worker%20node.png)
- Lets configure our config file so we point to the right IP for the Kubernetes API
- ![config file](https://github.com/AlexMc889/Portfolio/blob/main/Kubernetes%20Project/Images/setup%20config%20file.png)
- Now both of our nodes are running
- ![nodes running](https://github.com/AlexMc889/Portfolio/blob/main/Kubernetes%20Project/Images/kubectl%20get%20nodes%20.png)

## Deploy Nginx with ModSecurity 
- This will be our deployment for nginx
- ![nginx](https://github.com/AlexMc889/Portfolio/blob/main/Kubernetes%20Project/Images/nginx%20deployment.png)
- This will be our service for nginx
- ![service](https://github.com/AlexMc889/Portfolio/blob/main/Kubernetes%20Project/Images/service%20nginx.png)
- Now we can apply both of these
- ![applying](https://github.com/AlexMc889/Portfolio/blob/main/Kubernetes%20Project/Images/apply%20nginx%20deployment.png)
- We can see our services and pods now
- ![pods](https://github.com/AlexMc889/Portfolio/blob/main/Kubernetes%20Project/Images/get%20pods.png)
- ![svc](https://github.com/AlexMc889/Portfolio/blob/main/Kubernetes%20Project/Images/get%20svc.png)
- Now lets apply our ModSecurity config, which should block some known scanners
- ![modsecurity](https://github.com/AlexMc889/Portfolio/blob/main/Kubernetes%20Project/Images/Apply%20mod%20security%20config.png)
- If we attempt to curl with the headers "Nikto" we will get a 403 forbidden
- ![curl](https://github.com/AlexMc889/Portfolio/blob/main/Kubernetes%20Project/Images/curl%20test.png)

## Installing Falco 
- We can use helm to install faco in namespace "falco"
- ![falco](https://github.com/AlexMc889/Portfolio/blob/main/Kubernetes%20Project/Images/falco%20installing.png) '
- Now our falco pods are running
- ![falco running](https://github.com/AlexMc889/Portfolio/blob/main/Kubernetes%20Project/Images/falco%20started.png)
- Lets exec into one of our nginx servers and try to access sensitive files like /etc/shadow
- ![exec](https://github.com/AlexMc889/Portfolio/blob/main/Kubernetes%20Project/Images/kubectl%20exec.png)
- We can see falco logs these attempts
- ![falco logs](https://github.com/AlexMc889/Portfolio/blob/main/Kubernetes%20Project/Images/falcoalert.png)

## Future Improvements 
- We could add more rules and alerts in ModSecurity and Falco
- We could migrate this cluster to rancher for greater control and more integrations
