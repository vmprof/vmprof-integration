import requests
import shutil
from subprocess import run

class BaseVMProfTest(object):
    def setup_class(self):
        self.pypy = setup_local_pypy(version='latest')
        self.vmprofargs = "--web --web-url %s" % self.vmprof_url

    def pypy_exec(self, *args, jitlog=False, upload=True):
        params = ['-m', 'vmprof']
        if upload:
            params += ['--web', '--web-url', self.vmprof_url]
        if jitlog:
            params += ['--jitlog']
        return self.shell_exec(self.pypy, *params, *args)

    def shell_exec(self, *args):
        return run(*args)

def setup_local_pypy(version='latest', dist='linux64'):
    # uff, hardcoded paths & only for linux
    filename = "/tmp/pypy.tar.bz2"
    pypypath = "/tmp/pypy"
    download_pypy(filename, version, dist)
    run(["mkdir", "-xf", pypypath])
    run(["cd", pypypath, ";", "tar", "-xf", filename])
    return pypypath + "/pypy-nightly/bin/pypy"

def download_pypy(path, version='latest', dist='linux64'):
    link = "http://buildbot.pypy.org/nightly/default/pypy-c-jit-{}-{}.tar.bz2".format(version, dist)
    r = requests.get(link, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
            return

    raise Exception("cannot download pypy!")
