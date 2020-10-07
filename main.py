import requests
import json

headers1 = {
    'Host': 'www.instagram.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
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
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
    'Accept': '*/*',
    'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    # 'X-CSRFToken': 'gRUbRbU1rdQ4v8OPrn55Ofbrz1V6H1GL',
    'X-Instagram-AJAX': '470fd86be390',
    'X-IG-App-ID': '936619743392459',
    'X-IG-WWW-Claim': '0',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Content-Length': '61',
    'Origin': 'https://www.instagram.com',
    'Connection': 'keep-alive',
    'Referer': 'https://www.instagram.com/accounts/emailsignup/',
    # 'Cookie': 'ig_did=9687644B-7EC1-45D2-858D-2F76BECA1A85; csrftoken=gRUbRbU1rdQ4v8OPrn55Ofbrz1V6H1GL; mid=X3y5sAALAAH7HmAjBAM4nO3exIUZ',
    'TE': 'Trailers'
}

headers_login_to_mail = {
}


def generateClientId():
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
full_name = 'janusz skowyr'
username = 'janusz.skowyr.1234'
password = 'owlcity1'



client_id = generateClientId()
csrf_token, ig_did = generate_csrf_token()

print('client_id (mid): ', client_id)
print('csrf_token: ', csrf_token)
print('ig_did: ', ig_did)


headers1['X-CSRFToken'] = csrf_token
headers1['Cookie'] = f'ig_cb=1; mid={client_id}; csrftoken={csrf_token}; ig_did={ig_did};'

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
    'day': '12',
    'year': '1990'
}
data_send_code = {
    'device_id': ig_did,
    'email': email
}
data_verify_code = {
    'code': '123456',
    'device_id': ig_did,
    'email': email
}


cr_url = 'https://www.instagram.com/accounts/web_create_ajax/attempt/'
code_url = 'https://i.instagram.com/api/v1/accounts/send_verify_email/'
ver_url = 'https://i.instagram.com/api/v1/accounts/check_confirmation_code/'


with requests.session() as ses:
    g = ses.get('https://www.instagram.com/accounts/emailsignup/')

    p1 = ses.post(cr_url, headers=headers1, data=data)
    print('p1 response code: ', p1)
    with open('response1.html', 'w') as f:
        f.write(p1.text)

    p_send_mail = ses.post(code_url, headers=headers_code, data=data_send_code)
    print('p_send_mail response code: ', p_send_mail)
    with open('response2.html', 'w') as f:
        f.write(p_send_mail.text)

    headers_code['Content-Length'] = '126'

    p_verify_code = ses.post(ver_url, headers=headers_code, data=data_verify_code)
    print('p_verify_mail response code: ', p_verify_code)
    with open('response3.html', 'w') as f:
        f.write(p_verify_code.text)

