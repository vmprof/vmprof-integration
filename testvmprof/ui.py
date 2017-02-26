# import this module only for testing purpose
import pytest
from selenium import webdriver
import selenium.webdriver.support.ui as ui

@pytest.fixture(scope="function")
def drivers(request):
    drivers = [webdriver.Chrome()]
    #if os.environ.get('TRAVIS', 'false') == 'true':
    #    drivers += [webdriver.Firefox()]
    for dri in drivers:
        dri.wait = ui.WebDriverWait(dri, 2)
        request.addfinalizer(dri.quit)
    return drivers

def wait_until_loading_complete(dri):
    dri.wait.until(lambda d: \
            not query1(d, '#loading_img').is_displayed())

def local_url(path):
    host = "http://localhost:8000"
    if path[0] == "/":
        return host + path
    return host + "/" + path

def remote_url(path):
    host = "http://vmprof.com"
    if path[0] == "/":
        return host + path
    return host + "/" + path

def query1(elem, q):
    return elem.find_element_by_css_selector(q)

def query(elem, q):
    return elem.find_elements_by_css_selector(q)

def reset_search_criteria(driver):
    loop_checkbox = driver.find_element_by_id("filter_loop")
    if not loop_checkbox.is_selected():
        loop_checkbox.click() # do not show loops!

    bridge_checkbox = driver.find_element_by_id("filter_bridge")
    if bridge_checkbox.is_selected():
        bridge_checkbox.click() # do not show bridges!

def select_trace_entry(driver, wait, entry_name):
    trace_lines = driver.find_elements_by_css_selector("li.trace-entry")
    for line in trace_lines:
        name = line.find_element_by_css_selector(".trace-name").text
        if name != entry_name:
            continue
        line.click()
        wait.until(lambda d: not query1(d, '#loading_img').is_displayed())
        break
    else:
        pytest.fail("could not select %s in log" % entry_name)
