import requests
import shutil
import tempfile
import subprocess
import os

class VMProfTest(object):
    def vmprof_exec(self, *args, cwd=None, jitlog=False, web=False, output=None):
        script = args[0] 
        params = []
        if web:
            params += ['--web', '--web-url', self.vmprof_url]
        if jitlog:
            params += ['--jitlog']
        if output:
            params += ['-o', output]
        return self.shell_exec(self.interp, "testvmprof/test/examples/boot_env.py" ,
                               self.tmp + "/" + self.interpname + "-env/bin/activate_this.py",
                               "vmprof", "--", *params, *args, cwd=cwd)

    def shell_exec(self, *args, cwd=None, env={}):
        if cwd == None:
            cwd = os.getcwd()
        print("shexe> %s (pwd: %s)" % (' '.join(args), os.getcwd()))
        proc = subprocess.Popen(args, cwd=cwd,
                                stderr=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                env=env)
        try:
            outs, err = proc.communicate(timeout=60)
        except subprocess.TimeoutExpired:
            proc.kill()
            raise AssertionError("command: %s. failed %d" % \
                    (' '.join(args), ro.returncode))
        assert proc.returncode == 0, \
            "err\n%s\n\nout\n%s\n" % (err.decode(), outs.decode())
        return outs, err, proc.returncode


class VMProfCPythonTest(VMProfTest):
    def setup_class(self):
        tmp, cpython = setup_local_cpython()
        self.tmp = tmp
        self.interp = os.path.join(tmp, cpython)
        self.interpname = 'cpython'
        self.vmprofargs = "--web --web-url %s" % self.vmprof_url

class VMProfPyPyTest(VMProfTest):
    def setup_class(self):
        tmp, pypy = setup_local_pypy()
        self.tmp = tmp
        self.interp = os.path.join(tmp, pypy)
        self.interpname = 'pypy'
        self.vmprofargs = "--web --web-url %s" % self.vmprof_url

    def jitlog_exec(self, *args, cwd=None, web=False, upload=None, output=None, env={}):
        script = args[0] 
        params = []
        if web:
            params += ['--web', '--web-url', self.vmprof_url]
        if output:
            params += ['-o', output]
        if upload:
            params += ['--upload', '--web-url', self.vmprof_url]
        return self.shell_exec(self.interp, "testvmprof/test/examples/boot_env.py" ,
                               self.tmp + "/" + self.interpname + "-env/bin/activate_this.py",
                               "jitlog", "--", *params, *args, cwd=cwd, env=env)

def setup_local_cpython():
    tmp = tempfile.mkdtemp()
    absexe = "/usr/bin/python"
    subprocess.run(["virtualenv", "-p", absexe, "cpython-env"], cwd=tmp)
    subprocess.run(["cpython-env/bin/pip", "install", "--no-cache-dir", "--pre", "vmprof"], cwd=tmp)
    return tmp, os.path.join("cpython-env","bin","python")


def setup_local_pypy(branch='trunk', version='latest', dist='linux64'):
    # uff, hardcoded paths & only for linux
    filename = "pypy.tar.bz2"
    tmp = tempfile.mkdtemp()
    if "TEST_PYPY_EXEC" not in os.environ:
        download_pypy(os.path.join(tmp, filename), branch, version, dist)
        subprocess.run(["tar", "xf", os.path.join(tmp, filename)], cwd=tmp)
        executable = None
        found = False
        for root, dirs, files in os.walk(tmp):
            for dir in dirs:
                if dir.startswith("pypy-c"):
                    executable = os.path.join(dir, "bin", "pypy")
                    found = True
                    break
        if not found:
            raise AssertionError("could not setup local pypy")
        absexe = os.path.join(tmp, executable)
    else:
        absexe = executable = os.environ["TEST_PYPY_EXEC"]
    # poor man's dependency resolution
    subprocess.run(["virtualenv", "-p", absexe, "pypy-env"], cwd=tmp)
    subprocess.run(["pypy-env/bin/pip", "install", "--no-cache-dir", "--pre", "vmprof"], cwd=tmp)
    return tmp, os.path.join("pypy-env","bin","python")

def download_pypy(path, branch, version, dist):
    link = "http://buildbot.pypy.org/nightly/{}/pypy-c-jit-{}-{}.tar.bz2".format(branch, version, dist)
    print("downloading", link)
    r = requests.get(link, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
            return

    raise Exception("cannot download pypy!")

def output_extract_urls(output):
    found = {}
    for line in output.splitlines():
        if line.startswith("VMProf log: "):
            found['profile'] = line[12:]
        if line.startswith("PyPy JIT log: "):
            found['jitlog'] = line[14:]
    return found

