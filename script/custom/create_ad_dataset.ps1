####################################################
# This script is derived from one by Brian O'Connell
# AUTHOR : Brian O'Connell @LifeOfBrianOC
# https://lifeofbrianoc.wordpress.com/
# It will do the following:
# Check for Active Directory Powershell Module and install if not Present
# Create OU's based on csv Input - Checks for existing OU first
# Create Groups based on csv input - Checks for existing Groups first
# Adds Groups to other Groups based on csv input
# Create Users based on csv Input - Checks for existing Users first
# Add Users to specific Groups based on csv Input
#####################################################
Write-host "This script will create all required AD users & groups in Active Directory
" -ForegroundColor Yellow

# Set Console ForegroundColor to Yellow for Read-Host as -ForegroundColor doesn't work with Read-Host
[console]::ForegroundColor = "yellow"

# Ask user for csv path
$UserCSVPath = Read-Host "Please enter the full path to your csv with user details"

# Reset Console ForegroundColor back to default
[console]::ResetColor()

# Verify CSV Path
$testCSVPath = Test-Path $UserCSVPath
if ($testCSVPath -eq $False) {
    Write-Host "CSV File Not Found. Please verify the path and retry
    " -ForegroundColor Red
    Exit
}

# Set Console ForegroundColor to Yellow for Read-Host as -ForegroundColor doesn't work with Read-Host
[console]::ForegroundColor = "yellow"

$GroupCSVPath = Read-Host "Please enter the full path to your csv with group details"

# Reset Console ForegroundColor back to default
[console]::ResetColor()

# Verify CSV Path
$testCSVPath = Test-Path $GroupCSVPath
if ($testCSVPath -eq $False) {
    Write-Host "CSV File Not Found. Please verify the path and retry
    " -ForegroundColor Red
    Exit
}

# Set Console ForegroundColor to Yellow for Read-Host as -ForegroundColor doesn't work with Read-Host
[console]::ForegroundColor = "yellow"

$MbrCSVPath = Read-Host "Please enter the full path to your csv with group member details"

# Reset Console ForegroundColor back to default
[console]::ResetColor()

# Verify CSV Path
$testCSVPath = Test-Path $MbrCSVPath
if ($testCSVPath -eq $False) {
    Write-Host "CSV File Not Found. Please verify the path and retry
    " -ForegroundColor Red
    Exit
}

#####################################################
# AD Powershell Module #
#####################################################

# Checking for Required AD Powershell Module. Importing if not available
Write-host "Checking for Required AD Powershell Module
" -ForegroundColor Green

$name="ActiveDirectory"
if(-not(Get-Module -name $name))
{
if(Get-Module -ListAvailable | Where-Object { $_.name -eq $name })
{
# Module is installed so import it
Import-Module -Name $name
}
else
{
# If Module is not installed
$false
}
# Install Module
write-host "Active Directory powershell Module Not Installed - Installing
" -ForegroundColor Red
{
}
Import-Module servermanager
Add-WindowsFeature -Name "RSAT-AD-PowerShell" -IncludeAllSubFeature | Out-Null
}
# End if module is not installed
else
{
# If Module is already installed
write-host "Active Directory Module Already Installed - Continuing
" -ForegroundColor Green
}

#####################################################
# User Creation #
#####################################################
# Creating Users from csv
Write-Host "Creating Users
" -ForegroundColor Yellow

# Import CSV
$csv = @()
$csv = Import-Csv -Path $UserCSVPath

# Loop through all items in the CSV
ForEach ($item In $csv)
{
    #Check if the User exists
    $samAccountName = "CN=" + $item.AccountID
    $userExists = [ADSI]::Exists("LDAP://$($samAccountName),OU=Users,OU=RiskCo,$($searchbase)")

    If ($userExists -eq $true)
    {
        Write-Host "User $($item.AccountID) Already Exists. User creation skipped!
        " -ForegroundColor Red
    }
    else
    {
        # Create The User
        $name = $item."First Name" + " " + $item."Last Name"
        $userPrincinpal = $item.Email
        If ([string]::IsNullOrEmpty($item.Manager))
        {
            New-ADUser -Name $name `
            -GivenName $item."First Name" `
            -Surname $item."Last Name" `
            -Path ("OU=Users,OU=RiskCo," + $( $searchbase )) `
            -SamAccountName $item.AccountID `
            -UserPrincipalName $userPrincinpal `
            -EmailAddress $item.Email `
            -Company $item.Company `
            -Department $item.Department `
            -Title $item.Job `
            -AccountPassword (ConvertTo-SecureString "Password123!" -AsPlainText -Force) `
            -ChangePasswordAtLogon $false `
            -PasswordNeverExpires $true `
            -Enabled $true
        }
        else
        {
            New-ADUser -Name $name `
            -GivenName $item."First Name" `
            -Surname $item."Last Name" `
            -Path ("OU=Users,OU=RiskCo," + $( $searchbase )) `
            -SamAccountName $item.AccountID `
            -UserPrincipalName $userPrincinpal `
            -EmailAddress $item.Email `
            -Company $item.Company `
            -Department $item.Department `
            -Title $item.Job `
            -Manager $item.Manager `
            -AccountPassword (ConvertTo-SecureString "Password123!" -AsPlainText -Force) `
            -ChangePasswordAtLogon $false `
            -PasswordNeverExpires $true `
            -Enabled $true
        }
        Write-Host "User $($item.AccountID) created!
        " -ForegroundColor Green
    }
}
Write-host "Creating Users Complete
" -ForegroundColor Green

#####################################################
# Group Creation #
#####################################################
Write-host "
Creating Required Groups
" -ForegroundColor Yellow

# Get Domain Base Path
$searchbase = Get-ADDomainController | ForEach {  $_.DefaultPartition }

# Import CSV
$csv = @()
$csv = Import-Csv -Path $GroupCSVPath

# Loop through all items in the CSV
ForEach ($item In $csv)
{
    # Check if the Group already exists
    $groupName = "CN=" + $item.Group + ",OU=Groups,OU=RiskCo"
    $groupExists = [ADSI]::Exists("LDAP://$( $groupName ),$( $searchbase )")

    if ($groupExists -eq $true)
    {
        Write-Host "Group $( $item.Group ) already exists! Group creation skipped!
" -ForegroundColor Red
    }
    else
    {
        # Create the group if it doesn't exist
        New-ADGroup -Name $item.Group -Description $item.Group -ManagedBy $item.Owner -GroupScope 2 -Path ("OU=Groups,OU=RiskCo," + $( $searchbase ))
        Write-Host "Group $( $item.Group ) created!
" -ForegroundColor Green
    }
}

Write-Host "Group Creation Complete
" -ForegroundColor Green

#####################################################
# User Group Memberships Creation #
#####################################################
# Creating User Group Memberships from csv
Write-Host "Creating User Group Memberships
" -ForegroundColor Yellow

# Import CSV
$csv = @()
$csv = Import-Csv -Path $MbrCSVPath

# Loop through all items in the CSV
ForEach ($item In $csv)
{
    # Check if the User is already a member of the group
    $userIsMember = (Get-ADGroupMember -Identity $item.Group).SamAccountName -contains "$($item.Account)"
    If ($userIsMember -eq $true)
    {
        Write-Host "User $($item.Account) is already a member of $($item.Group). Add to Group skipped!
        " -ForegroundColor Red
    }
    else
    {
        Add-ADGroupMember -Identity $item.Group -Members $item.Account;
        Write-Host "User $($item.Account) added to group $($item.Group)!
        " -ForegroundColor Green
    }
}

Write-host "Creating User Group Memberships Complete
" -ForegroundColor Green