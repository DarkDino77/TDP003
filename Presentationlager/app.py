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

# The funktion projects reads search arguments sent to it
# If no input arguments can be read, a relevent standard value is given.
# It then loads the entire database through the data function load
# It then gets all the techniques used in the data base through the data function get_techniques
# it the searches through the data base for the relevant serach argument
# Then it returns a rederd template based on projects.html with the given searchd database technique used and relevent search terms
@app.route("/projects", methods=["POST", "GET"])
def projects():
    if request.method == "POST":
        sort_by = request.form.get("sort_by", 'start_date')
        sort_order = request.form.get("sort_order", 'desc') 
        search = request.form.get("search", None)
        search_fields = request.form.getlist("search_fields")
        techniques = request.form.getlist("technique_box")
    else:
        sort_by = request.args.get("sort_by", 'start_date')
        sort_order = request.args.get("sort_order", 'desc') 
        techniques = request.args.getlist("techniques")
        search = request.args.get("search", None)
        search_fields = request.args.getlist("search_fields")
    
    if not search_fields:
        search_fields = None
    if not techniques:
        techniques = None
    
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



@app.route("/project/<int:index>", methods=["GET"])
def id(index):
    try:
        data_base = data.load("data.json")
        project = data.get_project(data_base, index)        
        return render_template("id.html", project=project)
    except:
        return render_template("error.html", err= "404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.")

@app.errorhandler(Exception)
def not_found(err):
    return render_template("error.html", err= str(err))

if __name__ == '__main__':
   app.run(debug = True)

