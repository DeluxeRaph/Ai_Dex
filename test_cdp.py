from cdp import *

# Configure the CDP instance from a JSON file
cdp_instance = Cdp.configure_from_json("./secrets/cdp_api_key.json")
if cdp_instance:
    print("CDP SDK has been successfully configured from JSON file.")
else:
    print("Failed to configure CDP SDK from JSON file.")

# Create a wallet with one address by default
wallet = Wallet.create()

address = wallet.default_address
print(f"Wallet created successfully. Default address: {address}")

