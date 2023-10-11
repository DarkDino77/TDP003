from flask import Flask, render_template, request, redirect, url_for
import data, re, os, logging

app = Flask(__name__)
app.static_folder = 'static'

# Function index loads the infromation from info.json using the database function load.
# Retruns a rederder template of index.html with the insent infromation extracted from info.json as infromation_developers
@app.route("/")
def index():
    information_developers = data.load("info.json")
    return render_template("index.html", information_developers = information_developers)

# The function projects reads search arguments sent to it
# If no input arguments can be read, a relevent standard value is given.
# It then loads the entire database through the data function load
# It then gets all the techniques used in the data base through the data function get_techniques
# It then searches through the database for the relevant serach argument
# Then it returns a rendered template based on projects.html with the given searched database, techniques used and relevent search terms
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

    data_base = data.search(data.load("data.json"),
                            sort_by = sort_by, 
                            sort_order = sort_order, 
                            techniques = techniques, 
                            search = search, 
                            search_fields = search_fields)
    
    techniques_used = data.get_techniques(data_base)
    return render_template("projects.html",
                           data_base = data_base,
                           techniques_used = techniques_used,
                           sort_by_search = sort_by,
                           sort_order_search = sort_order,
                           techniques_search = techniques,
                           search_search = search,
                           search_fields_search = search_fields)

@app.route("/techniques")
def techniques():
    techniques_information_list = data.load("techniques.json")
    techniques_information = techniques_information_list.pop()
    data_base = data.load("data.json")
    techniques_used = data.get_technique_stats(data_base)

    return render_template("techniques.html", techniques_information = techniques_information, techniques_used = techniques_used)



@app.route("/project/<int:index>", methods=["GET"])
def project(index):
    try:
        data_base = data.load("data.json")
        project = data.get_project(data_base, index)
        project_folder = app.static_folder + "/projects/" + str(project["project_id"]) + "/"
        project_static = "projects/" + str(project["project_id"]) + "/"
        
        # Not very elegant :<
        # Check if the entry has content and replace it with a notice if not
        if os.path.isfile(app.template_folder + "/project_templates/" + project["long_description"]):
            project["long_description"] = "/project_templates/" + project["long_description"]
        else:
            project["long_description"] = "/project_templates/does_not_exist.html"
        
        # Check if the entry has a big or small image to display, otherwise display a placeholder image
        if not os.path.isfile(project_folder + project["big_image"]):
            if os.path.isfile(project_folder + project["small_image"]):
                project["big_image"] = url_for('static', filename = (project_static + project["small_image"]))
            else:
                project["big_image"] = url_for('static', filename = "style/placeholder.jpg")
        else:
            project["big_image"] = url_for('static', filename = (project_static + project["big_image"]))
        
        return render_template("project.html", project = project)
    except: # Fallback error page
        return not_found("You seem a little lost. This project does not exist in our files. Did you enter the correct URL?")

# Error handling
@app.errorhandler(404)
def not_found(err_message):
    return render_template("error.html", err_header = "404 Not found!", err_message = str(err_message), image = url_for('static', filename = "style/404_not_found.png"))

@app.errorhandler(Exception)
def generic_error(err_message):
    return render_template("error.html", err_message = str(err_message))

if __name__ == '__main__':
   app.run(debug = True)