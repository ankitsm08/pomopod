from pomopod.cli import app
from pomopod.startup import startup_check

if __name__ == "__main__":
  startup_check()
  print()
  app()
