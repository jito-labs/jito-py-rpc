import requests
import os
import json
import random

# Jito JSON RPC SDK
# Bindings for https://github.com/jito-labs/mev-protos/blob/master/json_rpc/http.md
class JitoJsonRpcSDK:
  # Initialize a block engine URL
  def __init__(self, url, uuid_var=None):
    self.url = url
    if uuid_var == None:
      self.uuid_var = None
    else:
      self.uuid_var = self.__get_uuid(uuid_var)

  def __get_uuid(self, uuid_var):
    return os.getenv(uuid_var)

  # Send a request to the Block engine url using the JSON RPC methods 
  def __send_request(self, endpoint, method, params=None):
    if endpoint == None:
      return "Error: Please enter a valid endpoint."
    
    if self.uuid_var == None:
      headers = {
          'Content-Type': 'application/json', 
          "accept": "application/json"
      }
    else:
      headers = {
          'Content-Type': 'application/json', 
          "accept": "application/json",
          "x-jito-auth": self.uuid_var
      }
    # Only add encoding parameter for sendBundle and sendTransaction methods
    if method in ["sendBundle", "sendTransaction"]:
        data = {
            "id": 1,
            "jsonrpc": "2.0",
            "method": method,
            "params": [params, {"encoding": "base64"}]
        }
    else:
        data = {
            "id": 1,
            "jsonrpc": "2.0",
            "method": method,
            "params": [params]
        }

    print(data)
    try:
      resp = requests.post(self.url + endpoint, headers=headers, json=data)
      resp.raise_for_status()
      return {"success": True, "data": resp.json()}
    except requests.exceptions.HTTPError as errh:
      return {"success": False, "error": f"HTTP Error: {errh}"}
    except requests.exceptions.ConnectionError as errc:
      return {"success": False, "error": f"Error Connecting: {errc}"}
    except requests.exceptions.Timeout as errt:
      return {"success": False, "error": f"Timeout Error: {errt}"}
    except requests.exceptions.InvalidHeader as err:
      return {"success": False, "error": f"Invalid Header error: {err}"}
    except requests.exceptions.InvalidURL as err:
      return {"success": False, "error": f"InvalidURL error: {err}"}
    except requests.exceptions.RequestException as err:
      return {"success": False, "error": f"An error occurred: {err}"}
  
  #Bundle Endpoint
  def get_tip_accounts(self, params=None):
    if self.uuid_var == None:
      return self.__send_request(endpoint="/bundles", method="getTipAccounts")
    else:
      return self.__send_request(endpoint="/bundles?uuid=" + self.uuid_var, method="getTipAccounts")
  
  def get_random_tip_account(self):
    response = self.get_tip_accounts()
    if not response['success']:
        print(f"Error getting tip accounts: {response.get('error', 'Unknown error')}")
        return None
    
    tip_accounts = response['data']['result']
    if not tip_accounts:
        print("No tip accounts found.")
        return None
    
    random_account = random.choice(tip_accounts)
    return random_account


  def get_bundle_statuses(self, bundle_uuids):
      endpoint = "/getBundleStatuses"
      if self.uuid_var is not None:
          endpoint += f"?uuid={self.uuid_var}"
      
      # Ensure bundle_uuids is a list
      if not isinstance(bundle_uuids, list):
          bundle_uuids = [bundle_uuids]
      
      # Correct format for the request
      params = bundle_uuids
      
      return self.__send_request(endpoint=endpoint, method="getBundleStatuses", params=params)

  def send_bundle(self, params=None):
    if self.uuid_var == None:
      return self.__send_request(endpoint="/bundles",method="sendBundle", params=params)
    else:
      return  self.__send_request(endpoint="/bundles?uuid=" + self.uuid_var, method="sendBundle", params=params)
  
  def get_inflight_bundle_statuses(self, bundle_uuids):
    endpoint = "/getInflightBundleStatuses"
    if self.uuid_var is not None:
        endpoint += f"?uuid={self.uuid_var}"
    
    # Ensure bundle_uuids is a list
    if not isinstance(bundle_uuids, list):
        bundle_uuids = [bundle_uuids]
    
    # Correct format for the request
    params = bundle_uuids
    
    return self.__send_request(endpoint=endpoint, method="getInflightBundleStatuses", params=params)

  # Transaction Endpoint
  def send_txn(self, params=None, bundleOnly=False):
    ep = "/transactions"
    query_params = []

    if bundleOnly:
        query_params.append("bundleOnly=true")
    
    if self.uuid_var is not None:
        query_params.append(f"uuid={self.uuid_var}")

    if query_params:
        ep += "?" + "&".join(query_params)

    return self.__send_request(endpoint=ep, method="sendTransaction", params=params)
