from pwn import *
from collections import defaultdict
import md5
import numpy as np

target_program = "bash"


file_path = "/home/seralee/Desktop/Research/KPM/downloads/bash/Bionic/4.4-5ubuntu1/bash-4.4/bash"

def do_compile(target_program):
  download_path = "downloads/%s" % target_program 
  for root, dirs, files in os.walk(download_path):
    for file in files:
        if ".tar" in file:
          cmd = "cd %s; tar -xvf *.tar*;cd bash*;./configure;make" % (root)
          print(cmd)
          print(os.path.join(root, file))
          os.system(cmd)

def find_fingerprints(target_program):
  download_path = "downloads/%s" % target_program 
  all_hashs = defaultdict(int)
  info = []
  unique_hash_result = {}
  for root, dirs, files in os.walk(download_path):
    for file in files:
      if file == target_program:
        full_path = os.path.join(root,file)
        hashs = get_hash_values(full_path)
        info.append([full_path,hashs])
        for h in hashs:
          all_hashs[h] += 1
  multi_key = [key for key, value in all_hashs.items() 
                   if value != 1]
  for i in info:
    bash, hashs = i
    unique = None
    for hash_ in hashs:
      if(hash_ in multi_key):
        unique = hash_
        break
    if(unique != None):
      uniq_h = unique
      unique_hash_result[bash] = [hashs.index(uniq_h),uniq_h]
  print(unique_hash_result)



  

def split_by_len(string,n):
  return [string[i:i+n] for i in range(0, len(string), n)]

def get_hash_values(binary):
  bash = ELF(binary)

  s = bash.get_section_by_name(".text").data()
  lists = split_by_len(s,4096)
  md5_results=[]
  for l in lists:
    m = md5.new()
    m.update(l)
    md5_results.append(m.digest())
  return md5_results


#do_compile("bash")
find_fingerprints("bash")
