from tests.support import BaseVMProfTest
from testvmprof.support import (drivers, query1, query,
        reset_search_criteria, select_trace_entry)

class VMProfTest(BaseVMProfTest):
    vmprof_url = None
    def test_run_vm(self, drivers):
        out, err = self.pypy_exec("code/loop.py", jitlog=True, upload=True)
        assert(not err)
        url = extract_traces_url(out)

        for driver in drivers:
            pass

class TestProduction(VMProfTest):
    vmprof_url = "https://www.vmprof.com"

#class TestLocal(VMProfTest):
#    vmprof_url = "http://localhost:8000"

