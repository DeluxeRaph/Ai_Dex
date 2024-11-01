# test_odos_quote.py
from tools.odos_tools import OdosQuoteTool
import logging

# Configure logging to see debug output
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_get_odos_quote():
    # Initialize the quote tool
    quote_tool = OdosQuoteTool()
    
    # Example parameters
    test_params = {
        "input_token": "0x940181a94A35A4569E4529A3CDfB74e38FD98631",  # AERO token
        "output_token": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",  # USDC token
        "amount": "1000000000000000000",  # 1 AERO in smallest units
        "user_address": "0xD0f61049A8d89c9d24b7D6B54348a4FAfA7C2e01",
        "chain_id": 8453
    }
    
    # Get quote directly
    quote_result = quote_tool._run(**test_params)
    print("Quote result:", quote_result)

if __name__ == "__main__":
    test_get_odos_quote()
