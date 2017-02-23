
from testvmprof.support import output_extract_urls

def test_output_extract_urls_empty():
    urls = output_extract_urls("")
    assert urls == {}

def test_output_extract_urls():
    output = """2500
Uploading to http://localhost:8000...
 => Uploading the cpu profile...
      http://localhost:8000/#/22035e02-2c9b-4927-bde4-d458cec099d4
 => Uploading the jit log...
      http://localhost:8000/#/f79d0e1b-cbae-410f-bd06-8f650770af24/traces
mem.c: 21 mallocs left (use PYPY_ALLOC=1 to see the list)\n
"""
    urls = output_extract_urls(output)
    assert urls == {
            "cpu": "http://localhost:8000/#/22035e02-2c9b-4927-bde4-d458cec099d4",
            "jit": "http://localhost:8000/#/f79d0e1b-cbae-410f-bd06-8f650770af24/traces"
    }
