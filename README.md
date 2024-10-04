# jito-sdk-python

[![Discord](https://img.shields.io/discord/938287290806042626?label=Discord&logo=discord&style=flat&color=7289DA)](https://discord.gg/jTSmEzaR)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![PyPI](https://img.shields.io/pypi/v/jito-py-rpc?label=PyPI&logo=python)
[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://jito-foundation.github.io/jito-sdk-python/)

The Jito JSON-RPC Python SDK provides an interface for interacting with Jito's enhanced Solana infrastructure. This SDK supports methods for managing bundles and transactions, offering improved performance and additional features while interacting with the Block Engine.

## Features

### Bundles
- `get_inflight_bundle_statuses`: Retrieve the status of in-flight bundles.
- `get_bundle_statuses`: Fetch the statuses of submitted bundles.
- `get_tip_accounts`: Get accounts eligible for tips.
- `send_bundle`: Submit bundles to the Jito Block Engine.

### Transactions
- `send_transaction`: Submit transactions with enhanced priority and speed.

## Installation

### Prerequisites

This project requires Python 3.8 or higher. If you haven't installed Python yet, follow these steps:

1. **Install Python**:
   Download and install Python from [python.org](https://www.python.org/downloads/)

2. Verify the installation:
   ```bash
   python --version
   ```

3. (Optional but recommended) Set up a virtual environment:
   ```bash
   python -m venv jito-env
   source jito-env/bin/activate  # On Windows use `jito-env\Scripts\activate`
   ```

### Installing jito-sdk-python

Install the SDK using pip:

```bash
pip install jito-sdk-python
```

## Usage Examples

### Basic Transaction Example


To run the basic transaction example:

1. Ensure your environment is set up in `basic_txn.py`:

   ```python
   # Load the sender's keypair
   wallet_path = "/path/to/wallet.json"

   # Set up receiver pubkey
   receiver = Pubkey.from_string("YOUR_RECEIVER_KEY")
   ```

2. Run the example:
   ```bash
   python basic_txn.py
   ```

### Basic Bundle Example

To run the basic bundle example:

1. Ensure your environment is set up in `basic_bundle.py`:

   ```python
   # Load the sender's keypair
   wallet_path = "/path/to/wallet.json"

   # Set up receiver pubkey
   receiver = Pubkey.from_string("YOUR_RECEIVER_KEY")
   ```

2. Run the example:
   ```bash
   python basic_bundle.py
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For support, please join our [Discord community](https://discord.gg/jTSmEzaR).
