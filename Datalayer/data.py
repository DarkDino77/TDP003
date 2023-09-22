import json
import re
import os

# Loads a json file of a given path  
# return None if path is invalid 
def load(file):
    # Check if path is valid 
    if os.path.isfile(file):

        # Load database in from file and return in a numerical order
        with open(file) as json_file:
            data = json.load(json_file)
            return search(data)
        
    # If path is invalid return none     
    return None

# returns the number of dictonarys in a given database
def get_project_count(db):
    return len(db)

# Searches the database for the asked for project based on its project id
# returns a dict containg the given project id 
# returns none if the id is invalid 
def get_project(db, project_id):
    return next((element for element in db if element['project_id'] == project_id), None)   

# Searches the datbase for all uniqe techniques that exists in a databes 
# returns A list of techniques sorted in alphabetically order
def get_techniques(db):
    # Creates a empty list 
    uniqe_techniques = []
    # searches the list techniques that do not exist in the new list uniqe_techniques
    for dictonary in db:
        for techniques_used in dictonary["techniques_used"]:
            if techniques_used not in uniqe_techniques:

                # Adds technique to the new list 
                uniqe_techniques.append(techniques_used)

    # sorts the list in alphabetically order
    return sorted(uniqe_techniques)

# Searches the datbase for all occurrences of all techniques 
# Makes them into a dict where the key are the techniques
# The value is a list containing the project id and project name where the key technique is used 

# returns a dict where the key are the techniques and the value is a list containing the project id and project name where the key technique is used
def get_technique_stats(db):
    # Makes a empty dictonary
    technique_stats = {}
    
    # Searches for the mention of a technique
    for dictonary in db:
        for technique in dictonary["techniques_used"]:

            # Adds a item into the dict where key the key is the technique and the value is a list containing the project id and project name where the key technique is used
            if technique not in technique_stats:
                technique_stats[technique] = [{"id": dictonary["project_id"], "name": dictonary["project_name"]}]

            # Adds the appropriet value to the appropriet key  
            else:
                technique_stats[technique].append({"id": dictonary["project_id"], "name": dictonary["project_name"]})

    # returns a dict where the key are the techniques and the value is a list containing the project id and project name where the key technique is used
    return technique_stats

def search(db, sort_by = 'start_date', sort_order = 'desc', techniques = None, search = None, search_fields = None):

    # Cheap workaround for empty search fields
    if search_fields == []:
        return []

    # Only parse techniques if asked to
    if techniques != None and techniques != []:
        filtered_db = [] # A new list of projects with qualified search results
        for project in db:
            for attribute in range(len(project)): # Iterate over all attributes
                if list(project.keys())[attribute] == "techniques_used": # Find the techniques_used attribute
                    for technique in project.get(list(project.keys())[attribute]): # Iterate over all techniques used to find matches
                        if technique in techniques:
                            filtered_db.append(project)
                            break # If this project has any filtered techniques then add it to filtered db and break
        db = filtered_db # Update the working database to only contain the filtered db

    # Only search the free text if there is anything to search for
    if search != None:
        filtered_db = [] # A new list of projects with qualified search results
        for project in db:
            for attribute in range(len(project)): # Iterate over attributes to find any qualified attribute
                if search_fields == None or list(project.keys())[attribute] in search_fields: # Utilizing lazy evaluation to not search through 'None'
                    if len(re.findall(search.lower(), str(project.get(list(project.keys())[attribute])).lower())) > 0: # Parse the attribute with RegEx
                        filtered_db.append(project)
                        break
        db = filtered_db # Update db with filtered db

    # Sort the list in ascending or descending order
    # First create a new dictionary with project ID as key and sort attribute as value
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
    print_db(search(db, techniques=[], search="okänt", search_fields=["project_id","project_name","course_name"]))
    #print_db(search(db, "start_date", "desc", None, "e", ["lulz_had"]))
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
   
