# godaddy-dyndns
DynDNS-like public IP auto-updater script for GoDaddy

## Usage
### Add the following line to your crontab

0 3 * * 1 /bin/bash /path/to/godaddy-ddns.sh >> /path/to/godaddy-ddns.log 2>&1
