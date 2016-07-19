
from testvmprof.support import output_extract_urls

def test_output_extract_urls_empty():
    urls = output_extract_urls("")
    assert urls == {}

def test_output_extract_urls():
    output = """2500
Compiling and uploading to http://vmprof.com...
VMProf log: http://vmprof.com/#/6e966f8bd1498571bbf48202c7edd72e
PyPy JIT log: http://vmprof.com/#/b3a936d8a24006b3fdbf805cb5defc11/traces
mem.c: 32 mallocs left (use PYPY_ALLOC=1 to see the list)
"""
    urls = output_extract_urls(output)
    assert urls == {
        "profile": "http://vmprof.com/#/6e966f8bd1498571bbf48202c7edd72e",
        "jitlog": "http://vmprof.com/#/b3a936d8a24006b3fdbf805cb5defc11/traces"
    }
