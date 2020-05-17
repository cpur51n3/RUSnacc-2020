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
    html_var = f"{remote_ip}"
    return render_template("index.html", content="Your IP is: {}".format(html_var))


@app.route("/local")
def local():
    remote_ip = request.remote_addr
    return render_template("local.html",
                           location=f"{remote_ip}")

@app.route("/all", methods=["GET","POST"])
def all():
    remote_ip = request.remote_addr
    if request.method == 'GET':
        image_location = generate_image()

    add = ""
    if request.method == 'POST':
        if request.form['submit'] == 'submit_add':
            num1 = [0,0,0,0,0,0]
            num1[0] = request.form['add_num1']
            num1[1] = request.form['add_num2']
            num1[2] = request.form['add_num3']
            num1[3] = request.form['add_num4']
            num1[4] = request.form['add_num5']
            num1[5] = request.form['add_num6']
            num1 = [ int(x) for x in num1]
            num2 = [element * 2 for element in num1]
            add = sum(num1)
            image_location = generate_image(num1,num2)

    r = make_response(render_template("all.html",
                           location=f"{remote_ip}",
                           add = add))
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

def generate_image(form1=[0,1,2,3,4,5],form2=[1,2,3,4,5,6]):
    df = pd.DataFrame({
                        'a': form1,
                        'b': form2,
                        }, index=[1990, 1997, 2003, 2009, 2014, 2019])
    lines = df.plot.line()
    fig = lines.get_figure()
    fig.savefig(full_filename)
    return full_filename

if __name__ == "__main__":
    app.run(debug=True)
