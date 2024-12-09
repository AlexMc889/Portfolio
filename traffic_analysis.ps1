get-nettcpconnection | Where-Object { $_.State -eq "Established" } | 
select-object -Property RemoteAddress | 
Out-File -FilePath ".\listactiveips.txt"
cat .\listactiveips.txt
python .\iprepcheckerpowershell.py