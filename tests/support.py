import requests
import shutil
import tempfile
from subprocess import run
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
        return self.shell_exec(self.pypy, *params, *args)

    def shell_exec(self, *args):
        ro = run(args, cwd=self.tmp)
        assert(ro.returncode == 0, "command: %s. returned %d" % \
                                         (' '.join(args), ro.returncode))
        return ro

def setup_local_pypy(version='latest', dist='linux64'):
    # uff, hardcoded paths & only for linux
    filename = "pypy.tar.bz2"
    tmp = tempfile.mkdtemp()
    download_pypy(os.path.join(tmp, filename), version, dist)
    run(["tar", "xf", os.path.join(tmp, filename)], cwd=tmp)
    for root, dirs, files in os.walk(tmp):
        for dir in dirs:
            if dir.startswith("pypy-c"):
                return tmp, os.path.join(dir, "bin", "pypy")
    assert(False, "could not setup local pypy")
    return None

def download_pypy(path, version='latest', dist='linux64'):
    link = "http://buildbot.pypy.org/nightly/default/pypy-c-jit-{}-{}.tar.bz2".format(version, dist)
    r = requests.get(link, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
            return

    raise Exception("cannot download pypy!")
