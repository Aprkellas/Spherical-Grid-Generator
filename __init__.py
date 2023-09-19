from vcApplication import *

def OnStart():
  cmduri = getApplicationPath() + 'Sphere.py'
  cmd = loadCommand('Sphere',cmduri)
  addMenuItem('VcTabTeach/Generate', "Sphere", -1, "Sphere")
