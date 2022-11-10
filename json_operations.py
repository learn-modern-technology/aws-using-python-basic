import os
import json

def loadjsondata(file_path):
    blank_json = {}
    if os.path.exists(file_path):
        try:
            f = open(file_path,"r")
            json_data = json.load(f)
            f.close()
            return json_data
        except ValueError:
            print("Some error in json load data")
            return blank_json
    else:
        return blank_json
    
def savejsondata(file_path, data_to_save):
    blank_json ={}
    current_json_data = json.dumps(data_to_save)
    f = open(file_path, "w")
    f.write(current_json_data)
    f.close()
    return True

    