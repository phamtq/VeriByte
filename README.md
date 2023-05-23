# VeriByte

## Description:
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

## Table of Contents
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Dependencies
You'll need the following Python libraries in order for this script to work:
- [Requests](https://pypi.org/project/requests/) - a simple, yet elegant, HTTP library.
- [tqdm](https://pypi.org/project/tqdm/) - Fast, Extensible Progress Meter.

You can install them using [pip](https://pypi.org/project/pip/) or use your OS's package manager.

This script has only been tested on Linux with a possibility that it also works in macOS. 

## Installation
Download the script to any directory and run it.

## Usage
To run the script type the following at the command prompt:
```
$ python veribyte.py
```

You'll be asked to copy and paste the URL of the various files. If you get a "Verified OK" then the file is legit. If you get any other message then it could be that the file is corrupted during download or that the file is compromised.

## License
This project is licensed under the MIT License - see the LICENSE file for details.