###################
#                 #
#   JSON Parser   #
#The API uses JSON#
###################
def jparse(json):
  j = str(json) # basically replacing JavaScript types with the Python equivalents
  j = j.replace("null", "None")
  j = j.replace("false", "False")
  j = j.replace("true", "True")
  j = j.replace("\n", "")
  # now, j is basically a dict that is in quotes (a string)
  return eval(j) # eval turns the string into a legal py datatype
