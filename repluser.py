###############
#             #
#   ReplUser  #
#             #
###############
import bs4 # webpage parsing
import requests # used to get webpage source
import jparser # my json parser library
def getLeaderboard(l): # l is the leaderboard, this func just formats the leaderboard
    leaders = l
    formatted = leaders.text.split(')')
    for i in range(len(formatted)):
        formatted[i] = formatted[i].split('(')[0]
    return formatted

class ReplAPI():
    def __init__(self, username): # I am doing all the parsing and stuff here since if I do it below, the code will be slow
      self.user = username.replace("@", '') # removing the @
      amoghthecool = requests.get(f"https://replit.com/data/profiles/{self.user}") # accessing the API
      if amoghthecool.text == '{"message":"user not found","name":"NotFoundError","status":404}': # checking if the account exists
        exit(f'"{self.user}" does not exist!!')
      self.json = jparser.jparse(amoghthecool.text) # the json data
      url = f'https://www.replit.com/@{self.user}' # this is their profile on replit (formatted and everything)
      reqs = requests.get(url) # src
      self.soup = bs4.BeautifulSoup(reqs.text,
      'html.parser',parse_only=bs4.SoupStrainer(['span'])) # strains for all span elements

      url = "https://replit.com/leaders?since=all_time" # leaders
      page = requests.get(url) # scraped html
      soup = bs4.BeautifulSoup(page.text,'html.parser',parse_only=bs4.SoupStrainer(['div'])) # strains for all divs
      leaders = soup.find(class_="jsx-776267233 leaderboard-list-top") # gets the list of leaders (in divs)
      self.l = leaders # this is the input to the getLeaderboard func
    def getBio(self):
        return self.json["bio"]
    def getOrg(self):
        try:
            return self.json["organization"]
        except:
            return "No orginizations found."
    def getCycles(self):
        return int(eval(self.soup.find(title = "cycles").text)) 
    def getIsHacker(self):
        try:
            return self.json["hacker"]
        except:
            return False
    def getPfp(self):
        try:
            return self.json["icon"]["url"]
        except:
            return "nopfp"
    def getTopLangs(self):
      return self.json["topLanguages"]
    def getFirstName(self):
      try:
        if (self.json["firstName"] != None): 
          return self.json["firstName"]
        else:
          raise IndexError("wut")
      except:
        return "null"
    def getLastName(self):
      try:
        if (self.json["lastName"] != None):
          return self.json["lastName"]
        else:
          raise IndexError("wut")
      except:
        return "null"
    def getName(self):
        return self.getFirstName() + ' ' + self.getLastName()
    def mergeListsIntoDict(self, l1, l2): # a helper func that I made that merges two lists into one dict
        dictionary = {}
        for i in range(len(l1)):
            dictionary[l1[i]] = l2[i]
        return dictionary
    def getRepls(self): # gets their repls
      repls2 = self.json["repls"]
      for i in range(len(repls2)):
        val = repls2[i]["title"]
        repls2[i] = {val: f"https://replit.com/@{self.user}/{val.replace(' ', '')}"}
      return repls2
    def isInLeaderboard(self):
        for i in getLeaderboard(self.l): # passing in the raw HTNK
            if i.upper() == self.user.upper(): # making case irrelavent
                return True
        return False
    def getNotifs(self): # broken... needs user login JinJaJAJA
      amoghthecool = requests.get(f"https://replit.com/notifications")
      soup = bs4.BeautifulSoup(amoghthecool.text,'html.parser', parse_only=bs4.SoupStrainer(['div']))
      n = soup.find_all(class_ = "jsx-806891921 item-container has-link")
      p = []
      for i in n:
        p.append(i.text)
      return n
