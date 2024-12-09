#!/bin/bash 
ss --ipv4 | awk '{split($6, a, ":"); print a[1]}' > listactiveips.txt
python3 check_ips.py
