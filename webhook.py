import urllib
import json
import os
from flask import Flask
from flask import request
from flask import make_response
from pymongo import MongoClient
import regex as re

# Flask app should start in global layout
app=Flask(__name__)
 
@app.route('/webhook',methods=['POST'])
def webhook():
    req=request.get_json(silent=True, force=True)
    print("I was here")
    print("Request")
    print(json.dumps(req,indent=4))
    res=makeWebhookResult(req)
    res=json.dumps(res,indent=4)
    print("I was here --->")
    print(res)
    r=make_response(res)
    r.headers['Content-Type']='application/json'
    print(r)
    
    return r
 
def makeWebhookResult(req):
    if req.get("queryResult").get("action")!="Check_Vendor":
        return {}
    #client = MongoClient('mongodb://localhost:27017/')
    client = MongoClient('mongodb://test:password101@ds125335.mlab.com:25335/supplier')
    
    alpha = req.get("queryResult").get("parameters").get("Vendor_Names")
    alpha = alpha.rstrip()
    alpha = str(alpha)
    print(alpha)
    

    db = client.supplier
    data = db.Vendor_data
    df =data.find({'name': {'$regex':'^' + re.escape(alpha)}})
    mydoc =data.find({'name': {'$regex':'^' + re.escape(alpha)}}).count()
    speech = ' '
    print(mydoc)


    if mydoc!=0:
        if mydoc == 1:
            for item in df:
                if item['name'] == alpha:
                    speech=("The Vendor Exist in Database")
                else:
                    speech = ('Do you mean '+item['name']+' ?')
        else:
            for item in df:
                speech = speech + item['name']+','
            speech = speech+'Which ' + alpha + ' you are talking about ?'
        return{"fulfillmentText":speech,"source":"Check_Vendor"}

    else:
        return{"fulfillmentText":"Vendor Doesn't Exist in the database. Please Register the Vendor using Admin Help or check the Vendor Name you have entered correctly","source":"Check_Vendor"}
 
if __name__=='__main__':
    port=int(os.getenv('PORT',7002))
    print("Starting app on port %d" %(port))
    app.run(debug=True, port = 7002, host='127.0.0.1')
    
