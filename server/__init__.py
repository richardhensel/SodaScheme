#from flask import Flask
#app = Flask(__name__)
#@app.route("/")
#def hello():
#    return "Hello, Welcome to Profitbricks!"
#if __name__ == "__main__":
#    app.run()

import pickle
from flask import Flask, request
from flask_restful import Resource, Api
import crypt

app = Flask(__name__)
api = Api(app)

#data_path = "data/"
data_path = "/var/www/Flask/Scheme/data/"

class RegisteredCards(Resource):
    def get(self):
        data = load_obj("purchase_data")
        hashes = data.keys()
        double_hashes = []
        for key in hashes:
            double_hashes.append(get_hash(key))
        return double_hashes

class LogCardTouch(Resource):
    def put(self):
        
        id_hash = request.form['data']
        print request
        print id_hash

        data = load_obj("purchase_data")
        if id_hash in data:
            data[id_hash]["Num_Purchases"] = data[id_hash]["Num_Purchases"] + 1
            save_obj(data, "purchase_data")
            return data[id_hash]['Name'] + ': ' + str(data[id_hash]["Num_Purchases"])
        else:
            return 'card not recognised'

api.add_resource(RegisteredCards, '/getregisteredcards')

api.add_resource(LogCardTouch, '/logcardtouch')

def save_obj(obj, name ):
    with open(data_path + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open(data_path + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def get_hash(raw_id):
    return str(crypt.crypt(raw_id, "$6$").replace("$6$$","").replace(" ",""))

if __name__ == '__main__':
    #app.run(debug=True)
    app.run()
