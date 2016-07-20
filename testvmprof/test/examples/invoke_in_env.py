path = "pypy-env/bin/activate_this.py"
execfile(activate_this_file, dict(__file__=activate_this_file))

import sys
import runpy
assert(sys.argv[2] == "--")
sys.argv = sys.argv[3:]
runpy.run_path('.', run_name='__main__')
