import logging
import sys
import time
import urllib.request
import urllib.error

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from settings import (
    EMAIL_INPUT,
    LOG_FORMAT,
    PASSWORD_INPUT,
    SELENIUM_SERVER,
    TIME_BETWEEN_CHECK
)


logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG, stream=sys.stdout)


def internet_on():

    '''
    Test is the network is up.
    '''

    test_url = 'http://www.google.fr'
    try:
        result = urllib.request.urlopen(test_url, timeout=20)
    except urllib.error.URLError:
        return False
    if result.getcode() != 200 or result.geturl() != test_url:
        return False
    return True


def complete_captive_portal():

    '''
    Go to the captive portal and complet the required fields.
    '''

    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")

    driver = webdriver.Remote(
        command_executor=SELENIUM_SERVER,
        desired_capabilities=options.to_capabilities()
    )

    driver.get('http://www.msftconnecttest.com/redirect')
    email = driver.find_element_by_css_selector('input[name="auth_user"]')
    password = driver.find_element_by_css_selector('input[name="auth_pass"]')
    login = driver.find_element_by_css_selector('input[name="accept"]')

    email.send_keys(EMAIL_INPUT)
    password.send_keys(PASSWORD_INPUT)
    login.click()
    driver.quit()

if __name__ == '__main__':
    while True:
        if not internet_on():
            logging.info('internet fuck up')
            try:
                complete_captive_portal()
            except:
                pass
        else:
            logging.info('internet ok')
        time.sleep(TIME_BETWEEN_CHECK)
