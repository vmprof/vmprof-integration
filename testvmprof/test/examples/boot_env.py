import sys
import runpy
import os

path = sys.argv[1]
assert(sys.argv[2] == "--")

activate_this_file = os.path.join(path, "pypy-env/bin/activate_this.py")
execfile(activate_this_file, dict(__file__=activate_this_file))

sys.argv = sys.argv[2:] # -- will be stripped off by vmprof
print(sys.argv)
runpy.run_module('vmprof', run_name='__main__')
