# Welcome to the Jito Python JSON RPC SDK!

[![Discord](https://img.shields.io/discord)](https://discord.gg/jito)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)


This is a minimal SDK that interfaces with the Block-Engine JSON-RPC API using [JSON-RPC 2.0](https://www.jsonrpc.org/specification) specification.

#### Jito MEV Background
For additional information on Jito MEV topics:

https://jito-labs.gitbook.io/mev

#### Jito JSON-RPC HTTP Method
For more information on the complete JSON-RPC method specification:

https://github.com/jito-labs/mev-protos/blob/master/json_rpc/http.md

## Getting Started

### Setting Up the SDK

#### Step 1: Clone the Repository
Clone the [repo](https://github.com/mdr0id/JitoJsonRpcSDK) to your local machine.

```
git clone git@github.com:mdr0id/JitoJsonRpcSDK.git
```

#### Step 2: Install Dependencies
You will need the Python `requests` module to make HTTP requests. If you don't have `requests` installed, you can install it using pip:

```
pip install requests
```

## Using the SDK
#### Step 1: Import the SDK

```
from sdk.jito_jsonrpc_sdk import JitoJsonRpcSDK
```

#### Step 2: Initialize the SDK
Depending on what network you would like to connect to, please select one of the following(e.g mainnet or testnet).

#### Step 3 (Optional): Environment Config for Authentication
If you are using authentication with UUIDs it is recommended to setup an `.envrc` like below:

```
export JITO_UUID=513f9c0c-260d-4e14-b5b4-495785548cd2
```

For instructions on setting up `direnv` please look [here](https://direnv.net/docs/installation.html)


##### Mainnet
For current list of of `mainnet` addresses, please see:

https://jito-labs.gitbook.io/mev/searcher-resources/block-engine/mainnet-addresses
```
BLOCK_ENG_URL = "https://mainnet.block-engine.jito.wtf:443/api/v1/bundles"
sdk = JitoJsonRpcSDK(BLOCK_ENG_URL)
```
##### Testnet
For current list of of `testnet` addresses, please see:

https://jito-labs.gitbook.io/mev/searcher-resources/block-engine/testnet-addresses
```
BLOCK_ENG_URL = "https://dallas.testnet.block-engine.jito.wtf/api/v1/bundles"
sdk = JitoJsonRpcSDK(BLOCK_ENG_URL)
```

#### Step 3: Call JSON-RPC Methods
You can now call JSON-RPC methods defined in the `http.md` document:

https://github.com/jito-labs/mev-protos/blob/master/json_rpc/http.md#json-rpc-api-reference

##### Example: getTipAccounts

###### Parameters
- `None`
  
```
sdk.get_tip_accounts()
```

##### Example: sendBundle

###### Parameters
- `<array[string]>`: `required` Fully-signed Transactions, as encoded string (base-58) upto a maximum of 5. Please note that at this point, we don't support base-64 encoded transactions

```
params =  [
      "4VbvoRYXFaXzDBUYfMXP1irhMZ9XRE6F1keS8GbYzKxgdpEasZtRv6GXxbygPp3yBVeSR4wN9JEauSTnVTKjuq3ktM3JpMebYpdGxZWUttJv9N2DzxBm4vhySdq2hbu1LQX7WxS2xsHG6vNwVCjP33Z2ZLP7S5dZujcan1Xq5Z2HibbbK3M3LD59QVuczyK44Fe3k27kVQ43oRH5L7KgpUS1vBoqTd9ZTzC32H62WPHJeLrQiNkmSB668FivXBAfMg13Svgiu9E",
      "6HZu11s3SDBz5ytDj1tyBuoeUnwa1wPoKvq6ffivmfhTGahe3xvGpizJkofHCeDn1UgPN8sLABueKE326aGLXkn5yQyrrpuRF9q1TPZqqBMzcDvoJS1khPBprxnXcxNhMUbV78cS2R8LrCU29wjYk5b4JpVtF23ys4ZBZoNZKmPekAW9odcPVXb9HoMnWvx8xwqd7GsVB56R343vAX6HGUMoiB1WgR9jznG655WiXQTff5gPsCP3QJFTXC7iYEYtrcA3dUeZ3q4YK9ipdYZsgAS9H46i9dhDP2Zx3"
    ]
sdk.send_bundle(params)
```

##### Example: getBundleStatuses

###### Parameters
- `<array[string]>`: `required` An array of bundle ids to confirm, as base-58 encoded strings (up to a maximum of 5).
```
params = ["892b79ed49138bfb3aa5441f0df6e06ef34f9ee8f3976c15b323605bae0cf51d"]
sdk.get_bundle_statuses(params)
```

##### Example: sendTransaction

###### Parameters
- `[string]`: `required` Fully-signed Transaction, as encoded string.
```
params =  [
      "4hXTCkRzt9WyecNzV1XPgCDfGAZzQKNxLXgynz5QDuWWPSAZBZSHptvWRL3BjCvzUXRdKvHL2b7yGrRQcWyaqsaBCncVG7BFggS8w9snUts67BSh3EqKpXLUm5UMHfD7ZBe9GhARjbNQMLJ1QD3Spr6oMTBU6EhdB4RD8CP2xUxr2u3d6fos36PD98XS6oX8TQjLpsMwncs5DAMiD4nNnR8NBfyghGCWvCVifVwvA8B8TJxE1aiyiv2L429BCWfyzAme5sZW8rDb14NeCQHhZbtNqfXhcp2tAnaAT"
    ]
sdk.send_txn(params)
```

### Step 4: Handling Responses
The sdk RPC methods return the JSON response from the server. You can then handle the response according to your program's requirements. For an example, please see example.py when handling a bundle that was not found.
