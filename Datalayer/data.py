import json
import re
import os
# Opening JSON file
def load(file):
    if os.path.isfile(file):
        with open(file) as json_file:
            data = json.load(json_file)
            return data
    return None

def get_project_count(db):
    return len(db)

def get_project(db, project_id):
    return next((element for element in db if element['project_id'] == project_id), None)   

def get_techniques(db):
    temp = []
    # Finds the techniques_used in list
    for dictonary in db:
        for techniques_used in dictonary["techniques_used"]:
           #extracts techniques_used to new list
            if techniques_used not in temp:
                temp.append(techniques_used)
    # sorterar listan i lexicographical order.
    return sorted(temp)

def get_technique_stats(db):
    temp = {}
    # Finds the techniques_used in list
    for dictonary in db:
        for technique in dictonary["techniques_used"]:
            if technique not in temp:
                temp[technique] = [{"id": dictonary["project_id"], "name": dictonary["project_name"]}]
            else:
                temp[technique].append({"id": dictonary["project_id"], "name": dictonary["project_name"]})
    return temp

def search(db, sort_by = 'project_name', sort_order = 'desc', techniques_used = [], search = "", search_fields = None): # What is search_fields for?!

    # Only parse techniques if asked to
    if len(techniques_used) > 0:
        filtered_db = [] # A new list of projects with qualified search results
        for project in db:
            for attribute in range(len(project)): # Iterate over all attributes
                if list(project.keys())[attribute] == "techniques_used": # Find the techniques_used attribute
                    for technique in project.get(list(project.keys())[attribute]): # Iterate over all techniques used to find matches
                        if technique in techniques_used:
                            filtered_db.append(project)
                            break # If this project has any filtered techniques then add it to filtered db and break
        db = filtered_db # Update the working database to only contain the filtered db

    
    # Only search the free text if there is anything to search for
    if search != "":
        filtered_db = [] # A new list of projects with qualified search results
        for project in db:
            for attribute in range(len(project)): # Iterate over attributes to find the course name
                if list(project.keys())[attribute] == sort_by:
                    if len(re.findall(search.lower(), project.get(list(project.keys())[attribute]).lower())) > 0: # Parse the course name with RegEx
                        filtered_db.append(project)
                        break
        db = filtered_db # Update db with filtered db

    # Sort the list in ascending or descending order
    # First create a new dictionary with course ID as key and sort attribute as value
    db_unsorted_metadata = {}
    for project in db:
        key = ""
        value = ""
        for attribute_iterator in range(len(project)):
            if list(project.keys())[attribute_iterator] == "project_id":
                key = project.get(list(project.keys())[attribute_iterator])
            elif list(project.keys())[attribute_iterator] == sort_by:
                value = project.get(list(project.keys())[attribute_iterator])
        db_unsorted_metadata[key] = value
    
    # Now sort the meta dictionary
    db_sorted_metadata = dict(sorted(
        db_unsorted_metadata.items(),
        key = lambda input : input[1],
        reverse = False if sort_order == "desc" else True))
    # IMPORTANT: The use of sorted dictionaries requires minimum Python version of 3.7 !

    # Cross-reference the data to the metadata to place the projects correctly
    filtered_db = []
    for meta_project in db_sorted_metadata: # Iterate through all sorted projects
        for project in db: # Iterate through all unsorted projects
            for attribute in range(len(project)):
                if list(project.keys())[attribute] == "project_id":
                    if project.get(list(project.keys())[attribute]) == meta_project:
                        filtered_db.append(project)
                        break

    db = filtered_db # Finally place filtered db back into db
    return db
    

def print_db(db):
    print("Database:")
    for project in db:
        for attribute in project:
            print(attribute, " ", project.get(attribute))
        print("")

# Debug main function
def main():
    db = load("data.json")
    #print_db(db)
    print_db(search(db, "project_name", "desc", [], "e"))
    #print(get_project_count(db))
    #print(get_project(db, 0))
    #print(get_project(db, 1))
    #print(get_project(db, 2))
    #print(get_techniques(db))
    #print(get_technique_stats(db))

if __name__ == "__main__":
    main()

    # Print the type of data variable
    
 
    # Print the data of dictionary
   
