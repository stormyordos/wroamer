# wroamer
---
Wroamer is a simple Python script leveraging Selenium and Nmap to automate taking screenshots of HTTP/HTTPS services on a network.


```
usage: wroamer.py [-h] [-c CIDR] [-p PORTS] [-f SCANFILE] [-nP] [-u USERNAME]
                  [-pw PASSWORD] [-b BINARY] [-fx]

 optional arguments:
  -h, --help            show this help message and exit
  -c CIDR, --cidr CIDR  CIDR-compliant IP addresses to scan for Web interfaces
  -p PORTS, --ports PORTS
                        ports to search for Web services (comma-separated, no
                        argument=1000 most common ports, 'all'=65535 ports)
  -f SCANFILE, --scanfile SCANFILE
                        use specified XML NMAP file as input
  -nP, --noping         do not use ping to map hosts
  -u USERNAME, --username USERNAME
                        username to send to login forms
  -pw PASSWORD, --password PASSWORD
                        password to send to login forms
  -b BINARY, --binary BINARY
                        path to Selenium driver or Firefox binary
  -fx, --firefox        Use Firefox instead of Chrome
```

# Features
* Scans a network with NMap for http/https services
* Scans Nmap's 1000 common ports, 65535 ports (option "-p all") or specific comma-separated ports
* Supports re-using another Nmap scan with direct XML input (option "-f")
* Supports both Firefox and Chrome in pseudo-headless modes
* Captures screenshots of visited services for later browsing
* Useful during pentest engagements in order to quickly map internal Web services
* *Experimental* : auto-logging on visited sites

# Installation
* ` git clone https://github.com/stormyordos/wroamer.git `
* For Chrome: Download chromedriver on http://chromedriver.chromium.org/downloads, Wroamer will look for it in the execution directory, may be manually specified with "-b" option
* For Firefox: Download geckodriver on https://github.com/mozilla/geckodriver/releases
* For Firefox: additional configuration/troubleshooting may require manual specification of Firefox Quantum binary using "-b" option 
* Requires python-PyVirtualDisplay and python-EasyProcess packages
* Tested on Python 2.7x / Linux OpenSuSE. Should work on most other distributions supporting Python ... may even work with Windows

# Examples
* Parse TEMP.XML Nmap output file with custom Firefox Quantum : `./wroamer.py --firefox --binary /usr/local/bin/firefox -f temp.xml`
* Perform a simple Nmap scan on Web ports with Chrome : `./wroamer.py -p 80,443,8080 -c 192.168.1.0/24`
* Perform an Nmap scan on all ports with Chrome : `./wroamer.py --noping -p all -c 10.1.200.30-150`


