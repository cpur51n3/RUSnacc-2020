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
        social_distance = []
        for i in range(28):
            social_distance.append(i)
        overdose_impact = calculate_medical_impact(1,200,18, 2.4,'overdose')
        covid_impact = calculate_medical_impact(1,200,18, 2.4,'covid')
        generate_image(covid_impact,overdose_impact,social_distance)

    if request.method == 'POST':
        if request.form['submit'] == 'submit_add':
            num1 = [0,0,0,0,0,0]
            num1[0] = request.form['add_num1']
            num1[1] = request.form['add_num2']
            num1[2] = request.form['add_num3']
            num1[3] = request.form['add_num4']
            num1 = [float(i) for i in num1]
            social_distance = []
            for i in range(28):
                social_distance.append(i)
            overdose_impact = calculate_medical_impact(num1[0],num1[1],num1[2],num1[3],'overdose')
            covid_impact = calculate_medical_impact(num1[0],num1[1],num1[2],num1[3],'covid')
            generate_image(covid_impact,overdose_impact,social_distance)

    r = make_response(render_template("all.html",
                           location=f"{remote_ip}"))
    r.headers.set("Cache-Control 'no-cache, no-store'", "Pragma 'no-cache'")
    return r

@app.after_request
def add_header(response):
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

def generate_image(covid_impact, overdose_impact, social_distance):
    df = pd.DataFrame({
                        'covid_impact': covid_impact,
                        'overdose_impact': overdose_impact,
                        }, index=social_distance)
    lines = df.plot.line()
    lines.set_xlabel("Social distance (every 1/4 meter)")
    lines.set_ylabel("Medical service impact (1 unit/day of treatment)")
    fig = lines.get_figure()
    fig.savefig(full_filename)
    return full_filename

def calculate_medical_impact(locations, avg_space, hours, social_distance, covid_or_overdose):
    impact_projection = []
    A = social_distance
    space = locations*avg_space
    norm = 500
    for S in range(28):
        infected =0.001*60*(A-S)
        critical_covid = 0.25*infected
        mild_covid = 0.75*infected
        overdose = norm - (hours/3)*(space/A)
        overdose = overdose*0.3
        if covid_or_overdose == 'overdose':
            impact_projection.append(int(2*overdose))
        elif covid_or_overdose == 'covid':
            impact_projection.append(int(14*mild_covid + 35*critical_covid))
    return impact_projection

if __name__ == "__main__":
    app.run(debug=True)
