import json
import random
import time

import pyperclip
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from proxies import proxies
import requests
import selenium

def getDriver():

    options = webdriver.ChromeOptions()

    options.add_argument("accept-language=en-US")  # set english browser language
    options.add_argument(
        "--disable-blink-features=AutomationControlled")  # disables "automated" pop-up, also helps not getting detected (or not), doesnt work hehe
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options, executable_path='C:\Python\chromedriver.exe')

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
    driver.execute_script("return navigator.userAgent;")
    driver.delete_all_cookies()

    return driver


headers = {
    'Host': 'www.instagram.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'X-CSRFToken': '',
    'X-Instagram-AJAX': '470fd86be390',
    'X-IG-App-ID': '936619743392459',
    'X-IG-WWW-Claim': '0',
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Length': '384',
    'Origin': 'https://www.instagram.com',
    'Connection': 'keep-alive',
    'Referer': 'https://www.instagram.com/accounts/emailsignup/',
    'Cookie': '',
    'TE': 'Trailers'
}

headers_code = {
    'Host': 'i.instagram.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'X-CSRFToken': '',
    'X-Instagram-AJAX': '470fd86be390',
    'X-IG-App-ID': '936619743392459',
    'X-IG-WWW-Claim': '0',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Content-Length': '61',
    'Origin': 'https://www.instagram.com',
    'Connection': 'keep-alive',
    'Referer': 'https://www.instagram.com/accounts/emailsignup/',
    'Cookie': '',
    'TE': 'Trailers'
}


def generate_client_id():
    url = 'https://www.instagram.com/web/__mid/'

    with requests.session() as ses:
        g = ses.get(url)
        return g.text


def generate_csrf_token():
    url = 'https://www.instagram.com/data/shared_data/?__a=1'

    with requests.session() as ses:
        g = ses.get(url)

        json_response = json.loads(g.text)
        csrf_token = json_response['config']['csrf_token']
        ig_did = json_response['device_id']
    return csrf_token, ig_did

email = 'janusz.skowyr@o2.pl'
full_name = 'janusz skowyr2'
username = 'janusz.skowyr.222'

client_id = generate_client_id()
csrf_token, ig_did = generate_csrf_token()

print('client_id (mid): ', client_id)
print('csrf_token: ', csrf_token)
print('ig_did: ', ig_did)


headers['X-CSRFToken'] = csrf_token
headers['Cookie'] = f'ig_cb=1; mid={client_id}; csrftoken={csrf_token}; ig_did={ig_did};'

headers_code['X-CSRFToken'] = csrf_token
headers_code['Cookie'] = f'mid={client_id}; csrftoken={csrf_token}; ig_did={ig_did};'


data = {
    'email': email,
    'enc_password': '#PWD_INSTAGRAM_BROWSER:10:1602024788:AXlQABuVy/rCsRztKdkOtDtS25flS2eH5HMggtqSnYI31gQ8Kl9Z3gQ3XUgxHnuIjqdtnBHOvDexmb2xmILEr2L87vOElD1cXEvBejMk9cFE91/HM0JP4X/vqAzdvwHUsTWszieoiLQKDRhJ',
    'username': username,
    'first_name': full_name.replace(' ', '+'),
    'client_id': client_id,
    'seamless_login_enabled': '1',
    'opt_into_one_tap': 'false',
    'month': '7',
    'day': '18',
    'year': '2000'
}

data2 = {
    'email': email,
    'enc_password': '#PWD_INSTAGRAM_BROWSER:10:1602024788:AXlQABuVy/rCsRztKdkOtDtS25flS2eH5HMggtqSnYI31gQ8Kl9Z3gQ3XUgxHnuIjqdtnBHOvDexmb2xmILEr2L87vOElD1cXEvBejMk9cFE91/HM0JP4X/vqAzdvwHUsTWszieoiLQKDRhJ',
    'username': username,
    'first_name': full_name.replace(' ', '+'),
    'month': '7',
    'day': '18',
    'year': '2000',
    'client_id': client_id,
    'seamless_login_enabled': '1'
}

data_send_code = {
    'device_id': ig_did,
    'email': email
}

data_verify_code = {
    'code': '',
    'device_id': ig_did,
    'email': email
}

cr_url = 'https://www.instagram.com/accounts/web_create_ajax/'
code_url = 'https://i.instagram.com/api/v1/accounts/send_verify_email/'
ver_url = 'https://i.instagram.com/api/v1/accounts/check_confirmation_code/'


# selenium part
# mail_url = 'https://temp-mail.org/pl/'
# driver = getDriver()
# random_mail = ''
#
# try:
#     driver.get(mail_url)
#     # inside the second tab
#     reset_button = WebDriverWait(driver, 8).until(
#         EC.presence_of_element_located((By.ID, 'click-to-delete')))
#     reset_button.click()
#
#     time.sleep(5)
#
#     # copy email to clipboard
#     ActionChains(driver).move_to_element(driver.find_element_by_id('click-to-copy')).click().perform()
#     random_mail = pyperclip.paste()
# except Exception as e:
#     print(e)
#     driver.quit()
#
# data['email'] = data_send_code['email'] = data_verify_code['email'] = random_mail
#
# print('random_mail: ', random_mail)

with requests.session() as ses:
    proxy_choice = random.choice(proxies)
    proxy = {"http": proxy_choice, "https": proxy_choice}
    print("proxy:", proxy)


    p1 = ses.post(cr_url, headers=headers, data=data, proxies=proxy)
    print('p1 response code: ', p1)
    with open('response1.html', 'w') as f:
        f.write(p1.text)

    time.sleep(3)

    # p2 = ses.post(cr_url, headers=headers, data=data2)
    # print('p2 response code: ', p2)
    # with open('response2.html', 'w') as f:
    #     f.write(p2.text)

    time.sleep(3)

    p_send_mail = ses.post(code_url, headers=headers_code, data=data_send_code, proxies=proxy)
    print('p_send_mail response code: ', p_send_mail)
    with open('response3.html', 'w') as f:
        f.write(p_send_mail.text)


    # #getting activation code from random mail
    #
    # # wait for 2 minutes for mail to read activation code from it
    # WebDriverWait(driver, 120).until(
    #     EC.presence_of_element_located(
    #         (By.XPATH, '/html/body/main/div[1]/div/div[3]/div[2]/div/div[1]/div/div[4]/ul/li[2]/div[1]')))
    #
    # # open mail
    # ActionChains(driver).move_to_element(driver.find_element_by_xpath(
    #     '/html/body/main/div[1]/div/div[3]/div[2]/div/div[1]/div/div[4]/ul/li[2]/div[1]/a')).click().perform()
    #
    # # get activation code from the mail
    # _mail_code = WebDriverWait(driver, 5).until(
    #     EC.presence_of_element_located((By.XPATH,
    #                                     '//*[@id="email_content"]/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td[2]'))
    # ).text
    #
    # data_verify_code['code'] = _mail_code
    #
    # print("_mail_code:", _mail_code)

    # driver.quit()

    data_verify_code['code'] = input("enter activation code from mail: ")

    headers_code['Content-Length'] = '126'

    p_verify_code = ses.post(ver_url, headers=headers_code, data=data_verify_code, proxies=proxy)
    print('p_verify_mail response code: ', p_verify_code)
    with open('response4.html', 'w') as f:
        f.write(p_verify_code.text)
