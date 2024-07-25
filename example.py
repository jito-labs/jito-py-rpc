from sdk.jito_jsonrpc_sdk import JitoJsonRpcSDK


def main():
  # Initialize the SDK
  # mainnet
  #BLOCK_ENG_URL = "https://mainnet.block-engine.jito.wtf:443/api/v1"

  # testnet
  BLOCK_ENG_URL = "https://dallas.testnet.block-engine.jito.wtf/api/v1"
  sdk = JitoJsonRpcSDK(BLOCK_ENG_URL)
  
  # If you are using authentication which is not needed unless you request rate limit increase
  #UUID_ENV = "JITO_UUID"
  #sdk = JitoJsonRpcSDK(BLOCK_ENG_URL, UUID_ENV)

  result = sdk.get_tip_accounts()
  print(result)

  params =  [
        "4VbvoRYXFaXzDBUYfMXP1irhMZ9XRE6F1keS8GbYzKxgdpEasZtRv6GXxbygPp3yBVeSR4wN9JEauSTnVTKjuq3ktM3JpMebYpdGxZWUttJv9N2DzxBm4vhySdq2hbu1LQX7WxS2xsHG6vNwVCjP33Z2ZLP7S5dZujcan1Xq5Z2HibbbK3M3LD59QVuczyK44Fe3k27kVQ43oRH5L7KgpUS1vBoqTd9ZTzC32H62WPHJeLrQiNkmSB668FivXBAfMg13Svgiu9E",
        "6HZu11s3SDBz5ytDj1tyBuoeUnwa1wPoKvq6ffivmfhTGahe3xvGpizJkofHCeDn1UgPN8sLABueKE326aGLXkn5yQyrrpuRF9q1TPZqqBMzcDvoJS1khPBprxnXcxNhMUbV78cS2R8LrCU29wjYk5b4JpVtF23ys4ZBZoNZKmPekAW9odcPVXb9HoMnWvx8xwqd7GsVB56R343vAX6HGUMoiB1WgR9jznG655WiXQTff5gPsCP3QJFTXC7iYEYtrcA3dUeZ3q4YK9ipdYZsgAS9H46i9dhDP2Zx3"
      ]
  result = sdk.send_bundle(params)
  print(result)

  params = ["892b79ed49138bfb3aa5441f0df6e06ef34f9ee8f3976c15b323605bae0cf51d"]
  result = sdk.get_bundle_statuses(params)
  print(result)

  params =  [
       "4hXTCkRzt9WyecNzV1XPgCDfGAZzQKNxLXgynz5QDuWWPSAZBZSHptvWRL3BjCvzUXRdKvHL2b7yGrRQcWyaqsaBCncVG7BFggS8w9snUts67BSh3EqKpXLUm5UMHfD7ZBe9GhARjbNQMLJ1QD3Spr6oMTBU6EhdB4RD8CP2xUxr2u3d6fos36PD98XS6oX8TQjLpsMwncs5DAMiD4nNnR8NBfyghGCWvCVifVwvA8B8TJxE1aiyiv2L429BCWfyzAme5sZW8rDb14NeCQHhZbtNqfXhcp2tAnaAT"
     ]
  result = sdk.send_txn(params)
  print(result)


if __name__ == "__main__":
  main()
