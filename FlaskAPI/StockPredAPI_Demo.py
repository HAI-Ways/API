from flask import Flask
from flask import request
import pickle
import pandas as pd


stockAPI = Flask(__name__)

@stockAPI.route('/demo',methods=['GET'])

def index():
	fld='C:/Users/hmxu/Desktop/ML/Stock/'           #path to the model and testing data
	modelFl=fld+'stock_Pred_Model_v07190216.pkl'    #path to the saved model 
	ivvJson=fld+'stockLatest.json'                  #path to testing data
	reqSym=request.args.get('symbol')               #get parameter value from url
	reqSym=reqSym.strip().upper()                   #transform parameter value
	
	if reqSym =='IVV':                              #the model is trained only with IVV data in this demo
		model_loaded = pickle.load(open(modelFl, 'rb'))       #load the model
		loadData=pd.read_json(ivvJson)                        #load testing data
		selData=loadData[loadData['symbol']==reqSym].iloc[:,:-1]     #filter data with user requested stock symbol
		result = model_loaded.predict(selData)                       #make a predict 
		pred=str(result[0])
		prob=model_loaded.predict_proba(selData)
		probl=str(prob.max())
		postBk='Prediction for '+reqSym+': '+pred+'. Probability: '+ probl                    
	else:
		postBk ='Sorry. The symbol you requested is not in our demo yet.'     #deal with error message
	return postBk                                                           #post prediction data back to users


if __name__ == '__main__':
    stockAPI.run()                               #run the app
    
#save this API file as StockPredAPI_v04190217.py or your favorite name   
#to test this API, open cmd in windows. cd to the folder that holds the API. run the API with command python StockPredAPI_v04190217.py
#paste this url to your browser. http://127.0.0.1:5000/demo?symbol=ivv
#deploy the API to ASW following the guide here.
#https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html
http://flask.pocoo.org/docs/1.0/deploying/
#access API through javascript/Ajax or other programs
