import asyncio
import json
import base58
import os
import sys
from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.system_program import TransferParams, transfer
from solders.transaction import Transaction
from solders.message import Message
from solders.instruction import Instruction
from solders.hash import Hash

# Note this will be removed with CI packaging to allow graceful import
# Get the absolute path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the jito-py-rpc directory to the Python path (NOTE: Only used until pip CI is stable)
jito_sdk_path = os.path.join(current_dir, 'jito-py-rpc')
sys.path.append(jito_sdk_path)

# Import the JitoJsonRpcSDK
from sdk.jito_jsonrpc_sdk import JitoJsonRpcSDK

async def check_bundle_status(sdk: JitoJsonRpcSDK, bundle_id: str, max_attempts: int = 30, delay: float = 2.0):
    for attempt in range(max_attempts):
        response = sdk.get_inflight_bundle_statuses([bundle_id])
        
        if not response['success']:
            print(f"Error checking bundle status: {response.get('error', 'Unknown error')}")
            await asyncio.sleep(delay)
            continue
        
        print(f"Raw response (Attempt {attempt + 1}/{max_attempts}):")
        print(json.dumps(response, indent=2))
        
        if 'result' not in response['data']:
            print(f"Unexpected response structure. 'result' not found in response data.")
            await asyncio.sleep(delay)
            continue
        
        result = response['data']['result']
        if 'value' not in result or not result['value']:
            print(f"Bundle {bundle_id} not found in response")
            await asyncio.sleep(delay)
            continue
        
        bundle_status = result['value'][0]
        status = bundle_status.get('status')
        print(f"Attempt {attempt + 1}/{max_attempts}: Bundle status - {status}")
        
        if status == 'Landed':
            print(f"Bundle {bundle_id} has landed on-chain! Performing additional confirmation...")
            final_status = await confirm_landed_bundle(sdk, bundle_id)
            return final_status
        elif status == 'Failed':
            print(f"Bundle {bundle_id} has failed.")
            return status
        elif status == 'Invalid':
            if attempt < 5:  # Check a few more times before giving up on Invalid(usually on start)
                print(f"Bundle {bundle_id} is currently invalid. Checking again...")
            else:
                print(f"Bundle {bundle_id} is invalid (not in system or outside 5-minute window).")
                return status
        elif status == 'Pending':
            print(f"Bundle {bundle_id} is still pending. Checking again in {delay} seconds...")
        else:
            print(f"Unknown status '{status}' for bundle {bundle_id}")
        
        await asyncio.sleep(delay)
    
    print(f"Max attempts reached. Final status of bundle {bundle_id}: {status}")
    return status

async def confirm_landed_bundle(sdk: JitoJsonRpcSDK, bundle_id: str, max_attempts: int = 60, delay: float = 2.0):
    for attempt in range(max_attempts):
        response = sdk.get_bundle_statuses([bundle_id])
        
        if not response['success']:
            print(f"Error confirming bundle status: {response.get('error', 'Unknown error')}")
            await asyncio.sleep(delay)
        
        print(f"Confirmation attempt {attempt + 1}/{max_attempts}:")
        print(json.dumps(response, indent=2))
        
        if 'result' not in response['data']:
            print(f"Unexpected response structure. 'result' not found in response data.")
            await asyncio.sleep(delay)
        
        result = response['data']['result']
        if 'value' not in result or not result['value']:
            print(f"Bundle {bundle_id} not found in confirmation response")
            await asyncio.sleep(delay)
        
        bundle_status = result['value'][0]
        if bundle_status['bundle_id'] != bundle_id:
            print(f"Unexpected bundle ID in response: {bundle_status['bundle_id']}")
            await asyncio.sleep(delay)
        
        status = bundle_status.get('confirmation_status')
        
        if status == 'finalized':
            print(f"Bundle {bundle_id} has been finalized on-chain!")
            # Extract transaction ID and construct Solscan link
            if 'transactions' in bundle_status and bundle_status['transactions']:
                tx_id = bundle_status['transactions'][0]
                solscan_link = f"https://solscan.io/tx/{tx_id}"
                print(f"Transaction details: {solscan_link}")
            else:
                print("Transaction ID not found in the response.")
            return 'Finalized'
        elif status == 'confirmed':
            print(f"Bundle {bundle_id} is confirmed but not yet finalized. Checking again...")
        elif status == 'processed':
            print(f"Bundle {bundle_id} is processed but not yet confirmed. Checking again...")
        else:
            print(f"Unexpected status '{status}' during confirmation for bundle {bundle_id}")
        
        # Check for errors
        err = bundle_status.get('err', {}).get('Ok')
        if err is not None:
            print(f"Error in bundle {bundle_id}: {err}")
            return 'Failed'
        
        await asyncio.sleep(delay)
    
    print(f"Max confirmation attempts reached. Unable to confirm finalization of bundle {bundle_id}")
    return 'Landed'
