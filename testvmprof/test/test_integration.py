import tempfile
from testvmprof.ui import (drivers, query1, query,
        reset_search_criteria, select_trace_entry,
        wait_until_loading_complete, local_url)
from testvmprof.support import (VMProfCPythonTest, VMProfPyPyTest,
        output_extract_urls)
from os.path import join

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

    def setup_class(self):
        tmp = tempfile.mkdtemp()
        self.test_tmp = tmp
        super(BaseVMProfPyPyTest, self).setup_class(self)

    def test_run_vm_and_upload(self, drivers):
        out, err, retcode = self.vmprof_exec("testvmprof/test/examples/simple_loop.py",
                                jitlog=True, web=True)
        print(out,"\n",err)
        url = output_extract_urls(err.decode())['jit']
        examine_simple_loop(drivers, url)


    def test_run_vm_and_upload_separate_step(self, drivers, tmpdir):
        file = tmpdir.join('test.jlog')
        out, err, retcode = self.jitlog_exec("testvmprof/test/examples/simple_loop.py",
                                             output=str(file))
        out, err, retcode = self.jitlog_exec(str(file), upload=True)
        url = output_extract_urls(err.decode())['jit']
        examine_simple_loop(drivers, url)

    def test_display_interp_pypy(self, drivers):
        self.vmprof_exec("testvmprof/test/examples/simple_loop.py", web=True)
        for dri in drivers:
            dri.get(local_url("#"))
            dri.wait.until(lambda d: not query1(d, '#loading_img').is_displayed())

            names = [elem.text for elem in query(dri, '.media .vm-name')]
            assert names[0] == 'pypy'

    #def test_run_moderatly_sized_log(self, drivers):
    #self.shell_exec(None, "wget", "https://bitbucket.org/pypy/pypy/get/default.tar.bz2", cwd=tmp)
    #self.shell_exec(None, "tar", "xf", "default.tar.bz2", cwd=tmp)
    #self.shell_exec(None, "hg", "clone", "https://bitbucket.org/pypy/example-interpreter", "kermit", cwd=tmp)
    #    tmp = self.test_tmp
    #    self.jitlog_exec(join(tmp,"pypy/rpython/bin/rpython"),
    #                     "--annotate", join(tmp,"kermit/targetkermit.py"),
    #                     "--web", env={'PYTHONPATH':join(tmp,'pypy')})

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

