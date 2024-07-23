import requests
import logging
import os

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
    
    self.log = logging.getLogger(self.__class__.__name__)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    self.log.addHandler(handler)
    self.log.setLevel(logging.INFO)
    
    if self.log.isEnabledFor(logging.DEBUG):
      self.log.debug(f"URL : {self.url}")
      self.log.debug(f"ENV VAR for UUID : {self.uuid_var}")

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
          "x-jito-atuh": self.uuid_var
      }
    data = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": method,
        "params": [params]
    }
    
    if self.log.isEnabledFor(logging.DEBUG):
      self.log.debug(f"send_request - endpoint : {self.url + endpoint}")
      self.log.debug(f"send_request - headers : {headers}")
      self.log.debug(f"send_request - data : {data}")

    try:
      resp = requests.post(self.url + endpoint, headers=headers, json=data)
      resp.raise_for_status()
      json_data = resp.json()
      return json_data
    except requests.exceptions.HTTPError as errh:
      return f"HTTP Error: {errh}"
    except requests.exceptions.ConnectionError as errc:
      return f"Error Connecting: {errc}"
    except requests.exceptions.Timeout as errt:
      return f"Timeout Error: {errt}"
    except requests.exceptions.RequestException as err:
      return f"An error occurred: {err}"
  
  #Bundle Endpoint
  def get_tip_accounts(self, params=None):
    if self.uuid_var == None:
      result = self.__send_request(endpoint="/bundles", method="getTipAccounts")
    else:
      result = self.__send_request(endpoint="/bundles?uuid=" + self.uuid_var, method="getTipAccounts")
    
    if self.log.isEnabledFor(logging.DEBUG):
      self.log.debug(f"get_tip_accounts : {result}")
    else:
      self.log.info(result)

  def get_bundle_statuses(self, params=None):
    if self.uuid_var == None:
      result = self.__send_request(endpoint="/bundles", method="getBundleStatuses",params=params)
    else:
      result = self.__send_request(endpoint="/bundles?uuid=" + self.uuid_var, method="getBundleStatuses",params=params)
    
    if self.log.isEnabledFor(logging.DEBUG):
      self.log.debug(f"get_bundle_statuses : {result}")
    else:
      if len(result["result"]["value"]) == 0:
        self.log.info("Warning: getBundleStatuses - Bundle not found")
      else:
        self.log.info(result)

  def send_bundle(self, params=None):
    if self.uuid_var == None:
      result = self.__send_request(endpoint="/bundles",method="sendBundle", params=params)
    else:
      result = self.__send_request(endpoint="/bundles?uuid=" + self.uuid_var, method="sendBundle", params=params)
    
    if self.log.isEnabledFor(logging.DEBUG):
      self.log.debug(f"send_bundle : {result}")
    else:
      self.log.info(result)

  # Transaction Endpoint
  def send_txn(self, params=None):
    if self.uuid_var == None:
      result = self.__send_request(endpoint="/transactions",method="sendTransaction", params=params)
    else:
      result = self.__send_request(endpoint="/transactions?uuid=" + self.uuid_var, method="sendTransaction", params=params)
    
    if self.log.isEnabledFor(logging.DEBUG):
      self.log.debug(f"send_txn : {result}")
    else:
      self.log.info(result)
