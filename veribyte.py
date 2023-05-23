"""
===============================================================================
Program Name: VeriByte 
Creator: Timothy Q pham
Creator's Email: phamtq@clikclak.io

Creation Date: 05-12-2023
Last Revision Date: N/A
Version: 1.0.0

License: Creative Commons

Program Description:
This program is designed to help automate the checking of the authenticity and 
integrity of downloaded ISO and image files for things like firewalls, routers,
etc... 

Often times people will download these files without checking to see if the
file is authentic. Simply checking to see if the cryptographic hash / digest
matches the one on the website isn't enough because that's only checking file
integrity. It is entirely possible that an attacker has replaced an ISO with
their own and changed the digest to reflect their copy (see 2016 Linux Mint
hack). 

Because of how time consuming or difficult it might be to perform this check
appropriately, this program was created to help folks out. 

It will ask you to paste the URL of the file, the digital signature (.sig), and
the public key (.pub). Ideally, these should all be from different mirrors.

===============================================================================
"""

import requests
from tqdm import tqdm
import time
import subprocess


# Ask for the URL of the file, the digital signature (.sig), and the public 
# key (.pub)
iso_url = input("Please enter the URL of the ISO/IMG file: ")
digital_sig_url = input("Enter the URL of the digital signature (.sig): ")
public_key_url = input("Enter the URL of the public key (.sig, PEM format): ")

# ------- Code Section for ISO/IMG download ---------------------

# Send a HTTP request to the URL of the file
response = requests.get(iso_url, stream=True)

# Get the total file size
file_size = int(response.headers.get('Content-Length', 0))

# Get the file name
iso_name = iso_url.split("/")[-1]

# Progress bar
progress = tqdm(response.iter_content(1024), f'Downloading {iso_name}', total=file_size, unit='B', unit_scale=True, unit_divisor=1024)

with open(iso_name, 'wb') as f:
    for data in progress.iterable:
        # Write data read to the file
        f.write(data)
        # Update the progress bar manually
        progress.update(len(data))

# ------- Code Section for digital signature download ---------------------

# Send a HTTP request to the URL of the file
response = requests.get(digital_sig_url, stream=True)

# Get the total file size of the next download
file_size = int(response.headers.get('Content-Length', 0))

# Get the file name
digital_sig_name = digital_sig_url.split("/")[-1]

# Progress bar
progress = tqdm(response.iter_content(1024), f'Downloading {digital_sig_name}', total=file_size, unit='B', unit_scale=True, unit_divisor=1024)

with open(digital_sig_name, 'wb') as f:
    for data in progress.iterable:
        # Write data read to the file
        f.write(data)
        # Update the progress bar manually
        progress.update(len(data))

# ------- Code Section for public key  download ---------------------

# Send a HTTP request to the URL of the file
response = requests.get(public_key_url, stream=True)

# Get the total file size
file_size = int(response.headers.get('Content-Length', 0))

# Get the file name
public_key_name =public_key_url.split("/")[-1]

# Progress bar
progress = tqdm(response.iter_content(1024), f'Downloading {public_key_name}', total=file_size, unit='B', unit_scale=True, unit_divisor=1024)

with open(public_key_name, 'wb') as f:
    for data in progress.iterable:
        # Write data read to the file
        f.write(data)
        # Update the progress bar manually
        progress.update(len(data))

# --------- Code for authentification ---------------------------

# Check if the signature file is in base64 format and if not convert to binary
cmd_output = subprocess.run("file " + "--mime " "./" + digital_sig_name, shell=True, capture_output=True).stdout.decode('utf-8').strip()
encoding_output = cmd_output.split()
if encoding_output[1] == "text/plain;":
    subprocess.run("openssl base64 -d -in " + digital_sig_name + " -out decoded.signature.file.sig", shell=True)
else:
    print("Error converting digital signature to binary format.")

# Now verify the file
cmd_output = subprocess.run("openssl dgst -verify " + public_key_name + " -sha256 -signature decoded.signature.file.sig " + iso_name, shell=True, capture_output=True).stdout.decode('utf-8').strip()
if cmd_output == "Verified OK":
    print("The file is authentic.")
else:
    print("Authenticity Failed: File is either compromised or damaged. Please perform a checksum and compare it to the one on the website.")