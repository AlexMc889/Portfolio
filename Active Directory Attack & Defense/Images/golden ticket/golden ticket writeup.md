# Golden Ticket Attack & Detection

## What is a Golden Ticket Attack
- A golden ticket attack targets the KRBTGT account's hash
- The KRBTGT is used to sign all TGTs, so compromising it grants the ability to forge any ticket
- Typically privileged access to the Domain Controller is required, although a DCSync attack can also acquire the KRBGT account hash
- Leads to complete domain compromise including dumping NTDS.DIT file (contains all domain users password hashes), typically though a shadow copy

## Executing the Attack 
### Getting Golden Ticket
- Lets use a mimikatz to perform a DCSync attack to get the KRBTGT account's hash
- ![dcynsc](https://github.com/AlexMc889/Portfolio/blob/main/Active%20Directory%20Attack%20%26%20Defense/Images/golden%20ticket/dcsnc%20krbgt.png)
- Now we have the KRBTGT account's hash
- ![hash](https://github.com/AlexMc889/Portfolio/blob/main/Active%20Directory%20Attack%20%26%20Defense/Images/golden%20ticket/golden%20ticket%20hash.png)

### Using Golden Ticket To Access Domain Controller
- Now lets inject the golden ticket in our current session to use it for authentication
- ![use ticket](https://github.com/AlexMc889/Portfolio/blob/main/Active%20Directory%20Attack%20%26%20Defense/Images/golden%20ticket/golden%20ticket.png)
- Using the golden ticket we can now access the Domain Controller
- ![access DC](https://github.com/AlexMc889/Portfolio/blob/main/Active%20Directory%20Attack%20%26%20Defense/Images/golden%20ticket/Access%20files.png)
- ![DC accessed](https://github.com/AlexMc889/Portfolio/blob/main/Active%20Directory%20Attack%20%26%20Defense/Images/golden%20ticket/access%20to%20domain%20controller.png)

### Extracting the NTDS.DIT File over SMB
- The NTDS.DIT file is typically locked down by AD services so copying it regularly isn't feasible
- ![failed access ntds.dit](https://github.com/AlexMc889/Portfolio/blob/main/Active%20Directory%20Attack%20%26%20Defense/Images/golden%20ticket/cant%20copy%20because%20ntds.dit%20in%20use.png)
- Now that we have access to the DC lets create a shadow copy, expose the shadow copy to the internet, and pull the NTDS.DIT file from the SMB share
- ![Create shadow](https://github.com/AlexMc889/Portfolio/blob/main/Active%20Directory%20Attack%20%26%20Defense/Images/golden%20ticket/create%20shadow.png)
- Lets expose the shadow copy to exfiltrate it
- ![expose](https://github.com/AlexMc889/Portfolio/blob/main/Active%20Directory%20Attack%20%26%20Defense/Images/golden%20ticket/expose%20shadow.png)
- Now lets copy the NTDS.DIT file from the shadow copy
- ![copy](https://github.com/AlexMc889/Portfolio/blob/main/Active%20Directory%20Attack%20%26%20Defense/Images/golden%20ticket/expose%20shadow.png)

## Detection
- We can detect the SMB logs of the NTDS.DIT file being extracted using wireshark on the DC
- ![smb access](https://github.com/AlexMc889/Portfolio/blob/main/Active%20Directory%20Attack%20%26%20Defense/Images/golden%20ticket/smb%20logs%20ntds%20dit%20transfer.png)
- Since SMB is not encrypted by default we can see what files are being accessed.

## Mitigations
- Securing access to the Domain Controller is essential to preventing a KRBTGT attack. (EDR, Implementing JumpBox, Least Privilege, Physical Access etc)
  
