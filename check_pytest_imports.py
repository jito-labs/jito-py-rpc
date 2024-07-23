import jito_jsonrpc_sdk
import sys

def test_import():
    print(jito_jsonrpc_sdk.__file__)
    assert 'jito_jsonrpc_sdk' in sys.modules
