from flask import Flask, render_template, request, redirect, url_for
import data

app = Flask(__name__)


@app.route("/")
def index():
    information_developers = data.load("info.json")
    return render_template("index.html", information_developers = information_developers)

@app.route("/projects")
#ta in alla search filter
def projects(sort_by='start_date', sort_order='desc', techniques=None, search=None, search_fields=None):
    
    data_base = data.load("data.json")
    data_base = data.search(data_base, sort_by=sort_by, sort_order=sort_order, techniques=techniques, search=search, search_fields=search_fields)
    return render_template("projects.html", data_base = data_base)

@app.route("/techniques")
def techniques():
    techniques_information_list = data.load("techniques.json")
    techniques_information = techniques_information_list.pop()
    data_base = data.load("data.json")
    techniques_used = data.get_technique_stats(data_base)

    return render_template("techniques.html", techniques_information = techniques_information, techniques_used = techniques_used)
"""
@app.route("/remove/<data_base>", methods=["GET"])
def remove(data_base):
    data_base.pop(0)
    return redirect(url_for("projects", data_base = data_base))   
"""
@app.route("/add", methods=["POST"])
def add(sort_by='start_date', sort_order='desc', techniques=None, search=None, search_fields=None):
    #Läsa in från projects alla filter som search ska ha 
    # och sicka dom till projects i redirect
    return redirect(url_for("projects",sort_by=sort_by, sort_order=sort_order, techniques=techniques, search=search, search_fields=search_fields))

@app.route("/project/id")
def id():
    return render_template("project/id.html", )


if __name__ == '__main__':
   app.run(debug = True, port=5000)

