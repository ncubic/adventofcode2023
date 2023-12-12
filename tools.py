import os

def getLines(fileName):
  script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
  abs_file_path = os.path.join(script_dir, fileName)

  puzzle = open(abs_file_path, 'r')
  return puzzle.readlines()
