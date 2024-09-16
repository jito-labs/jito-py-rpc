import sys
import os
import json
import asyncio
import base58
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.system_program import TransferParams, transfer
from solders.instruction import Instruction
from solders.transaction import Transaction
from solders.compute_budget import set_compute_unit_limit, set_compute_unit_price
from solders.transaction_status import TransactionConfirmationStatus
from solders.signature import Signature
from solana.rpc.async_api import AsyncClient
from solana.exceptions import SolanaRpcException

# Get the absolute path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the jito-py-rpc directory to the Python path (NOTE: Only used until pip CI is stable)
jito_sdk_path = os.path.join(current_dir, 'jito-py-rpc')
sys.path.append(jito_sdk_path)

# Import the JitoJsonRpcSDK
from sdk.jito_jsonrpc_sdk import JitoJsonRpcSDK

async def check_transaction_status(client: AsyncClient, signature_str: str):
    print("Checking transaction status...")
    max_attempts = 60  # 60 seconds
    attempt = 0
    
    signature = Signature.from_string(signature_str)
    
    while attempt < max_attempts:
        try:
            response = await client.get_signature_statuses([signature])
            
            if response.value[0] is not None:
                status = response.value[0]
                slot = status.slot
                confirmations = status.confirmations
                err = status.err
                confirmation_status = status.confirmation_status

                print(f"Slot: {slot}")
                print(f"Confirmations: {confirmations}")
                print(f"Confirmation status: {confirmation_status}")
                
                if err:
                    print(f"Transaction failed with error: {err}")
                    return False
                elif confirmation_status == TransactionConfirmationStatus.Finalized:
                    print("Transaction is finalized.")
                    return True
                elif confirmation_status == TransactionConfirmationStatus.Confirmed:
                    print("Transaction is confirmed but not yet finalized.")
                elif confirmation_status == TransactionConfirmationStatus.Processed:
                    print("Transaction is processed but not yet confirmed or finalized.")
            else:
                print("Transaction status not available yet.")
            
            await asyncio.sleep(1)
            attempt += 1
        except Exception as e:
            print(f"Error checking transaction status: {e}")
            await asyncio.sleep(1)
            attempt += 1
    
    print(f"Transaction not finalized after {max_attempts} attempts.")
    return False

async def send_transaction_with_priority_fee(sdk, solana_client, sender, receiver, amount, jito_tip_amount, priority_fee, compute_unit_limit=100_000):
    try:
        recent_blockhash = await solana_client.get_latest_blockhash()
        
        # Transfer to the known receiver
        transfer_ix = transfer(TransferParams(from_pubkey=sender.pubkey(), to_pubkey=receiver, lamports=amount))
        
        # Jito tip transfer
        jito_tip_account = Pubkey.from_string(sdk.get_random_tip_account())
        jito_tip_ix = transfer(TransferParams(from_pubkey=sender.pubkey(), to_pubkey=jito_tip_account, lamports=jito_tip_amount))
        
        # Priority Fee
        priority_fee_ix = set_compute_unit_price(priority_fee)

        transaction = Transaction.new_signed_with_payer(
            [priority_fee_ix, transfer_ix, jito_tip_ix],
            sender.pubkey(),
            [sender],
            recent_blockhash.value.blockhash
        )

        serialized_transaction = base58.b58encode(bytes(transaction)).decode('ascii')
        
        print(f"Sending transaction with priority fee: {priority_fee} micro-lamports per compute unit")
        print(f"Transfer amount: {amount} lamports to {receiver}")
        print(f"Jito tip amount: {jito_tip_amount} lamports to {jito_tip_account}")
        print(f"Serialized transaction: {serialized_transaction}")
        
        response = sdk.send_txn(params=serialized_transaction, bundleOnly=False)

        if response['success']:
            print(f"Full Jito SDK response: {response}")
            signature_str = response['data']['result']
            print(f"Transaction signature: {signature_str}")

            finalized = await check_transaction_status(solana_client, signature_str)
            
            if finalized:
                print("Transaction has been finalized.")
                solscan_url = f"https://solscan.io/tx/{signature_str}"
                print(f"View transaction details on Solscan: {solscan_url}")
            else:
                print("Transaction was not finalized within the expected time.")
            
            return signature_str
        else:
            print(f"Error sending transaction: {response['error']}")
            return None

    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return None

async def main():
    solana_client = AsyncClient("https://api.mainnet-beta.solana.com")
    sdk = JitoJsonRpcSDK(url="https://mainnet.block-engine.jito.wtf/api/v1")
    wallet_path = "/path/to/wallet.json"
    
    with open(wallet_path, 'r') as file:
        private_key = json.load(file)
        sender = Keypair.from_bytes(bytes(private_key))

    receiver = Pubkey.from_string("YOU_RECIEVER_KEY")

    print(f"Sender public key: {sender.pubkey()}")
    print(f"Receiver public key: {receiver}")

    priority_fee = 1000  # Lamport for priority fee
    amount = 1000  # Lamports to transfer to receiver
    jito_tip_amount = 1000  # Lamports for Jito tip

    signature = await send_transaction_with_priority_fee(sdk, solana_client, sender, receiver, amount, jito_tip_amount, priority_fee)
    
    if signature:
        print(f"Transaction process completed. Signature: {signature}")

    await solana_client.close()

asyncio.run(main())