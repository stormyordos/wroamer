# wroamer
---
Wroamer is a simple Python script leveraging Selenium and Nmap to automate taking screenshots of HTTP/HTTPS services on a network.


```
usage: wroamer.py [-h] [-c CIDR] [-p PORTS] [-f SCANFILE] [-nP] [-u USERNAME]
                  [-pw PASSWORD] [-b BINARY] [-fx]

 optional arguments:
    h, --help            show this help message and exit
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

