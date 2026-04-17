from flask import Flask,request,redirect,url_for
import json

app = Flask(__name__)

db = {}

@app.route('/', methods=['GET'])
def main():
    # ritorna una stringa e lo status code 200 (OK)
    # return 'Hello World!', 200
    return redirect(url_for('static', filename='index.html'))

@app.route('/login', methods=['POST'])
def login():
    return redirect(url_for('static', filename='graph.html'))

@app.route('/graph', methods=['GET'])
def graph():
    # ritorna un url che punta alla pagina statica graph.html
    return redirect(url_for('static', filename='graph.html'))


# il database è pensato come lista di coppie (data, val) per ogni sensore
@app.route('/sensors',methods=['GET'])
def sensors():
    return json.dumps(list(db.keys())), 200

# queste funzioni sensor servono per gestire i dati dei sensori, 
# aggiungere nuovi dati e restituire i dati esistenti con un formato json 
@app.route('/sensors/<s>',methods=['POST'])
# questa funzione permette di inviare valori del senso
def add_data(s):
    data = request.values['data']
    val = float(request.values['val'])
    if s in db:
        db[s].append((data,val))
    else:
        db[s] = [(data,val)]
    return 'ok',200

# si crea una lista con tutti i valori del sensore s, con il formato [[0,val0],[1,val1],...],
# dove val0 è il primo valore del sensore s, val1 è il secondo valore, ecc.
@app.route('/sensors/<s>',methods=['GET'])
def get_data(s):
    if s in db:
        # return json.dumps(db[s])
        r = []
        for i in range(len(db[s])):
            r.append([i,db[s][i][1]])
        return json.dumps(r),200
    else:
        return 'sensor not found',404


if __name__ == '__main__':
    # fa partire l'applicazione Flask
    app.run(host='0.0.0.0', port=80, debug=True)
