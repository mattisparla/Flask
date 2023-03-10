from flask import Flask, render_template, redirect, url_for, request
import sqlite3
import time
import AlphaBot
import hashlib 
import requests

app = Flask(__name__)

bot = AlphaBot.AlphaBot()


def validate(username, password): #semplice funzione di python
    completion = False
    con = sqlite3.connect('./comandi.db')
    #with sqlite3.connect('static/db.db') as con:
    cur = con.cursor() #La chiamata di metodo "cursor()" su un oggetto "con" crea un oggetto
   # cursore che rappresenta la posizione corrente in una tabella di un database. Il cursore viene 
    #utilizzato per eseguire le query sul database e recuperare i risultati.
    cur.execute("SELECT * FROM Utenti")
    rows = cur.fetchall() #viene utilizzato per recuperare tutti i risultati di una query che è stata eseguita sul database
    for row in rows:
        dbUser = row[1]
        dbPass = row[2]
        if dbUser==username:
            completion=check_password(dbPass, password)
    con.close()
    return completion


def check_password(hashed_password, user_password):
    return hashed_password == user_password

@app.route('/', methods=['GET', 'POST'])  #funzioni associate a una risorsa del sito e devono avere quetso decorarartore 
#che mi permette di associare una URL a una funzione python.
#quando il sito ha una richiesta su questa URL flask esegue la funzione associata
#si puo fare che risponde a soli alcuni meotdi di richiesta es [get,post]
def login():
    error = None
    if request.method == 'POST': #invio di username e password
        username = request.form['username'] #arriva da html
        password = request.form['password']
        password=hashlib.sha256(password.encode()).hexdigest()#"hashlib.sha256()" viene utilizzata per creare un oggetto hash SHA-256,
        #che può quindi essere aggiornato con la password in formato di byte tramite il metodo "encode()" e convertito in una stringa di 
        #hash mediante il metodo "hexdigest()".
        completion = validate(username, password)
        if completion ==False:
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('secret')) #url_for -> ottiene la url della funzione secret
        #si fa il redirect a quella url senza conoscere l url
    return render_template('login.html', error=error) #messaggio che puo comparire su html

@app.route('/secret', methods=['GET', 'POST']) #metto un URL dinamica
def secret():
    if request.method == 'POST':
        if request.form.get('action1') == '➡': #per catturare i bottoni
            print("Bottone1")
            #sposta1()
            bot.right()
            time.sleep(0.1)
            bot.stop()
        elif  request.form.get('action2') == '⬅':
            print("Bottone2")
            #sposta2()
            bot.left()
            time.sleep(0.1)
            bot.stop()
        elif  request.form.get('action3') == '⬆':
            print("Bottone3")
            #sposta3()
            bot.forward()
            time.sleep(0.3)
            bot.stop()
        elif  request.form.get('action4') == '⬇':
            print("Bottone4")
            #sposta4()
            bot.backward()
            time.sleep(0.3)
            bot.stop()
        else:
            print("Unknown")
    elif request.method == 'GET':
        return render_template('index.html') #il template "index.html" viene caricato e renderizzato.
    
    return render_template("index.html")

if __name__== "__main__":
    app.run(debug=True, host='192.168.1.143',port=5000)
    #debug =true quando lancio il prgramma e apro la pagina del browser e mi accorogo che ce un errore lo correggo e ricarico il browser
    #host= in verifica 127.0.0.1