#!/usr/bin/env python

import urllib
import json
import os
import sympy
from sympy import symbols,init_session,sympify,integrate
from sympy import *
from sympy.abc import x,y,z
from sympy.core.sympify import kernS
from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") == "solve":
        result = req.get("result")
        parameters = result.get("parameters")
        eq_name = parameters.get("equation_name")
        query = result.get("resolvedQuery")
        eq = query.split(" ")
        symbol = parameters.get("symbols")

        intent = result.get("metadata").get("intentName")
        types = {'Differentiate':'2','Integrate':'3','Solve':'4'}



        if str(types[eq_name])=="2":
            expr = sympify(eq[1])
            speech = str(diff(expr,x))


        if str(types[eq_name])=="3":
            expr = sympify(eq[1])
            speech = str(integrate(expr,x))

        if str(types[eq_name])=="4":
            speech = "lol" + str(len(eq))
            if len(eq)==6:
                expr1 = sympify(eq[1])
                expr2 = sympify(eq[3])
                var = linsolve([expr1,expr2],(x,y))
                speech = "x = "+str(list(var)[0][0])+ " y = "+str(list(var)[0][1])
            #speech = str(expr1)+","+str(expr2)
            if len(eq)==8:
                expr1 = sympify(eq[1])
                expr2 = sympify(eq[3])
                expr3 = sympify(eq[5])
                var = linsolve([expr1,expr2,expr3],(x,y,z))
                speech = "x = "+str(list(var)[0][0])+ " y = "+str(list(var)[0][1])+ "z = "+str(list(var)[0][2])








    elif req.get("result").get("action") == "operate":
        result = req.get("result")
        parameters = result.get("parameters")
        op_name = parameters.get("operation_name")
        query = result.get("resolvedQuery")
        op = query.split(" ")
        intent = result.get("metadata").get("intentName")
        cost = {'solve':'2','compute':'3','evaluate':'4'}

        speech = str(sympify(op[1]))

    else:
        return {}

    print("Response:")
    print(speech)
    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        #"contextOut": [],
        "source": intent
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 80))

    print ("Starting app on port %d" %(port))

    app.run(debug=True, port=port, host='0.0.0.0')
