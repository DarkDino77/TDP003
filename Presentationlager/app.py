from flask import Flask, render_template, request, redirect, url_for
import data
from os import getcwd

app = Flask(__name__)
app.static_folder = 'static' 

# Funktion index loads the infromation from info.json using the database function load.
# Retruns a rederder template of index.html with the insent infromation extracted from info.json as infromation_developers
@app.route("/")
def index():
    information_developers = data.load("info.json")
    return render_template("index.html", information_developers = information_developers)

#
@app.route("/projects")
def projects():
    sort_by = request.args.get("sort_by", 'start_date')
    sort_order = request.args.get("sort_order", 'desc') 
    techniques = request.args.getlist("techniques")
    if not techniques:
        techniques = None
    search = request.args.get("search", None)
    search_fields = request.args.getlist("search_fields")
    if not search_fields:
        search_fields = None

    #print("Pass")
    #print(f"sort_by {sort_by}")
    #print(f"sort_order {sort_order}")
    #print(f"techniques {techniques}")
    #print(f"search {search}")
    #print(f"search_fields {search_fields}")

    data_base = data.load("data.json")
    techniques_used = data.get_techniques(data_base)
    data_base = data.search(data_base, sort_by=sort_by, sort_order=sort_order, techniques=techniques, search=search, search_fields=search_fields)
    return render_template("projects.html", data_base = data_base, techniques_used=techniques_used , sort_by_search=sort_by, sort_order_search=sort_order, techniques_search=techniques, search_search=search, search_fields_search=search_fields)

@app.route("/techniques")
def techniques():
    techniques_information_list = data.load("techniques.json")
    techniques_information = techniques_information_list.pop()
    data_base = data.load("data.json")
    techniques_used = data.get_technique_stats(data_base)

    return render_template("techniques.html", techniques_information = techniques_information, techniques_used = techniques_used)

@app.route("/redirect_search", methods=["POST"])
def redirect_search():
    #Läsa in från projects alla filter som search ska ha 
    # och sicka dom till projects i redirect
    sort_by = request.form.get("sort_by")
    sort_order = request.form.get("sort_order") 
    search = request.form.get("search")
    search_fields = request.form.getlist("search_fields")
    techniques = request.form.getlist("technique_box")
    #print(techniques)
    return redirect(url_for("projects",sort_by=sort_by, sort_order=sort_order, techniques=techniques, search=search, search_fields=search_fields))

@app.route("/redirect/<index>", methods=["GET"])
def redirect_techniques(index):
    technique = [index]
    return redirect(url_for("projects",techniques=technique))


@app.route("/project/<index>", methods=["GET"])
def id(index):
    try:
        data_base = data.load("data.json")
        project = data.search(data_base, search=index, search_fields=["project_id"])
        project = project.pop()
        return render_template("id.html", project=project)
    except Exception as err:
        return render_template("404_error.html", type_err=type(err), err= str(err))

@app.errorhandler(404)
def not_found(err):
    return render_template("404_error.html", type_err=type(err), err= str(err))

if __name__ == '__main__':
   app.run(debug = True)

