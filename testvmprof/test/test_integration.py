from testvmprof.ui import (drivers, query1, query,
        reset_search_criteria, select_trace_entry,
        wait_until_loading_complete, local_url)
from testvmprof.support import (VMProfCPythonTest, VMProfPyPyTest,
        output_extract_urls)

def examine_simple_loop(drivers, url):
    for dri in drivers:
        dri.get(url)
        wait_until_loading_complete(dri)
        elems = [elem.text for elem in \
            dri.find_elements_by_css_selector( \
                      'li.trace-entry span.trace-name')]
        assert elems == ['simple_loop']
        select_trace_entry(dri, dri.wait, 'simple_loop')

        link_count = 0
        for link in \
            dri.find_elements_by_css_selector('.trace-type-switch li a'):
            link.click()
            wait_until_loading_complete(dri)
            lines = [line for line in dri.find_elements_by_css_selector(\
                        '.resops .trace-line')]
            assert len(lines) > 0
            link_count += 1
        assert link_count == 4

class BaseVMProfPyPyTest(VMProfPyPyTest):
    vmprof_url = None
    def test_run_vm_and_upload(self, drivers):
        out, err, retcode = self.vmprof_exec("testvmprof/test/examples/simple_loop.py",
                                jitlog=True, web=True)
        print(out,"\n",err)
        url = output_extract_urls(err.decode())['jitlog']
        examine_simple_loop(drivers, url)


    def test_run_vm_and_upload_separate_step(self, drivers, tmpdir):
        file = tmpdir.join('test.jlog')
        out, err, retcode = self.jitlog_exec("testvmprof/test/examples/simple_loop.py",
                                             output=str(file))
        out, err, retcode = self.jitlog_exec(str(file), upload=True)
        url = output_extract_urls(err.decode())['jitlog']
        examine_simple_loop(drivers, url)

    def test_display_interp_pypy(self, drivers):
        self.vmprof_exec("testvmprof/test/examples/simple_loop.py", web=True)
        for dri in drivers:
            dri.get(local_url("#"))
            dri.wait.until(lambda d: not query1(d, '#loading_img').is_displayed())

            names = [elem.text for elem in query(dri, '.media .vm-name')]
            assert names[0] == 'pypy'

class BaseVMProfCPythonTest(VMProfCPythonTest):
    def test_display_interp_cpython(self, drivers):
        self.vmprof_exec("testvmprof/test/examples/simple_loop.py", web=True)
        for dri in drivers:
            dri.get(local_url("#"))
            dri.wait.until(lambda d: not query1(d, '#loading_img').is_displayed())

            names = [elem.text for elem in query(dri, '.media .vm-name')]
            assert names[0] == 'cpython'

#class TestProduction(VMProfTest):
#    vmprof_url = "http://vmprof.com"

class TestLocalPyPy(BaseVMProfPyPyTest):
    vmprof_url = "http://localhost:8000"

class TestLocalCPython(BaseVMProfCPythonTest):
    vmprof_url = "http://localhost:8000"

