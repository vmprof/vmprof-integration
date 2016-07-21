from testvmprof.ui import (drivers, query1, query,
        reset_search_criteria, select_trace_entry)
from testvmprof.support import (BaseVMProfTest,
        output_extract_urls)

class VMProfTest(BaseVMProfTest):
    vmprof_url = None
    def test_run_vm_and_upload(self, drivers):
        out, err, retcode = self.pypy_exec("testvmprof/test/examples/simple_loop.py", jitlog=True, upload=True)
        assert(retcode == 0)
        url = output_extract_urls(out)['jitlog']

        for dri in drivers:
            dri.get(url)
            wait_until_loading_complete(dri)
        elems = [elem for elem in \
            driver.find_elements_by_css_selector( \
                      'li.trace-entry span.trace-name')]
        assert elems == ['simple_loop']
        select_trace_entry(dri, dri.wait, 'simple_loop')

        for link in \
            driver.find_elements_by_css_selector('trace-type-switch > li > a'):
            link.click()
            wait_until_loading_complete(dri)
            lines = [line for line in driver.find_elements_by_css_selector(\
                        '.resops .trace-line')]
            assert len(lines) > 0


class TestProduction(VMProfTest):
    vmprof_url = "https://www.vmprof.com"

#class TestLocal(VMProfTest):
#    vmprof_url = "http://localhost:8000"

