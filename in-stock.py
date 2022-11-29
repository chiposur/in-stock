import requests
from time import sleep

class InStock:
  MIN_COOLDOWN_MS = 1000

  def __init__(self):
    self.setup()
    self.start()

  def setup(self):
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
      print(f'Error parsing args: {e}')
      exit(1)

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
    except requests.exceptions.ReadTimeout as e:
      print(f'Timeout reading request...')
      return
    if req.status_code == 200:
      print("Request successful, parsing...")
    else:
      print(f'Request failed with error code {req.status_code}')

  def notify(self):
    pass

if __name__ == "__main__":
    inStock = InStock()