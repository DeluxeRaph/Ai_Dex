import os  # Add this import
from web3 import Web3
from dotenv import load_dotenv

#Load environment variables
load_dotenv()


def check_eth_balance(address, provider_url):
    # Initialize web3 connection
    w3 = Web3(Web3.HTTPProvider(provider_url))
    
    try:
        # Check if address is valid
        if not Web3.is_address(address):
            return "Invalid Ethereum address"
            
        # Convert address to checksum format
        checksum_address = Web3.to_checksum_address(address)
        
        # Get balance in Wei
        balance_wei = w3.eth.get_balance(checksum_address)
        
        # Convert Wei to ETH
        balance_eth = w3.from_wei(balance_wei, 'ether')
        
        return {
            'address': checksum_address,
            'balance_eth': float(balance_eth),
            'balance_wei': balance_wei
        }
        
    except Exception as e:
        return f"Error: {str(e)}"

# Example usage
if __name__ == "__main__":
    # Replace with your Infura/Alchemy URL or local node
    PROVIDER_URL = os.getenv('WEB3_PROVIDER_URL')
    
    # Replace with the address you want to check
    ADDRESS_TO_CHECK = "0xD0f61049A8d89c9d24b7D6B54348a4FAfA7C2e01"
    
    result = check_eth_balance(ADDRESS_TO_CHECK, PROVIDER_URL)
    print(result)