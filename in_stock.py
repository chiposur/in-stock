from datetime import datetime
from email.mime.text import MIMEText
import getopt
from io import StringIO
from lxml import etree
import os
import requests
from smtplib import SMTP
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
        opts, _ = getopt.getopt(sys.argv[1:], "hf:v", ["help", "verbose", "file="])
    except getopt.GetoptError as err:
        print(f'{err}\n')
        self.printHelp()
        sys.exit(1)
    for o, a in opts:
        if o in ("-v", "--verbose"):
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
    try:
      with open(self.options.parseFile, 'r') as file:
        try:
          line = file.readline()
          while line:
            parsedLine = line.split(':', 1)
            if len(parsedLine) < 2:
              continue
            field = parsedLine[0]
            value = parsedLine[1].strip()
            if field == 'url':
              self.options.url = value
            elif field == 'notExistsXPATH':
              self.options.notExistsXPATH = value
            elif field == 'cooldownMs':
              self.options.cooldownMs = max(int(value), self.MIN_COOLDOWN_MS)
            elif field == 'email':
              self.options.email = value
            elif field == 'smtpServer':
              self.options.smtpServer = value
            elif field == 'smtpPort':
              self.options.smtpPort = int(value)
            line = file.readline()
        finally:
          file.close()
    except IOError as e:
      print(f'Could not open file for reading: {e}')
    except Exception as e:
      print(f'Error parsing file: {e}')
      sys.exit(1)
    if not self.options.isValid():
      print("Parsed file is not valid. Check that url, notExistsXPATH, and cooldownMs are set correctly.")
      sys.exit(1)

  def parseSettingsFromUserInput(self):
    try:
      print("Enter URL:")
      self.options.url = str(input())
      if not self.options.url:
        raise Exception("URL is required")
      print("Enter XPATH that indicates item is unavailable. For more info see --help:")
      self.options.notExistsXPATH = str(input())
      if not self.options.notExistsXPATH:
        raise Exception("Item unavailable XPATH is required")
      print("Enter cooldown time in ms:")
      self.options.cooldownMs = max(int(input()), self.MIN_COOLDOWN_MS)
      print("Enter email to notify:")
      self.options.email = str(input())
      print("Enter SMTP server:")
      self.options.smtpServer = str(input())
      print("Enter SMTP server port (default :587):")
      port = input()
      if port:
        self.options.smtpPort = int(input())
    except Exception as e:
      print(f'Error parsing user input: {e}')
      sys.exit(1)

  def printHelp(self):
    print("#########")
    print("#InStock#")
    print("#########")
    print("© Chip Osur 2022\n")
    print("A utility for retrieving web docs and checking if an item is in stock.\n")
    print("-f, -file: Parse required and optional settings from file")
    print("-h, -help: Show utility help")
    print("       -v: Verbose output when running\n")
    print("Environment Variables")
    print("---------------------")
    print("SMTP_SERVER_USERNAME")
    print("SMTP_SERVER_PASSWORD\n")
    print("Sample Settings File")
    print("--------------------")
    print("url: https://www.example.com/store/products/popular-product/")
    print("notExistsXPATH: //span[text()=\"Sold out\"]")
    print("cooldownMs: 3000")
    print("email: chip@example.com")
    print("smtpServer: smtp.example.com")
    print("smtpPort: 587")

  def start(self):
    print("Running...")
    self.running = True
    while self.running:
      self.checkAvailability()
      sleep(self.options.cooldownMs / 1000)
    self.notify()

  def checkAvailability(self):
    self.vPrint("Checking availability...")
    self.vPrint(f"Retrieving '{self.options.url}'...")
    try:
      req = requests.get(self.options.url, timeout=(8, 30))
      if req.status_code == 200:
        self.vPrint("Request successful, parsing...")
      else:
        self.vPrint(f'Request failed with error code {req.status_code}')
        return
      parser = etree.HTMLParser()
      root = etree.parse(StringIO(req.text), parser).getroot()
      self.inStock = len(root.xpath(self.options.notExistsXPATH)) == 0
      if self.inStock:
        self.running = False
        self.finishedAt = datetime.now()
        print(f'{self.finishedAt}: XPATH does not exist. Item may be in stock, stopping.')
    except requests.exceptions.ReadTimeout:
      self.vPrint("Timeout reading request...")
      return
    except requests.exceptions.MissingSchema:
      print("Missing schema. Did you forget to specify http/s?")
      sys.exit(1)
    except etree.XPathEvalError as e:
      print(f'Error evaluating XPATH: {e}')

  def notify(self):
    try:
      body = f'InStock finished running and item may be in stock. Check the URL for confirmation: {self.options.url}' \
        f'Time: {self.finishedAt}' \
        f'XPATH: {self.options.notExistsXPATH}'
      msg = MIMEText(body)
      fromAddr = "noreply@InStock.com"
      msg['Subject'] = "InStock Alert"
      msg['From'] = fromAddr
      msg['To'] = self.options.email
      with SMTP(self.options.smtpServer, self.options.smtpPort) as smtpServer:
        username = os.environ['SMTP_SERVER_USERNAME']
        password = os.environ['SMTP_SERVER_PASSWORD']
        smtpServer.starttls()
        smtpServer.login(username, password)
        smtpServer.sendmail(self.options.email, self.options.email, msg.as_string())
    except Exception as e:
      print(
        f'Sending email to {self.options.email} failed: {e}\n' \
        f'SMTP Server: {self.options.smtpServer}\n' \
        f'SMTP Port: {self.options.smtpPort}')

  def vPrint(self, s):
    if self.options.verbose:
      print(s)

if __name__ == "__main__":
    inStock = InStock()
