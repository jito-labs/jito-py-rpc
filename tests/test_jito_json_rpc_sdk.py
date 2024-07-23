import pytest
import responses
import os
from jito_jsonrpc_sdk-0.1.0 import JitoJsonRpcSDK

TESTNET_URL = os.getenv('JITO_TESTNET_URL', 'https://dallas.testnet.block-engine.jito.wtf/api/v1')

@responses.activate
def test_get_tip_accounts():
    sdk = JitoJsonRpcSDK(TESTNET_URL)
    
    responses.add(responses.POST, f"{TESTNET_URL}/bundles",
                  json={"result": {"value": []}}, status=200)
    
    result = sdk.get_tip_accounts()
    assert result == {"result": {"value": []}}

@responses.activate
def test_get_bundle_statuses():
    sdk = JitoJsonRpcSDK(TESTNET_URL)
    
    responses.add(responses.POST, f"{TESTNET_URL}/bundles",
                  json={"result": {"value": []}}, status=200)
    
    result = sdk.get_bundle_statuses(params={})
    assert result == {"result": {"value": []}}

@responses.activate
def test_send_bundle():
    sdk = JitoJsonRpcSDK(TESTNET_URL)
    
    responses.add(responses.POST, f"{TESTNET_URL}/bundles",
                  json={"result": "success"}, status=200)
    
    result = sdk.send_bundle(params={})
    assert result == {"result": "success"}

@responses.activate
def test_send_txn():
    sdk = JitoJsonRpcSDK(TESTNET_URL)
    
    responses.add(responses.POST, f"{TESTNET_URL}/transactions",
                  json={"result": "success"}, status=200)
    
    result = sdk.send_txn(params={})
    assert result == {"result": "success"}
