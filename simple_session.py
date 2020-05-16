from flask import Flask, redirect, url_for, render_template, request, make_response
import datetime
import os
import json
import pandas as pd
import matplotlib

# Path for test image
photo_folder = os.path.join('static')
full_filename = os.path.join(photo_folder, 'sample.png')


app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"

with open('webpage_strings.json', 'r') as file1:
    data = file1.read()
data = json.loads(data)
page_strings = data['page_strings']


@app.route("/")
def index():
    return render_template("index.html", content="{}".format(datetime.datetime.now()))


@app.route("/home")
def home():
    referrer = request.headers.get("Referer")
    remote_ip = request.remote_addr
    if "127.0.0.1" in remote_ip:
        html_var = f"{remote_ip}, welcome home!"
    elif "192.168" in remote_ip:
        html_var = f"{remote_ip}, hello neighbour!"
    else:
        html_var = f"{remote_ip}"
    return render_template("index.html", content="Your IP is: {}".format(html_var))


@app.route("/local")
def local():
    remote_ip = request.remote_addr
    return render_template("local.html",
                           location=f"{remote_ip}")

@app.route("/all", methods=["GET"])
def all():
    remote_ip = request.remote_addr
    if request.method == 'GET':
        image_location = generate_image()
    r = make_response(render_template("all.html",
                           location=f"{remote_ip}"))
    r.headers.set("Cache-Control 'no-cache, no-store'", "Pragma 'no-cache'")
    return r

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'no-cache, no-store'
    response.headers['Pragma'] = 'no-cache'
    return response

# @app.route("/dcp_connection")
# def all():
#     return render_template("dcp.html",
#                            header_string="Distributed Computing Protocol",
#                            content="{}".format(page_strings['dcp_worker_string']),
#                            which_action=page_strings['worker_action'],
#                            which_action_desc=page_strings['worker_action_desc'])

def generate_image():
    df = pd.DataFrame({
                        'a': [20, 18, 11, 615, 113],
                        'b': [4, 25, 11, 602, 123]
                        }, index=[1990, 1997, 2003, 2009, 2014])
    lines = df.plot.line()
    fig = lines.get_figure()
    fig.savefig(full_filename)
    return full_filename

if __name__ == "__main__":
    app.run(debug=True)