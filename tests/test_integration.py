from tests.support import BaseVMProfTest, setup_local_pypy

class VMProfTest(BaseVMProfTest):
    vmprof_url = None
    def test_run_vm(self):
        self.pypy_exec("code/loop.py", jitlog=True, upload=True)

class TestLocal(VMProfTest):
    vmprof_url = "http://localhost:8000"