async def basic_bundle():
    # Initialize connection to Solana testnet
    solana_client = AsyncClient("https://api.mainnet-beta.solana.com")

    # Read wallet from local path
    wallet_path = "/path/to/wallet.json"
    with open(wallet_path, 'r') as file:
        wallet_keypair_data = json.load(file)
    wallet_keypair = Keypair.from_bytes(bytes(wallet_keypair_data))

    # Initialize JitoJsonRpcSDK
    jito_client = JitoJsonRpcSDK(url="https://mainnet.block-engine.jito.wtf/api/v1")

    #Example using UUID
    #jito_client = JitoJsonRpcSDK(url="https://mainnet.block-engine.jito.wtf/api/v1", uuid_var="YOUR_UUID" )  

    # Set up transaction parameters
    receiver = Pubkey.from_string("YOUR_RECIEVER_KEY")
    jito_tip_account = Pubkey.from_string(jito_client.get_random_tip_account())
    jito_tip_amount = 1000  # lamports
    transfer_amount = 1000  # lamports

    # Memo program ID
    memo_program_id = Pubkey.from_string("MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr")

    # Create instructions
    transfer_ix = transfer(TransferParams(
        from_pubkey=wallet_keypair.pubkey(),
        to_pubkey=receiver,
        lamports=transfer_amount
    ))

    tip_ix = transfer(TransferParams(
        from_pubkey=wallet_keypair.pubkey(),
        to_pubkey=jito_tip_account,
        lamports=jito_tip_amount
    ))

    memo_ix = Instruction(
        program_id=memo_program_id,
        accounts=[],
        data=bytes("Let's Jito!", "utf-8")
    )

    # Get recent blockhash
    recent_blockhash = await solana_client.get_latest_blockhash()

    # Create the transaction
    message = Message.new_with_blockhash(
        [transfer_ix, tip_ix, memo_ix],
        wallet_keypair.pubkey(),
        recent_blockhash.value.blockhash
    )
    transaction = Transaction.new_unsigned(message)

    # Sign the transaction
    transaction.sign([wallet_keypair], recent_blockhash.value.blockhash)

    # Serialize and base58 encode the entire signed transaction
    serialized_transaction = base58.b58encode(bytes(transaction)).decode('ascii')

    try:
            # Prepare the bundle request
            bundle_request = [serialized_transaction]
            print(f"Sending bundle request: {json.dumps(bundle_request, indent=2)}")

            # Send the bundle using sendBundle method
            result = jito_client.send_bundle(bundle_request)
            print('Raw API response:', json.dumps(result, indent=2))

            if result['success']:
                bundle_id = result['data']['result']
                print(f"Bundle sent successfully. Bundle ID: {bundle_id}")
                
                # Check the status of the bundle
                final_status = await check_bundle_status(jito_client, bundle_id, max_attempts=30, delay=2.0)
                
                if final_status == 'Finalized':
                    print("Bundle has been confirmed and finalized on-chain.")
                elif final_status == 'Landed':
                    print("Bundle has landed on-chain but could not be confirmed as finalized within the timeout period.")
                else:
                    print(f"Bundle did not land on-chain. Final status: {final_status}")
            else:
                print(f"Failed to send bundle: {result.get('error', 'Unknown error')}")

    except Exception as error:
        print('Error sending or confirming bundle:', str(error))

    # Close the Solana client session
    await solana_client.close()
    
async def confirm_bundle(jito_client, bundle_id, timeout_seconds=60):
    start_time = asyncio.get_event_loop().time()
    
    while asyncio.get_event_loop().time() - start_time < timeout_seconds:
        try:
            status = jito_client.get_bundle_statuses([[bundle_id]])
            print('Bundle status:', status)
            
            if status['success'] and bundle_id in status['data']['result']:
                bundle_status = status['data']['result'][bundle_id]
                if bundle_status['status'] == 'finalized':
                    print('Bundle has been finalized on the blockchain.')
                    return bundle_status
                elif bundle_status['status'] == 'confirmed':
                    print('Bundle has been confirmed but not yet finalized.')
                elif bundle_status['status'] == 'processed':
                    print('Bundle has been processed but not yet confirmed.')
                elif bundle_status['status'] == 'failed':
                    raise Exception(f"Bundle failed: {bundle_status.get('error')}")
                else:
                    print(f"Unknown bundle status: {bundle_status['status']}")
        except Exception as error:
            print('Error checking bundle status:', str(error))

        # Wait for a short time before checking again
        await asyncio.sleep(2)
    
    print(f"Bundle {bundle_id} has not finalized within {timeout_seconds}s, but it may still be in progress.")
    return jito_client.get_bundle_statuses([bundle_id])

if __name__ == "__main__":
    asyncio.run(basic_bundle())