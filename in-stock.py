import getopt
import requests
import sys
from time import sleep

from options import Options

class InStock:
  MIN_COOLDOWN_MS = 1000

  def __init__(self):
    self.options = Options()
    self.setup()
    self.start()

  def setup(self):
    self.parseCmdLineOptions()
    if self.options.parseFile:
      self.parseSettingsFromFile()
    else:
      self.parseSettingsFromUserInput()

  def parseCmdLineOptions(self):
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "hf:v", ["help", "file="])
    except getopt.GetoptError as err:
        print(f'{err}\n')
        self.printHelp()
        exit(2)
    for o, a in opts:
        if o == "-v":
            self.options.verbose = True
        elif o in ("-h", "--help"):
            self.printHelp()
            sys.exit()
        elif o in ("-f", "--file"):
            if len(a) > 0:
              self.options.parseFile = a
        else:
            assert False, "unhandled option"

  def parseSettingsFromFile(self):
    print(f"Parsing '{self.options.parseFile}'...")

  def parseSettingsFromUserInput(self):
    try:
      print("Enter URL:")
      self.url = str(input())
      if not self.url:
        raise Exception("URL is required")
      print("Enter selector:")
      self.selector = str(input())
      print("Enter cooldown time in ms:")
      self.cooldownMs = max(int(input()), self.MIN_COOLDOWN_MS)
      print("Enter email to notify:")
      self.email = str(input())
    except Exception as e:
      print(f'Error parsing user input: {e}')
      exit(1)

  def printHelp(self):
    print("#########")
    print("#InStock#")
    print("#########")
    print("© Chip Osur 2022\n")
    print("A utility for retrieving web docs and checking if an item is in stock.\n")
    print("-h, -help: Show utility help")
    print("-f, -file: Parse required and optional settings from file")

  def start(self):
    print("Starting check...")
    self.running = True
    while self.running:
      self.checkAvailability()
      sleep(self.cooldownMs / 1000)
    self.notify()

  def checkAvailability(self):
    print("Checking availability...")
    print(f"Retrieving '{self.url}'...")
    try:
      req = requests.get(self.url, timeout=(8, 30))
    except requests.exceptions.ReadTimeout:
      print("Timeout reading request...")
      return
    except requests.exceptions.MissingSchema:
      print("Missing schema. Did you forget to specify http/s?")
      exit(1)
    if req.status_code == 200:
      print("Request successful, parsing...")
    else:
      print(f'Request failed with error code {req.status_code}')

  def notify(self):
    pass

if __name__ == "__main__":
    inStock = InStock()