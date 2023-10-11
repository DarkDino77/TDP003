from flask import Flask, render_template, request, redirect, url_for
import data, re, os, logging, datetime

app = Flask(__name__)
app.static_folder = 'static'

# Function index loads the infromation from info.json using the database function load.
# Retruns a rederder template of index.html with the insent infromation extracted from info.json as infromation_developers
@app.route("/")
def index():
    log("DEBUG", "Fetching index", request)
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
    log("DEBUG", "Fetching projects", request)
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
    log("DEBUG", "Fetching techniques", request)
    techniques_information_list = data.load("techniques.json")
    techniques_information = techniques_information_list.pop()
    data_base = data.load("data.json")
    techniques_used = data.get_technique_stats(data_base)

    return render_template("techniques.html", techniques_information = techniques_information, techniques_used = techniques_used)



@app.route("/project/<int:index>", methods=["GET"])
def project(index):
    log("DEBUG", "Fetching a project", request)
    try:
        project = data.get_project(data.load("data.json"), index)
        project_folder = app.static_folder + "/projects/" + str(project["project_id"]) + "/"
        project_static = "projects/" + str(project["project_id"]) + "/"
        
        # Not very elegant :v
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
        log("WARNING", f"Failed to fetch a project ({index})", request)
        return not_found("You seem a little lost. This project does not exist in our files. Did you enter the correct URL?")

# Error handling
@app.errorhandler(404)
def not_found(err_message):
    log("WARNING", "404 Not found", request)
    return render_template("error.html",
                           err_header = "404 Not found!",
                           err_message = str(err_message),
                           image = url_for('static', filename = "style/404_not_found.png"))

@app.errorhandler(Exception)
def generic_error(err_message = ""):
    log("ERROR", "Unhandled exception", request)
    return render_template("error.html", err_message = str(err_message))

# Server logging
# Parameters:
# level: A fully capitlized string with the error level (DEBUG, INFO, WARNING, ERROR)
    # If level is invalid, it defaults to info
# message: A string literal containing the log message
# source: The connection metadata (contains e.g. host IP)
# Returns: nothing
def log(level: str, message: str, source: request = ""):
    # Define colors
    # Info is white
    color_debug = '\033[96m'
    color_warning = '\033[93m'
    color_error = '\033[91m'
    color_end = '\033[0m'
    text_bold = '\033[1m'

    # Extract client IP adress
    source_string = ""
    if source != "":
        source_string = f" [{source.remote_addr}]"

    match (level): # Print error message
        case 'DEBUG': print(f"{text_bold}{color_debug}DEBUG{source_string}: {color_end}"     + color_debug   + message + color_end)
        case 'WARNING': print(f"{text_bold}{color_warning}WARNING{source_string}: {color_end}" + color_warning + message + color_end)
        case 'ERROR': print(f"{text_bold}{color_error}ERROR{source_string}: {color_end}"     + color_error   + message + color_end)
        case _: print(f"INFO{source_string}: {message}"); level = "INFO" # Default and info level
    
    # Print error to file
        # Format is: [DATE & TIME] LOGLEVEL [HOST IP]: MESSAGE
    with open("log.md", 'a') as logfile:
        logfile.write(f"[{datetime.datetime.now().isoformat(' ', 'seconds')}] {level}{source_string}: {message}\n")
        logfile.close()

if __name__ == '__main__':
   app.run(debug = True)