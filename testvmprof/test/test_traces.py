import pytest
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from testvmprof.ui import (reset_search_criteria,
    select_trace_entry, drivers, query1, query,
    local_url)

class TestTracesView(object):
    def test_display_schedule(self, drivers):
        for driver in drivers:
            wait = ui.WebDriverWait(driver,10)
            driver.get(local_url("#/richards/traces"))
            wait.until(lambda d: not query1(d, '#loading_img').is_displayed())

            # will blow up if not present
            select_trace_entry(driver, wait, "schedule")

    def test_filter_checkboxes(self, drivers):
        for driver in drivers:
            wait = ui.WebDriverWait(driver,20)
            driver.get(local_url("#/richards/traces"))
            wait.until(lambda d: not query1(d, '#loading_img').is_displayed())
            for elem in driver.find_elements_by_css_selector('li.trace-entry span.trace-name'):
                if 'schedule' in elem.text:
                    break
            else:
                pytest.fail("could not find 'schedule' function in trace view")


            count = len(driver.find_elements_by_css_selector('li.trace-entry'))

            bridge_checkbox = driver.find_element_by_id("filter_bridge")
            bridge_checkbox.click() # it is now on

            # there must be more bridges filtered
            assert count < len(driver.find_elements_by_css_selector('li.trace-entry'))

            bridge_checkbox.click() # it is now off
            loop_checkbox = driver.find_element_by_id("filter_loop")
            loop_checkbox.click() # do not show loops!

            assert len(driver.find_elements_by_css_selector('li.trace-entry')) == 0
            reset_search_criteria(driver)

    def test_search_traces(self, drivers):
        for driver in drivers:
            wait = ui.WebDriverWait(driver,20)
            driver.get(local_url("#/1v1/traces"))
            wait.until(lambda d: not query1(d, '#loading_img').is_displayed())
            search_input = driver.find_element_by_id("filter_text")
            assert len(driver.find_elements_by_css_selector('li.trace-entry')) > 1
            search_input.send_keys("funcname1")
            loop_checkbox = driver.find_element_by_id("filter_loop")
            assert len(driver.find_elements_by_css_selector('li.trace-entry')) == 1

    def test_load_trace(self, drivers):
        for driver in drivers:
            wait = ui.WebDriverWait(driver,10)
            driver.get(local_url("#/1v1/traces"))
            wait.until(lambda d: not query1(d, '#loading_img').is_displayed())
            select_trace_entry(driver, wait, "funcname1")
            query1(driver, "#switch_trace_rewritten").click()
            names = set()
            for line in driver.find_elements_by_css_selector(".resops > .trace-line"):
                names.add(query1(line, ".resop-name").text)
            assert len(names) == 2
            assert 'int_add' in names
            assert 'guard_true' in names

    def test_switch_to_opt(self, drivers):
        for driver in drivers:
            wait = ui.WebDriverWait(driver,10)
            driver.get(local_url("#/1v1/traces"))
            wait.until(lambda d: not query1(d, '#loading_img').is_displayed())
            select_trace_entry(driver, wait, "funcname1")
            query1(driver, "#switch_trace_opt").click()
            names = set()
            for line in query(driver, ".resops > .trace-line"):
                names.add(query1(line, ".resop-name").text)
            assert len(names) == 3
            assert 'jump' in names
            assert 'int_add' in names
            assert 'guard_true' in names

    def test_display_asm(self, drivers):
        for driver in drivers:
            wait = ui.WebDriverWait(driver,10)
            driver.get(local_url("#/1v1/traces"))
            wait.until(lambda d: not query1(d, '#loading_img').is_displayed())
            select_trace_entry(driver, wait, "func_with_nop_assembly")
            #
            query1(driver, "#switch_trace_asm").click()
            asm = []
            for line in query(driver, ".trace-asm-line > div"):
                asm.append(line.text.strip())
            assert asm == ["nop"] * 3

    def test_powerpc_asm(self, drivers):
        for driver in drivers:
            wait = ui.WebDriverWait(driver,10)
            driver.get(local_url("#/ppc64lev1/traces"))
            wait.until(lambda d: not query1(d, '#loading_img').is_displayed())
            select_trace_entry(driver, wait, "ppcloop")
            #
            query1(driver, "#switch_trace_asm").click()
            asm = []
            for line in query(driver, ".trace-asm-line > div"):
                asm.append(line.text.strip())
            assert asm == ["ld r9, 0x10(r6)", "std r9, 0x10(r6)"]

    def test_no_merge_point_source_duplication(self, drivers):
        for driver in drivers:
            wait = ui.WebDriverWait(driver,10)
            driver.get(local_url("#/1v1/traces"))
            wait.until(lambda d: not query1(d, '#loading_img').is_displayed())
            select_trace_entry(driver, wait, "func_opcode_and_dup_merge_points")
            query1(driver, "#switch_trace_opt").click()

            # enable source code show
            while not query1(driver, "input#show_source_code").is_selected():
                query1(driver, "#show_source_code").click()
            names = []
            for elem in query(driver, "code.trace-source > pre"):
                names.append(elem.text.strip())
            # assert no duplicate
            assert len(names) == len(set(names))
            assert 'a = b + c' in names
            assert 'def wait_for_me():' in names
            assert 'yield 13' in names
            assert 'a,b,c = call.me(1,2,3) # here is a comment' in names

            # disable source code show
            while query1(driver, "input#show_source_code").is_selected():
                query1(driver, "#show_source_code").click()

            names = []
            for elem in query(driver, "code.trace-source > pre"):
                names.append(elem.text.strip())
            # assert empty
            assert names == []

    def test_display_bytecode(self, drivers):
        for driver in drivers:
            wait = ui.WebDriverWait(driver,10)
            driver.get(local_url("#/1v1/traces"))
            wait.until(lambda d: not query1(d, '#loading_img').is_displayed())
            select_trace_entry(driver, wait, "func_opcode_and_dup_merge_points")
            query1(driver, "#switch_trace_opt").click()
            while not query1(driver, "input#show_bytecodes").is_selected():
                query1(driver, "#show_bytecodes").click()
            bytecodes = []
            for elem in query(driver, "code.trace-bytecode > pre"):
                bytecodes.append(elem.text.strip())
            assert bytecodes == ['LOAD_FAST', 'LOAD_FAST', 'LOAD_FAST', \
                                 'INT_ADD', 'STORE_FAST', 'LOAD_FAST', \
                                 'YIELD', 'YIELD2', 'CALL']

            while query1(driver, "input#show_bytecodes").is_selected():
                query1(driver, "#show_bytecodes").click()
            bytecodes = []
            for elem in query(driver, "code.trace-bytecode > pre"):
                bytecodes.append(elem.text.strip())
            # there should not be any byte code!
            assert bytecodes == []

    def test_sort_traces(self, drivers):
        for dri in drivers:
            dri.get(local_url("#/sortingv2/traces"))
            dri.wait.until(lambda d: not query1(d, '#loading_img').is_displayed())

            def extract_names():
                names = []
                for elem in query(dri, ".trace-entry"):
                    name = query1(elem, '.trace-name')
                    names.append(name.text.strip())
                return names
            #
            query1(dri, '#sort_count').click()
            names = extract_names()
            assert names == ['c order 1', 'b order 3', 'a order 2']

            query1(dri, '#sort_name').click()
            names = extract_names()
            assert names == ['a order 2', 'b order 3', 'c order 1']

            query1(dri, '#sort_recording').click()
            names = extract_names()
            assert names == ['b order 3', 'a order 2', 'c order 1']

    def test_error_loading_nonexistent_trace(self, drivers):
        for dri in drivers:
            dri.get(local_url("#/nonexistenttrace/traces"))
            dri.wait.until(lambda d: not query1(d, '#loading_img').is_displayed())

            assert query1(dri, '#error').is_displayed()
            assert '404 Not Found' in query1(dri, '#error').text

    def test_follow_guard(self, drivers):
        for dri in drivers:
            dri.get(local_url("#/1v1/traces"))
            dri.wait.until(lambda d: not query1(d, '#loading_img').is_displayed())

            select_trace_entry(dri, dri.wait, "unknown")
            query1(dri, "#switch_trace_rewritten").click()
            elem = list(query(dri, '.instr'))[1]
            link = query1(elem, 'a.resop-descr')
            link.click()
            dri.wait.until(lambda d: not query1(d, '#loading_img').is_displayed())
            assert query1(dri, '.parent-failed-guard').text.strip() == 'guard_true(i2) guard_resume'
            resops = query1(dri, '.resops')
            # see loggen.py 2 is the number of that bridge
            assert int(resops.get_attribute("data-trace-id")) == 2
