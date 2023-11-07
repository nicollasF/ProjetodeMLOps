import requests

inf = {
    'garagem':2,
    'ano':2008,
    'tamanho':275

}
url = 'http://127.0.0.1:5000/cotacao/'

config = requests.auth.HTTPBasicAuth('admin','password')

resultado =  requests.post(url, json=inf,auth=config)
resultado.json()