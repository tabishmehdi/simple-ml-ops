import os
from flask import Flask,request,render_template,jsonify
import yaml
import joblib
import numpy as np
from prediction_service import prediction

webapp_root = "webapp"

static_dir = os.path.join(webapp_root,"static")
template_dir = os.path.join(webapp_root,"templates")

app = Flask(__name__,static_folder=static_dir,template_folder=template_dir)

##### Route Method
@app.route("/home",methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            if request.form:
                data_req = dict(request.form)
                response = prediction.form_response(data_req)
                return render_template("index.html", response=response)
            elif request.json:
                response = prediction.api_response(request.json)
                return jsonify(response)
        except Exception as e:
            print(e)
            # error = {"error" : "Something went wrong!! Try again."}
            error = {"error" : e}
            return render_template("404.html", error=error)
    else:
        return render_template("index.html")

@app.route("/",methods=["GET", "POST"])
def calculation():
    if request.method == "POST":
        try:
            if request.form:
                data_req = dict(request.form)
                mass = data_req['mass']
                density = data_req['density']
                diameter = data_req['diameter']
                radius = float(diameter) / 2
                vol = float(mass) / float(density)
                vol_one_sphere = 4 / 3 * 3.14 * radius ** 3
                response = vol / vol_one_sphere
                return render_template("calculate.html", response=str(response))
        except Exception as e:
            print(e)
            # error = {"error" : "Something went wrong!! Try again."}
            error = {"error" : e}
            return render_template("404.html", error=error)
    else:
        return render_template("calculate.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
