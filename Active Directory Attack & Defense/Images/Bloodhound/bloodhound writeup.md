# Bloodhound Recon & Detection

## What is Bloodhound
- Bloodhound is a tool used to map relationships, privileges, and potential attack paths in an AD environment
- Typically data is extracted using Sharphound by querying the Domain Controller.
- Commonly used by both red teams and blue teams, to find and mitigate attack vectors
- Bloodhound allows to graphically visualize relationships and an attack path.

## Setup 
- Lets install Bloodhound on a Kali machine
- ![bloodhound install](https://github.com/AlexMc889/Portfolio/blob/main/Active%20Directory%20Attack%20%26%20Defense/Images/Bloodhound/install%20bloodhound.png)
- Lets make sure we port forward the web access to Bloodhound when we SSH into our Kali machine.
- ![port forward](https://github.com/AlexMc889/Portfolio/blob/main/Active%20Directory%20Attack%20%26%20Defense/Images/Bloodhound/port%20forward%20bloodhound.png)
- Now we can access the Bloodhound interface
- ![bloodhound interface](https://github.com/AlexMc889/Portfolio/blob/main/Active%20Directory%20Attack%20%26%20Defense/Images/Bloodhound/login%20bloodhound.png)

## Executing the Attack 
- To collect data to import into Bloodhound, we will use a tool called Sharphound
- ![Sharphound](https://github.com/AlexMc889/Portfolio/blob/main/Active%20Directory%20Attack%20%26%20Defense/Images/Bloodhound/sharphound%20running.png)
- This will generate JSON files containing all AD data
- ![AD file](https://github.com/AlexMc889/Portfolio/blob/main/Active%20Directory%20Attack%20%26%20Defense/Images/Bloodhound/json%20files.png)
- After importing these JSON files into Bloodhound lets visualize some relationships
- This is a relationship from the OU "AllComputers" to the Domain Controller
- ![computer to dc](https://github.com/AlexMc889/Portfolio/blob/main/Active%20Directory%20Attack%20%26%20Defense/Images/Bloodhound/map%20allcomputers%20to%20admin.png)
- We can also map the user Bob to Domain Admin
- ![bob to admin](https://github.com/AlexMc889/Portfolio/blob/main/Active%20Directory%20Attack%20%26%20Defense/Images/Bloodhound/map%20bob%20to%20admin.png)
- This will help us find misconfigurations in OUs, security groups, and policies that can lead to exploitation.

## Detection 
- Sharphound gathers all info about the AD environment which creates a lot of noise.
- We can use Event ID 3 (Network Connection) and the stats command in splunk.
- ![splunk](https://github.com/AlexMc889/Portfolio/blob/main/Active%20Directory%20Attack%20%26%20Defense/Images/Bloodhound/excessive%20network%20connections%20by%20sharphound.png)
- As we can see Sharphound generated 124 Events from querying data from the DC
- We can also use wireshark to see the noise Sharphound creates
- ![wireshark](https://github.com/AlexMc889/Portfolio/blob/main/Active%20Directory%20Attack%20%26%20Defense/Images/Bloodhound/SAMR%20requests.png)
- Here we can see SAMR requests (Security Account Manager Remote) from Sharphound gathering info on users
- Sharphound also generates LDAP requests while enumerating the domain.
- ![ldap](https://github.com/AlexMc889/Portfolio/blob/main/Active%20Directory%20Attack%20%26%20Defense/Images/Bloodhound/ldap%20requests.png)

## Mitigations
- Limiting enumeration abilites and monitor for excessive queries from one source
