from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import numpy
import tensorflow as tf
import requests
import subprocess
import json
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.applications import Xception # TensorFlow ONLY
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications import VGG19
from tensorflow.keras.applications import imagenet_utils
from tensorflow.keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
#from keras.preprocessing.image import load_image
from urllib.request import urlopen
from urllib import request as R
import numpy as np
from tensorflow.keras.preprocessing import image
from PIL import Image
from io import BytesIO
from tensorflow.keras.models import load_model
preprocess = preprocess_input

model= load_model('INCEPTION.h5')
InputShape = (299, 299)
def LoadImageFromUrl(URL):
    res = R.urlopen(URL).read()
    res=Image.open(BytesIO(res)).resize(InputShape)
    res= img_to_array(res)
    return res

app = Flask(__name__)
api = Api(app)

client = MongoClient('localhost', 27017)
#client = MongoClient("mongodb://db:27017") docker

db = client.Monapi
utilisateurs = db["Mesutilisateurs"]

def verifier_si_utilisateur_existe(username):
    
    if utilisateurs.find({"Nom":username}).count() == 0:
        return False
    else:
        return True
class Inscription(Resource):
    def post(self):
        reponse_json = request.get_json()
        username = reponse_json ["nom"]
        password = reponse_json ["motdepasse"] 

        if verifier_si_utilisateur_existe(username):
            statusJson = {
                'status':301,
                'message': 'Nom Invalide'
            }
            return jsonify(statusJson )

        hashed_mot_de_passe = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        #Store username and pw into the database
        utilisateurs.insert({"Nom": username,"Motdepasse": hashed_mot_de_passe,
        "Jetons":50})
        statusJson = {'status':200,'message':'Merci de vous être inscrit'}
        return jsonify(statusJson)

def verifierMotdepasse(username, password):
    if not verifier_si_utilisateur_existe(username):
        return False

    hashed_mot_de_passe = utilisateurs.find({
        "Nom":username
    })[0]["Motdepasse"]
    if bcrypt.hashpw(password.encode('utf8'),hashed_mot_de_passe) ==hashed_mot_de_passe:
        return True
    else:
        return False


def genererStatusDictionary(status, message):
    statusJson  = {
        'status': status,
        'message': message
    }
    return statusJson 

def verifier_identite(username, password):
    if not verifier_si_utilisateur_existe(username):
        return genererStatusDictionary(301, 'Nom Invalide'), True

    correct_mot_de_passe = verifierMotdepasse(username, password)

    if not correct_mot_de_passe:
        return genererStatusDictionary(302, 'Mot de passe Incorrect'), True

    return None, False


class Classify_Image(Resource):
    def post(self):
        reponse_json = request.get_json()

        username = reponse_json["nom"]
        password = reponse_json["motdepasse"]
        url = reponse_json["url"]
        image=LoadImageFromUrl(url)
        image= np.expand_dims(image, axis=0)
        image = preprocess(image)
        predictions=model.predict(image)
        #predictions=np.argmax(predictions)
        Proba=imagenet_utils.decode_predictions(predictions,top=3)
        

        statusJson, erreur_type = verifier_identite(username, password)
        if erreur_type:
            return jsonify(statusJson)

        jetons = utilisateurs.find({
            "Nom":username
        })[0]["Jetons"]

        if jetons<=0:
            return jsonify(genererStatusDictionary(303, 'Pas assez de jetons'))
        retJson = {}
        for (i, (imagenetID, label, prob)) in enumerate(Proba[0]):
            retJson[label]="{:.2f}%".format(prob*100)

        utilisateurs.update({
            "Nom": username
        },{
            "$set":{
                "Jetons": jetons-1
            }
        })

        return jsonify(retJson)


class RechargerCompte(Resource):
    #pour recharer son compte l'utlisateur doit utiliser admin comme mot de passe
    def post(self):
        reponse_json  = request.get_json()

        username = reponse_json ["nom"]
        password = reponse_json ["admin"]
        amount = reponse_json ["montant"]

        if not verifier_si_utilisateur_existe(username):
            return jsonify(genererStatusDictionary(301, 'Nom Invalide'))

        correct_pass = "admin"
        if not password == correct_pass:
            return jsonify(genererStatusDictionary(302, 'Mauvais mot de passe'))

        utilisateurs.update({
            "Nom": username
        },{
            "$set":{
                "Jetons": amount
            }
        })
        return jsonify(genererStatusDictionary(200, 'Compte Bien Rechargé.Merci je viens de gagner de argent mdr'))


api.add_resource(Inscription, '/inscription')
api.add_resource(Classify_Image, '/classifier')
api.add_resource(RechargerCompte, '/recharge')

if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)
