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
            driver.get(local_url("#/1111/traces"))
            wait.until(lambda d: not query1(d, '#loading_img').is_displayed())

            # will blow up if not present
            select_trace_entry(driver, wait, "schedule")

    def test_filter_checkboxes(self, drivers):
        for driver in drivers:
            wait = ui.WebDriverWait(driver,20)
            driver.get(local_url("#/1111/traces"))
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
