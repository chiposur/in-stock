class Options:
  def __init__(self):
      # Command Line Settings
      self.verbose = False
      self.parseFile = None
      # Settings
      self.url = None
      self.notExistsXPATH = None
      self.cooldownMs = None
      self.notifyEmail = None
      self.smtpServer = None
      self.smtpPort = 587

  def isUrlValid(self):
    return len(str(self.url)) > 0

  def isNotExistsXPATHValid(self):
    return len(str(self.notExistsXPATH)) > 0

  def isCooldownMsValid(self):
    return int(self.cooldownMs) >= 1000

  def isValid(self):
    try:
      return self.isUrlValid() and self.isNotExistsXPATHValid() and self.isCooldownMsValid()
    except:
      return False
