import json
import re
import os
# Opening JSON file
def load(file_to_load):
    if os.path.isfile(file_to_load):
        with open(file_to_load) as json_file:
            data = json.load(json_file)
            return data
    return None
    
def get_project_count(db):
    return len(db)

def get_project(db,project_id):
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

#def search(db, sort_by='start_date', sort_order='desc', techniques_used=None, search=None, search_fields=None):
        
    #pass
def main():
    db = load("data.json")

    print(db)
    print(get_project_count(db))
    print(get_project(db,0))
    print(get_project(db,1))
    print(get_project(db,2))
    print(get_techniques(db))
    print(get_technique_stats(db))
    pass

if __name__ == "__main__":
    main()

    # Print the type of data variable
    
 
    # Print the data of dictionary
   