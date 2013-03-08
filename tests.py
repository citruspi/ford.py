import httplib
import unittest
import subprocess


def test_is_running():

    subprocess.call(["ford.py", "-s", "test-content", "-m", "serve"], shell=True)

    conn = httplib.HTTPConnection("127.0.0.1:8000")
    conn.request("HEAD", "/index.html")
    res = conn.getresponse()

    assert(res.getheaders()[5][1] == 'ford.py')
