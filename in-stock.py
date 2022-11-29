class InStock:
  def __init__(self):
    self.setup()
    self.run()

  def setup(self):
    try:
      print("Enter URL:")
      self.url = str(input())
      print("Enter duration in ms:")
      self.durationMs = int(input())
      print("Enter email to notify:")
      self.email = str(input())
    except Exception as e:
      print(f'Error parsing args: {e}')
      exit(1)

  def run(self):
    print("Starting check...")

if __name__ == "__main__":
    inStock = InStock()