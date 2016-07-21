
import sys
import runpy
assert(sys.argv[3] == "--")
path = sys.argv[2]
activate_this_file = os.path.join(path, "pypy-env/bin/activate_this.py")
execfile(activate_this_file, dict(__file__=activate_this_file))

sys.argv = sys.argv[4:]
runpy.run_path('.', run_name='__main__')
