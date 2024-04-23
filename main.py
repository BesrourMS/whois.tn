import requests
from bs4 import BeautifulSoup
import json

url = "https://whois.ati.tn/"

payload = "domain=bnb&ext=1&submit=ok&b_existe=Existe%3F"
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'https://registre.tn/',
    'User-Agent': 'insomnia/2023.5.8'
}

cookies = {
    'PHPSESSID': '1oi1k48jki92f6r5lg36cdprv2'
}

response = requests.request("POST", url, headers=headers, data=payload, cookies=cookies)

page = BeautifulSoup(response.text, 'html.parser')

# Selecting the specific div
t = page.select_one('#middle > div')

# Creating a new BeautifulSoup object from the selected div
soup = BeautifulSoup(str(t), 'html.parser')

whois_result = {}

# Extracting domain name and status
domain_name = soup.find('a').text
domain_status = soup.find('strong', style='color:#C00;').text
whois_result['DomainName'] = domain_name
whois_result['DomainStatus'] = domain_status

# Extracting creation date and domain state
details = soup.find_all('ul')
creation_date = details[0].li.text.replace('Date création: ', '')
domain_state = details[1].li.text.replace('Etat domaine: ', '')
whois_result['CreationDate'] = creation_date
whois_result['DomainState'] = domain_state

# Extracting registrar
registrar = details[2].li.a.text
whois_result['Registrar'] = registrar

# Extracting registrant details
registrant_info = details[3:11]
registrant = {}
for info in registrant_info:
    key = info.li.strong.text.replace(':', '').strip()
    value = info.li.text.split(':')[-1].strip()
    registrant[key] = value
whois_result['Registrant'] = registrant

# Extracting administrative contact details
admin_contact_info = details[11:19]
admin_contact = {}
for info in admin_contact_info:
    key = info.li.strong.text.replace(':', '').strip()
    value = info.li.text.split(':')[-1].strip()
    admin_contact[key] = value
whois_result['AdministrativeContact'] = admin_contact

# Extracting technical contact details
tech_contact_info = details[19:27]
tech_contact = {}
for info in tech_contact_info:
    key = info.li.strong.text.replace(':', '').strip()
    value = info.li.text.split(':')[-1].strip()
    tech_contact[key] = value
whois_result['TechnicalContact'] = tech_contact

# Extracting DNS servers
dns_servers = [item.li.text.replace('Nom : ', '') for item in details[-3:-1]]
whois_result['DNSServers'] = dns_servers

# Extracting DNSSEC status
dnssec_status_tag = details[-1].find('li')
dnssec_status = dnssec_status_tag.text.replace('dnssec : ', '') if dnssec_status_tag else "Not Found"
whois_result['DNSSEC'] = dnssec_status


# Convert to JSON
json_result = json.dumps({'WhoisResult': whois_result}, indent=2)
print(json_result)
