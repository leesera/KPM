import json
from pprint import pprint
import os

target_program = "bash"

download_path = "downloads/%s" % target_program 

json_data=open("output.json").read()

datas = json.loads(json_data)

for data in datas:
  print data["version"]
  path = os.path.join(download_path,data["target"])
  path = os.path.join(path,data["version"])
  cmd = "mkdir -p %s" % path
  print(cmd)
  os.system(cmd)
  for filename in data["links"].keys():
    link = data["links"][filename]
    cmd = "wget %s -O %s" % (link, os.path.join(path,filename))
    print(cmd)
    os.system(cmd)
