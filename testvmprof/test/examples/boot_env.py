import sys
import runpy
import os

path = sys.argv[1]
assert(sys.argv[3] == "--")

activate_this_file = path
execfile(activate_this_file, dict(__file__=activate_this_file))

mod = sys.argv[2]
sys.argv = sys.argv[3:] # -- will be stripped off by vmprof
runpy.run_module(mod, run_name='__main__')
