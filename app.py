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

                radio_mass_options = data_req['options']
                radio_diameter_options = data_req['diameter']

                mass = float(data_req['mass'])
                density = float(data_req['density'])
                diameter = float(data_req['diameterradius'])

                if radio_mass_options == 'microgram':
                    mass = mass * 0.000001
                elif radio_mass_options == 'milligram':
                    mass = mass * 0.001
                else:
                    mass = mass

                radius = diameter / 2
                if radio_diameter_options == 'nanometer':
                    radius = radius * 0.0000001
                elif radio_diameter_options == 'micrometer':
                    radius = radius * 0.0001
                elif radio_diameter_options == 'millimeter':
                    radius = radius * 0.1
                else:
                    radius = radius
                vol = mass / density
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
