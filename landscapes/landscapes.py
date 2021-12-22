import os
import sys
import json
import bundle

#
# The name of the pipe to connect to.
#

PIPE_NAME = "project_pipe_name"

#
# The format to output board data with the get request. Can be
# 'data', 'dial' or 'dump'
#

OUTPUT_FORMAT = "data"

def main(appname, argv):

  # Help information
  
  if len(argv) == 0:
    
    print("usage  : %s <mode> [options]" % appname)
    print("example: %s get p742176c va6ca839 g809dbc0" % appname)
    print()
    print(" build   Execute the create-units request. No other options must be given.")
    print(" get     Execute a get-units request. The mode must be followed by 0 or more")
    print("         options. If none are given, all units are selected. If 1 is given, it")
    print("         is used as a filter to select units. If 2 or more are given, they are")
    print("         used as uids to select specific units.")    
    exit()
  
  # Read arguments
  
  mode = argv[0]
  
  if not mode in ['build', 'get']:
    print("'%s' is not a valid mode. Use 'build' or 'get'." % mode)
    exit(1)
  
  # Connect to the pipe.
  
  client = bundle.Client(PIPE_NAME)
  
  # Perform handshake
  
  pid = client.send({"status":"OK", "name":"Landscapes Script"})
  print("Application pid: %s" % pid)

  # Check for AutoAPI launch success
  
  response = client.read()
  if response['status'] == "ERROR":
    print(response['message'])
    exit(1)

  # Execute request
  
  if mode == "build":
  
     load_lists(client)
     load_tags(client)
     load_data(client)
   
  else:
     
     get_units(client, argv[1:])

#
# Execute the get request.
#

def get_units(client, argv):
  
  command = None
  
  if len(argv) == 0:
    command = ""
  elif len(argv) == 1:
    command = argv[0]
  else: 
    command = argv
   
  output = client.send({"command" : "get-units", "data" : {"filter" : command, "mode" : OUTPUT_FORMAT}})
  
  with open("output.json", "w") as f:
    f.write(json.dumps(output["units"], indent=2)) 
    
  if len(output["log"]):
    print("Log Messages:\n")
    for line in output["log"]:
      print("  " + line)
  
#
# Load the lists of the project.
#

def load_lists(client):
  
  lists = [{'key': 'climate', 'name': 'Climate', 'items': [{'key': 'desert', 'name': 'Desert'}
                                                         , {'key': 'forest', 'name': 'Forest'}
                                                         , {'key': 'coastal', 'name': 'Coastal'}
                                                         , {'key': 'plains', 'name': 'Plains'}
                                                         , {'key': 'mountains', 'name': 'Mountains'}
                                                         , {'key': 'cave', 'name': 'Cave'}
                                                         , {'key': 'sky', 'name': 'Sky'}]
           }
                                                         
          ,{'key': 'beauty', 'name': 'Beauty', 'items': [{'key': 'water', 'name': 'Water'}
                                                       , {'key': 'color', 'name': 'Colorful'}
                                                       , {'key': 'plants', 'name': 'Plants'}
                                                       , {'key': 'animals', 'name': 'Animals'}
                                                       , {'key': 'pristine', 'name': 'Pristine'}]
           }
          ]

  client.send({"command":"create-lists", "data":lists})

#
# Load the tags of the project.
#

def load_tags(client):
  
  tags = [{'key': 'night', 'name': 'Night Time', 'usage': 'The scene is captured at night.'}
        , {'key': 'invalid', 'name': 'Invalid', 'usage': 'The scene is not actually a landscape.'}]
        
  client.send({"command":"create-tags", "data":tags})

#
# Load the data of the project
#

def load_data(client):

  with open("data.json") as file:
    data = json.load(file)
  
  for item in data:
    for field in item["fields"]:
      if field["type"] == "image":
        field["path"] = os.path.realpath(field["path"]);

  command  = {"command":"create-units", "data": data}
  response = client.send(command)


def load_folder(client, dirpath):

  files   = os.dirpath()
  units   = []
  command = {"command":"create-units", "data":units}

  for path in files:
  
    fields = []
    tags   = []
    unit   = {"fields":fields, "tags":tags}
    
    units.append(unit)
    
    fields.append({"type":"image", "key":"sample", "name":"Sample", "path":path})

  response = client.send(command)

#
# The application entry-point.
#

if __name__ == "__main__":
  main(sys.argv[0], sys.argv[1:]);
