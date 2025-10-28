# Pass-The-Hash Attack & Detection 

## What is Pass-The-Hash
- Pass-The-Hash is when an attacker gains local admin access and then dump credentials from LSASS (Local Security Authority Subsystem Service), typically using mimikatz
- From there it can use the NTLM hash to authenticate to other systems
- Attacker never needs to know password since he has NTLM hash.

## Setup 
- First we need to enable Event ID 10 in our sysmon config file, which is usually set to off due to the amount of noise it generates
- Event ID 10 detects when a process accessed another process's memory
- It can detect credential theft attempts like Mimikatz accessing LSASS
- ![enable 10](https://github.com/AlexMc889/Portfolio/blob/main/Active%20Directory%20Attack%20%26%20Defense/Images/pass%20the%20hash/sysmonconfig%20for%20event%20ID%2010.png)
- Now lets update sysmon
- ![update sysmon](https://github.com/AlexMc889/Portfolio/blob/main/Active%20Directory%20Attack%20%26%20Defense/Images/pass%20the%20hash/sysmonconfig%20for%20event%20ID%2010.png)

## Executing the Attack 
- This attack requires local admin access on the computer to access LSASS
- We will first open mimikatz and ensure we have the privilege "debug"
- ![privilege debug](https://github.com/AlexMc889/Portfolio/blob/main/Active%20Directory%20Attack%20%26%20Defense/Images/pass%20the%20hash/privilege%20debu%20mimikatz.png)
- Now lets dump LSASS
- ![dump lsass](https://github.com/AlexMc889/Portfolio/blob/main/Active%20Directory%20Attack%20%26%20Defense/Images/pass%20the%20hash/get%20logonpassswords.png)
- Now with the hash from dumping lsass we can authenticate to the DC
- ![generate tgt](https://github.com/AlexMc889/Portfolio/blob/main/Active%20Directory%20Attack%20%26%20Defense/Images/pass%20the%20hash/ask%20tgt.png)

## Detection with Splunk & Wireshark
- Event ID 10 generated with access to lsass from a suspicious program is the main indicator
- Lets make a search for Event ID 10 logs with suspicious attributes
- ![event id 10 splunk](https://github.com/AlexMc889/Portfolio/blob/main/Active%20Directory%20Attack%20%26%20Defense/Images/pass%20the%20hash/10%20lsass%20access.png)
- We can see that mimikatz.exe access lsass.exe, additionally the SourceUser being different from the TargetUser is also a indicator
- We can also find the network logs of the kerberos requests for the TGT
- ![wireshark](https://github.com/AlexMc889/Portfolio/blob/main/Active%20Directory%20Attack%20%26%20Defense/Images/pass%20the%20hash/Kerbos%20request.png)
- ![username of tgt request](https://github.com/AlexMc889/Portfolio/blob/main/Active%20Directory%20Attack%20%26%20Defense/Images/pass%20the%20hash/Kerbos%20request.png)
- We can also find the username of the TGT request in the wireshark logs

## Mitigations
- Restriciting and alerting on local administrator access can help detect this attack. Implementing LAPS would help secure local admin accounts.
- Most EDRs will detect and alert on suspicious LSASS access.
