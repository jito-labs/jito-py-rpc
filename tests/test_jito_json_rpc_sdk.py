import pytest
import requests_mock
from jito_jsonrpc_sdk import JitoJsonRpcSDK

@pytest.fixture
def sdk():
    return JitoJsonRpcSDK(url="https://dallas.testnet.block-engine.jito.wtf/api/v1", uuid_var="TEST_UUID")

def test_get_tip_accounts(sdk, requests_mock):
    requests_mock.post("https://dallas.testnet.block-engine.jito.wtf/api/v1", json={"status_code": 200}, status_code=200)
    result = sdk.get_tip_accounts()
    if result is None:
        print("there be nothing here from this call")
    
    print(result)
    assert result.status_code == 200
    #assert result['data']['result'] == "success"

def test_get_bundle_statuses(sdk, requests_mock):
    requests_mock.post("https://dallas.testnet.block-engine.jito.wtf/api/v1/bundles", json={"result": {"value": []}}, status_code=200)
    result = sdk.get_bundle_statuses(params={"bundleId": "123"})
    assert result['status_code'] == 200
    #assert result['data']['result']['value'] == []

def test_send_bundle(sdk, requests_mock):
    requests_mock.post("https://dallas.testnet.block-engine.jito.wtf/api/v1/bundles", json={"result": "bundle_sent"}, status_code=200)
    result = sdk.send_bundle(params={"bundleData": "data"})
    assert result['status_code'] == 200
    #assert result['data']['result'] == "bundle_sent"

def test_send_txn(sdk, requests_mock):
    requests_mock.post("https://dallas.testnet.block-engine.jito.wtf/api/v1/transactions", json={"result": "txn_sent"}, status_code=200)
    result = sdk.send_txn(params={"txnData": "data"})
    assert result['status_code'] == 200
    #assert result['data']['result'] == "txn_sent"