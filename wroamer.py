#!/usr/bin/python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

import os
import xml.etree.ElementTree
import argparse
import string
import time
from pyvirtualdisplay import Display


def check_exists_by_css_selector(driver,selector):
    try:
        element=driver.find_element_by_css_selector(selector)
    except NoSuchElementException:
        return None
    return element

def get_firefox_driver(path_to_binary):
    #FIREFOX START (REQUIRES QUANTUM)
    #gecko = os.path.normpath(os.path.join(os.path.dirname(__file__), 'geckodriver'))
    profile = webdriver.FirefoxProfile()
    profile.accept_untrusted_certs = True
    binary = FirefoxBinary(path_to_binary)
    #return webdriver.Firefox(firefox_binary=binary, firefox_profile=profile)
    return webdriver.Firefox(firefox_binary=binary, firefox_profile=profile)


def get_chrome_driver(path_to_binary):
    #CHROME START
    chrome_options = Options()
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(chrome_options=chrome_options, executable_path=path_to_binary)


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--cidr", required=False,
	help="CIDR-compliant IP addresses to scan for Web interfaces")
ap.add_argument("-p", "--ports", required=False,
	help="ports to search for Web services (comma-separated, no argument=1000 most common ports, 'all'=65535 ports)")
ap.add_argument("-f", "--scanfile", required=False,
	help="use specified XML NMAP file as input")
ap.add_argument("-nP", "--noping", required=False,
	help="do not use ping to map hosts", action='store_true')
ap.add_argument("-u", "--username", required=False,
	help="username to send to login forms")
ap.add_argument("-pw", "--password", required=False,
	help="password to send to login forms")
ap.add_argument("-b","--binary", required=False,
	help="path to Selenium driver or Firefox binary")
ap.add_argument("-fx","--firefox", required=False,
	help="Use Firefox instead of Chrome",action='store_true')
args = vars(ap.parse_args())
    
nmapcommand = "nmap"
    
if args["ports"] is None:
    portsarg = ""
else:
    if args["ports"] == "all":
        portsarg="-p 1-65535"
    else:
        portsarg = "-p "+args["ports"]

if args["noping"] == True:
    nmapcommand = nmapcommand+" -Pn"

if args["scanfile"] is None:
    scanfile = "./temp.xml"
    if args["cidr"] is None:
        raise ValueError("Argument CIDR or SCANFILE is required")
    print(" + Performing new Nmap scan ...")
    nmapcommand = nmapcommand+" -T4 -sV -oX "+scanfile+" "+portsarg+" "+args["cidr"]+" > /dev/null"
    os.system(nmapcommand)
else:
    scanfile = args["scanfile"]
    nmapcommand = ""
    
display = Display(visible=0, size=(800, 600))
display.start()
    
if args["firefox"] == True:
    binary='/usr/bin/firefox'
    if args["binary"] is not None:
        binary=args["binary"]
    browser = get_firefox_driver(binary)
else:
    if args["binary"] is None:
        binary='./chromedriver'
    else:
        binary=args["binary"]
    browser = get_chrome_driver(binary)
    
try:
    browser.implicitly_wait(10) # seconds

    print(" + Opening NMAP XML file ...")
    e = xml.etree.ElementTree.parse(scanfile).getroot()
    for hosts in e.findall('host'):
        curaddr = hosts.find('address').attrib["addr"]
        print("------------------")
        print(" + "+curaddr)
        print("------------------")
        for port in hosts.find('ports').findall('port'):
            curport = port.attrib["portid"]
            protocol = ""
            if port.find('state').attrib["state"]=="open":
                if (port.find('service').attrib["name"] == "http"):
                    protocol = "http"
                    if "tunnel" in port.find('service').attrib:
                        if port.find('service').attrib["tunnel"] == "ssl":
                            protocol = "https"

                if (port.find('service').attrib["name"] == "https"):
                    protocol = "https"
                #if (port.find('service').attrib["name"] == "ftp"):                
                #    protocol = "ftp"
                    
                if not (protocol == ""):
                    print(""+curport+":open:"+protocol)
                    basicauth=""
                    #    basicauth=args["username"]+":"+args["password"]+"@"
                    try:
                        browser.get(protocol+"://"+basicauth+curaddr+":"+curport)
                        wait = WebDriverWait(browser, timeout=15)
                        time.sleep(1)
                        if (args["username"] is not None) and (args["password"] is not None):
                            element=check_exists_by_css_selector(browser,"input[id*=username]")
                            if element is not None:
                                element.send_keys(args["username"])
                                #print element.text

                            element=check_exists_by_css_selector(browser,"input[id*=password]")
                            if element is not None:
                                element.send_keys(args["password"])
                                #print element.text

                            element=check_exists_by_css_selector(browser,"input[id*=passwd]")
                            if element is not None:
                                element.send_keys(args["password"])
                                #print element.text
                            
                            element=check_exists_by_css_selector(browser,"input[id*=submit]")                                                
                            if element is not None:
                                element.click()
                                wait = WebDriverWait(browser, timeout=15)
                                time.sleep(5)
                        else:
                            if protocol=="https":
                                time.sleep(5)
                        print browser.title
                    except TimeoutException:
                        print "Timeout!"
                       

                    browser.save_screenshot("./"+curaddr+"-"+curport+".png")     

    #if not (nmapcommand == ""):
    #    os.remove("./temp.xml")
finally:
    browser.quit()
    display.stop()
