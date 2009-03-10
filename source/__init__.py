def name():
  return "Anuga Interface"
def description():
  return "A collection of tools for Anuga pre and post processing"
def version():
  return "Version 0.0"
def qgisMinimumVersion():
  return "1.0"
def authorName():
  return "Vincent Edgewater"
def classFactory(iface):
  from anugaInterface import AnugaInterface
  return AnugaInterface(iface)
