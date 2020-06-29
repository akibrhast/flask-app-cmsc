from flask import Flask, flash, redirect, render_template, request, session, abort,url_for,jsonify
import cmscExamFunctions

import os

#from flask_login import login_user, current_user, logout_user, login_required #Optional login imports, need to 'pip install flask_login'

app = Flask(__name__)

#function_names=["FloatAnalysisBitsToValue","AsciiParity","ByteOrder","IntegerRepresentation","IntegerAnalysisBitsToValue","GenerateIfCondition"]

test = {"IntegerRepresentation"         :   ["/static/IntegerRepresentation.png","187"],
        "IntegerAnalysisBitsToValue"    :   ["/static/IntegerAnalysisBitsToValue.png","0x04180002"],
        "FloatAnalysisBitsToValue"      :   ["/static/FloatAnalysisBitsToValue.png"," 00100000,00000000,00000000,00000000"],
        "AsciiParity"                   :   ["/static/AsciiParity.png","c + odd||even"],
        "ByteOrder"                     :   ["/static/ByteOrder.png","FDC62D93 + be||le"],
        "CodeIfElseTest"                :   ["/static/CodeIfElseTest.png","if ( X0 == 11 ) {X10 = X0 ;}else {X10 = 11 ;}"]
        }

@app.route('/')
def index():
    
    return render_template("base.html",function_names = test)


@app.route('/search',methods=['POST'])
def search():
    ''' request.get_json() returns a dictionary with the keys "data" and "function_name" 
        data can be a single value or 2 values separated by comma
        e.x: data:  "500"
           : data:  "c,even"  
    '''
    search_query = request.get_json()
    func  = getattr(cmscExamFunctions, search_query['function_name'])
    result = func(search_query['data'])
    return jsonify({'data': render_template('partial.html', object=result)})

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)