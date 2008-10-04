# load AnugaInterface class from file anugaInterface.py
from anugaInterface import AnugaInterface
def name():
  return "Anuga Interface"
def description():
  return "A collection of tools for Anuga pre and post processing"
def version():
  return "Version 0.0"
def classFactory(iface):
  return AnugaInterface(iface)
