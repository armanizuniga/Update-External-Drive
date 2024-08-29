# This is a  Python script to update the Orange External Harddrives used for macOS Installs
# Date: September 28, 2023
# Armani Zuniga

# Scaffolding stuff to make this script work:
# Need to add user_name ALL=(ALL) NOPASSWD: /usr/sbin/softwareupdate to sudoer file to bypass initial password using sudo visudo in terminal 
# pip3 install psutil package
# Harddrive should already be partioned with "Install macOS {name}"
# Can use command: softwareupdate --list-full-installers in terminal to find version number or apple website

import psutil
import subprocess
import os
import platform

#Function to check if the MacBook is connected to Ethernet
def is_ethernet_connected():
    if platform.system() == "Darwin":  # Check if the system is macOS
        try:
            result = subprocess.run(
                ["ifconfig", "en0"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            output = result.stdout
            if "status: active" in output.lower():
                return True
        except subprocess.CalledProcessError:
            pass
    return False


# Function to check if the External Hardrive is connected to the MacBook
def is_external_disk_connected():
    partitions = psutil.disk_partitions(all=True)
    for partition in partitions:
        if "/volumes/ipsw" in partition.mountpoint.lower():
            return True
    return False

# Function to execute terminal commands
# It will except user input as a string and determine with macOS to download and install to the drive
def execute_command():
    # Define your terminal commands as a list of strings
    version_number = input("Enter the macOS version number: ")
    if float(version_number[0:3]) >= 15:
        os_name = version_number
    if float(version_number[0:3]) >= 14 and float(version_number[0:3]) < 15:
        os_name = "Sonoma"
    if float(version_number[0:3]) >= 13 and float(version_number[0:3]) < 14:
        os_name = "Ventura"
    if float(version_number[0:3]) >= 12 and float(version_number[0:3]) < 13:
        os_name = "Monterey"
    if float(version_number[0:3]) >= 11 and float(version_number[0:3]) < 12:
        os_name = "Big Sur"
    if version_number == "10.15.7":
        os_name = "Catalina"
    if version_number == "10.14.6":
        os_name = "Mojave"

    print("Downloading macOS", os_name)

    # Command for terminal to download correct version number
    command1 = ["softwareupdate", "--fetch-full-installer", "--full-installer-version", version_number]
    # Command to image the harddrive with the provided macOS version
    command2 = ["sudo", "-S", "/Applications/Install macOS {}.app/Contents/Resources/createinstallmedia".format(os_name), "--volume", "/Volumes/Install macOS {}".format(os_name)]

    # Execute the first command and wait for it to finish
    try:
        subprocess.run(command1, check=True)
        print("Command 1 finished successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Command 1 failed with error code {e.returncode}")

    # Execute the second command and wait for it to finish
    try:
        subprocess.run(command2, check=True)
        print("Command 2 finished successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Command 2 failed with error code {e.returncode}")

# Main Function to run the script
# Checks first is ethernet and hard drive are present and then executes terminal commands
if __name__ == '__main__':
    #read_file()
    if is_external_disk_connected():
        print("An external disk is connected.")
        print("Beginning macOS Download")
        execute_command()
    else:
        print("No external disk is connected. Please connect the external harddrive")


