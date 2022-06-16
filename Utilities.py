import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from urllib.request import URLopener
from socket import timeout

import re
import time
import os
import pandas as pd
import sys
import logging

def openURL(url, headers = {"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}, sleep_sec=0):
    """
    Opens/Access the URL then returns a bs4.BeautifulSoup class
    
    Parameters
    ----------
    url : string (required)
        http url that is intended to be opened/accessed

    headers : dict (optional)
        contains the header settings for the request

    sleep_sec : int (optional)
        the number of seconds to wait for the website to load

    Returns
    -------
    object
        returns a bs4.BeautifulSoup object for further data manipulation
    """
    
    loaded = False       # tells us whether the page has loaded or not
    reloadCount = 0      # counts how many times we've tried to load the page
    max_reloadCount = 10 # the maximum amount of times for the program to reload
    wait_for_reload = 3  # the amount of time it takes for the program to reload
    timeout = (30, 60)   # wait for a maximum of 20 seconds for the page to load
    soup = -1
    while(loaded == False and reloadCount < max_reloadCount):
        try:
            try:
                response = requests.get(url, headers=headers, timeout=timeout) # goes to the url (ex. https://www.sephora.com/ca/en/shop/face-makeup?pageSize=300)
                time.sleep(sleep_sec)
                loaded = True
                soup = BeautifulSoup(response.text, 'html.parser')
                response.close()
            except requests.exceptions.RequestException as e:
                reloadCount += 1  # increment reload count
                time.sleep(wait_for_reload) # wait for [wait_for_reload] (the time we designate for it to wait until reload)
                logError('Failed to load, now restarting', url, e)
                logging.error('\tFailed to load, now restarting')
        except Exception as e:
            logError('Failed to load the page', url, e)
            logging.error('\tFailed to load the page')
            break
    if(reloadCount == 10):
        logging.error('\tERROR: {} failed to load...'.format(url))
        logError('ERROR website failed to load', url, '')    
    return soup

# gets downloads the file (retries to download if failed)
def retrieveFile(source, filename):
    """
    Downloads a file in the current directory using the filename from the source
    
    Parameters
    ----------
    source: string

    filename: string
        the filenname 
    """
    opener = URLopener(timeout=15)
    opener.addheader('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36')
    tries = 10
    wait_for_reload = 3
    n = 0
    not_loaded = True
    while(not_loaded):
        try:
            opener.retrieve(source, filename)
            not_loaded = False
        except timeout:
            logging.error('socket timed out - URL %s', url)
        except Exception as e:
            logging.error('\t\tERROR: Failed to load [ %s ] [ %s ] and will retry to get the file' % (filename, source))
            n += 1
        if(n > tries):
            logError('Failed to get the file %s' % filename, source, e)
            logging.error('\t\tERROR: Failed to get the url -> %s [ ]' % (filename, source))
            break
        else:
            time.sleep(wait_for_reload)

# Logs the error to easily see where errors occured
def logError(message, url='', e=''):
    """
    Logs the error using the message, url, and exception error to a error_log.txt file

    Parameters
    ----------
    message : string (required)
        description of the error

    url : string (optional)
        url where the error occured

    e : str(Exception) (optional)
        Error Exception that occured
    """
    with open('error_log.txt', 'a') as f:
        f.write('{}|{}|{}\n'.format(message, url, e))


# Scrolls to the Bottom of the Page
def scrollToBottom(driver):
    """
    Scrolls to the bottom of the page to load the informations that will not be loaded unless you scroll

    Parameters
    ----------
    driver : chromedriver (required)
        the driver that will be scrolled on
    """
    scroll = 0         # set scroll to 0px/top of the page (default) which will later on allow us to navigate the scrolling of the website
    scrollValue = 800  # constant incrementor (meaning we go down 800px in a page)
    while(scroll < driver.execute_script("return document.body.scrollHeight")): # gets the scrollheight of the page and continues to loop until it hasn't reach the bottom of the page
        scroll += scrollValue  # increment scroll by scrollValue
        driver.execute_script("window.scrollTo(0, {});".format(scroll)) # executes a javascript command to scroll to a specific area which in this case is [scroll]
        time.sleep(0.2)        # wait for 0.2 sec to prevent it from scrolling too fast (scrolling too fast will sometimes give us errors)

# Sets up chromeOptions for the Web Driver Settings
def settingDriverOptions():
    """
    Sets up the chrome options for the chrome web driver

    Returns
    -------
    object
        selenium.webdriver.chrome.options.Options() object
    """
    # webdriver options
    chromeOptions = Options()
    # chromeOptions.add_argument('--kiosk')                          # sets the headless browser into full screen mode
    chromeOptions.add_argument('--headless')                       # opens the browser silently (hides it, if you enable this, make sure to disable kiosk)
    chromeOptions.add_argument('--log-level=3')                    # stops the headless browser's logging features
    chromeOptions.add_argument('blink-settings=imagesEnabled=false') # set loading images to be false (for faster loading)
    chromeOptions.add_argument('--no-sandbox')                     # required when running as root user. otherwise you would get no sandbox errors. 
    chromeOptions.add_argument('--disable-extensions')
    chromeOptions.add_argument('--disable-gpu')
    # chromeOptions.add_argument('--profile-directory=Default')
    # chromeOptions.add_argument("--incognito")
    # chromeOptions.add_argument('--ignore-certificate-errors')
    # chromeOptions.add_argument("--disable-plugins-discovery")
    chromeOptions.page_load_strategy = 'normal'

    return chromeOptions

# Runs the driver
def runDriver(chromeOptions):
    """
    Runs/Open the chrome web driver passing it the chromeOptions options

    Parameters
    ----------
    driver: chromedriver (required)
        the driver that will be scrolled on

    Errors
    ------
    Message : session not created: This version of ChromeDriver only supports Chrome version 81
        Enter the command "sudo apt-get install libsqlite3-dev chromium-driver" on the terminal
        Solution taken from: https://blog.toshima.ru/2019/12/20/fix-chromedriver-only-supports-chrome-version.html   

    Returns
    -------
    object
        selenium.webdriver.Chrome() for further usage and manipulation
    """
    try: # try to open the driver
        driver = webdriver.Chrome('./chromedriver/chromedriver.exe', options=chromeOptions, service_args=['--verbose']) # opens the headless browser for windows
    except Exception as e:
        logging.error('ERROR: Failed to open Chrome Web Driver...\n', e) # outputs the following if it failed to load 
        logError('Error failed to open chrome web driver', '', e)
        input("Press any key to exit...")
        exit()
    return driver # returns the driver for further usage

# Goes to the URL
def getPage(driver, url):
    """
    The driver goes to the page designated by the URL

    Parameters
    ----------
    driver : chromedriver (required)
        the driver that will be used

    url : string (required)
        http url that the driver will be directed to
    """
    try:
        driver.get(url) # gets the URL
    except Exception as e:
        logging.error('\tERROR: Failed to load page ' + url + '\n', e)
        logError('Error loading the page', url, e)

# Close the Driver
def closeDriver(driver):
    """
    Closes the driver

    Parameters
    ----------
    driver : chromedriver (required)
        closes the driver through calling 'driver.close()'
    """
    try:
        driver.close()
    except Exception as e:
        logging.error('ERROR: Something occured while closing the driver...\n', e)
        logError('Error closing the driver', '', e)
