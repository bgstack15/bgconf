# File: /usr/share/bgconf/localapp.py

# DEFINE CLASSES
class bgfile:
   def __init__(self,source,dest):
      self.source = source
      self.dest = dest

class bgdirectory:
   def __init__(self,source,dest):
      self.source = source
      self.dest = dest

class bgapp:
   def __init__(self,name):
      self.name = name
      self.force = False
      self.overwrite = False
      self.files = []
      self.directories = []
      self.action = ""
      self.source = ""
      self.overwriteall = ""
      self.forceall = ""
      self.check = ""
