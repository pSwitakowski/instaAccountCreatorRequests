import requests
import json
import pprint

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'X-Instagram-AJAX': 'cc6f59f85f33',
    'X-IG-App-ID': '936619743392459',
    'X-IG-WWW-Claim': '0',
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://www.instagram.com',
    'Connection': 'keep-alive',
    'Referer': 'https://www.instagram.com/accounts/emailsignup/',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}
# csrftoken
# ig_did
# mid
# limit = 1
# name
# email
# username
# proxy_file


def generateClientId():
    url = 'https://www.instagram.com/web/__mid/'

    with requests.session() as ses:
        g = ses.get(url)
        return g.text

# private function generateCsrfToken($proxy = null): bool
# 	{
# 		$strUrl = 'https://www.instagram.com/data/shared_data/?__a=1';
#
# 		$ch = curl_init();
# 		curl_setopt($ch, CURLOPT_URL, $strUrl);
# 		curl_setopt($ch, CURLOPT_USERAGENT, $this->user_agent);
# 		if ($proxy)
# 		{
# 			curl_setopt($ch, CURLOPT_PROXYTYPE, CURLPROXY_SOCKS5);
# 			curl_setopt($ch, CURLOPT_PROXY, $proxy);
# 		}
# 		curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
# 		$result = curl_exec($ch);
# 		curl_close($ch);
#
# 		$json = json_decode($result, true);
#
# 		$this->csrftoken = $json['config']['csrf_token'];
# 		$this->ig_did    = $json['device_id'];
#
# 		return true;
# 	}

def generate_csrf_token():
    url = 'https://www.instagram.com/data/shared_data/?__a=1'

    with requests.session() as ses:
        g = ses.get(url)

        json_response = json.loads(g.text)
        csrf_token = json_response['config']['csrf_token']
        ig_did = json_response['device_id']
    return csrf_token, ig_did


email = 'puste271@wp.pl'
full_name = 'janusz skowyr'
username = 'janusz.skowyr.123'
password = '123456!@#$%^'



client_id = generateClientId()
csrf_token, ig_did = generate_csrf_token()

headers['X-CSRFToken'] = csrf_token
headers['Cookie'] = f'ig_cb=1; mid={client_id}; csrftoken={csrf_token}; ig_did={ig_did}; rur=FRC'

data = {
    'email': email,
    'enc_password': '#PWD_INSTAGRAM_BROWSER:10:1601968787:AWRQAJGc3u2QxZavxESOD1qdtjFTxSh2ylt60Hv98r8X+2B4QOUJsNOm8wD0Auz6LzADM2OEVl68RhQY1wBuW9TX9Z8h9f+e209xX5Yd2HLaqzj7KPOaSshD8j9iS6sFFi8GthKr8Zsx0xRg',
    'password': 'owlcity1',
    'username': username,
    'first_name': full_name.replace(' ', '+'),
    'client_id': client_id,
    'seamless_login_enabled': '1',
    'opt_into_one_tap': 'false',
    'month': '7',
    'day': '12',
    'year': '1990'
}

cr_url = 'https://www.instagram.com/accounts/web_create_ajax/attempt/'
with requests.session() as ses:
    p = ses.post(cr_url, headers=headers, data=data)
    print(p)
    with open('response.html', 'w') as f:
        f.write(p.text)

# print('client id:', client_id)
# print('csrf_token:', csrf_token)
# print('ig_did:', ig_did)



