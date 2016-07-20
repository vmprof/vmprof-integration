import requests
import shutil
import tempfile
import subprocess
import os

class BaseVMProfTest(object):
    def setup_class(self):
        tmp, pypy = setup_local_pypy(version='latest')
        self.tmp = tmp
        self.pypy = os.path.join(tmp, pypy)
        self.vmprofargs = "--web --web-url %s" % self.vmprof_url

    def pypy_exec(self, *args, jitlog=False, upload=False):
        params = ['-m', 'vmprof']
        if upload:
            params += ['--web', '--web-url', self.vmprof_url]
        if jitlog:
            params += ['--jitlog']
        return self.shell_exec(self.pypy, "testvmprof/test/examples/invoke_in_env.py" ,
                               "--", *params, *args)

    def shell_exec(self, *args):
        proc = subprocess.Popen(args, cwd=self.tmp,
                                stderr=subprocess.STDOUT)
        try:
            outs, err = proc.communicate(timeout=15)
        except TimeoutExpired:
            proc.kill()
            raise AssertionError("command: %s. failed %d" % \
                    (' '.join(args), ro.returncode))
        return outs, err, proc.returncode

def setup_local_pypy(version='latest', dist='linux64'):
    # uff, hardcoded paths & only for linux
    filename = "pypy.tar.bz2"
    tmp = tempfile.mkdtemp()
    download_pypy(os.path.join(tmp, filename), version, dist)
    subprocess.run(["tar", "xf", os.path.join(tmp, filename)], cwd=tmp)
    executable = None
    for root, dirs, files in os.walk(tmp):
        for dir in dirs:
            if dir.startswith("pypy-c"):
                executable = os.path.join(dir, "bin", "pypy")
                break
    else:
        assert(False, "could not setup local pypy")
    absexe = os.path.join(tmp, executable)
    # poor man's dependency resolution
    subprocess.run(["virtualenv", "-p", absexe, "pypy-env"], cwd=tmp)
    subprocess.run(["pypy-env/bin/pip", "install", "--pre", "vmprof"], cwd=tmp)
    return tmp, os.path.join("pypy-env","bin","python")

def download_pypy(path, version='latest', dist='linux64'):
    link = "http://buildbot.pypy.org/nightly/default/pypy-c-jit-{}-{}.tar.bz2".format(version, dist)
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

