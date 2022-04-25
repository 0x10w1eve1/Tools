$secpasswd = ConvertTo-SecureString "USER_PASSWORD_HERE" -AsPlainText -Force
$mycreds = New-Object System.Management.Automation.PSCredential ("USER_NAME_HERE",$secpasswd)
$computer = "computer name goes here"
[System.Diagnostics.Process]::Start("C:\Users\user name goes here\shell.exe","",$mycreds.Username, $mycreds.Password, $computer)

