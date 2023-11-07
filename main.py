from flask import Flask, request, jsonify
from textblob import TextBlob
import pandas as pd
from flask_basicauth import BasicAuth
from sklearn.linear_model import LinearRegression
import pickle

#pip install -r requirements.txt

#Criacao do modelo no notebook
'''df = pd.read_csv('casas.csv')
df.head(2)
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np

SEED = 123
np.random.seed(SEED)

x = df.drop(columns=['ano','garagem','preco'])
y = df['preco']

train_x, test_x, train_y, test_y = train_test_split(x,y, test_size=0.3)

modelo = LinearRegression()
modelo.fit(train_x, train_y)'''
#FIM


df_colunas = ['tamanho','ano','garagem']

modelo = pickle.load(open('modelo.sav','rb'))

#começo do script para API
app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'admin' #usuario precisa passar essa informações onde for solicitado no end_point
app.config['BASIC_AUTH_PASSWORD'] = 'password' #usuario precisa passar essa informações onde for solicitado no end_point

basic_auth = BasicAuth(app)

@app.route('/')
def home():
    return 'Minha primeira API'

@app.route('/sentimento/<frase>')
@basic_auth.required             #chama a instacia configurada para solicitação de acesso
def sentimento(frase):
    tb = TextBlob(frase)
    tb_en = tb.translate(from_lang='pt', to='en')
    polaridade = tb_en.sentiment.polarity
    return "polaridade {}".format(polaridade)

@app.route('/cotacao/', methods=['POST'])
@basic_auth.required 
def calculocasa():
    valores = request.get_json()
    colunas_valores = [valores[col] for col in df_colunas] #para coluna que vem do get_json, colocamos em ordem correta
    preco = modelo.predict([colunas_valores]) #predicao do json
    return jsonify(preco=preco[0]) #para simplificar a comunicação web, como os dados chegaram em json mandamos em json tbm

app.run(debug=True)