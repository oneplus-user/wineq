from flask import Flask, render_template, request, jsonify
import os
import yaml
import joblib
import numpy as np
from prediction_service import prediction


webapp_root = "webapp"
static_dir = os.path.join(webapp_root, "static")
template_dir = os.path.join(webapp_root, "templates")

app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)

params_path = "params.yaml"
def read_params(params_path):
    with open(params_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def predict(data):
    config = read_params(params_path)
    model_dir_path = config["webapp_model_dir"]
    model = joblib.load(model_dir_path)
    prediction = model.predict(data)
    print(prediction)
    return prediction[0]

def form_or_api_response(dict_request):
    try:
        data = dict_request.values()
        data = [list(map(float, data))]
        response = predict(data)
        return response
    except Exception as e:
        print(e)
        error = {"error": "Something went wrong!! Try again later!"}
        return error  

@app.route("/", methods=["GET", "POST"])
def index():
    if (request.method == "POST")&(len(request.data)>0):
        try:
            if request.form:
                dict_req = dict(request.form)
                response = form_or_api_response(dict_req)
                # return jsonify(response)                                #for POSTMAN
                return render_template("index.html", response=response)   #for Browser-based app
            elif request.json:
                dict_req = request.json
                response = form_or_api_response(dict_req)
                return jsonify(response)                                  #for POSTMAN (only option)
            
        except Exception as e:
            print(e)
            error = {"error": "Something went wrong!! Try again later!"}
            return render_template("404.html", error=error)
    else:
        # return jsonify("It is LIVE")                #for POSTMAN
        return render_template("index.html")        #for Browser-based app


# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         # pass
#         try:
#             if request.form:
#                 dict_req = dict(request.form)
#                 response = prediction.form_response(dict_req)
#                 #return jsonify(response)   #for POSTMAN
#                 return render_template("index.html", response=response) #for Browser-based app
#             elif request.json:
#                 response = prediction.api_response(request.json) #for POSTMAN
#                 return jsonify(response)

#         except Exception as e:
#             print(e)
#             error = {"error": "Something went wrong!! Try again later!"}
#             # error = {"error": e}

#             return render_template("404.html", error=error)
#     else:
#         return render_template("index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
