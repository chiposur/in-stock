class Options:
  def __init__(self):
      # Command Line Settings
      self.verbose = False
      self.parseFile = None
      # Settings
      self.url = None
      self.notExistsXPATH = None
      self.cooldownMs = None
      self.email = None

  def isValid(self):
    try:
      return len(str(self.url)) > 0 and len(str(self.notExistsXPATH)) > 0 and int(self.cooldownMs) > 1000
    except:
      return False
