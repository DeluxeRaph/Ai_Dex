from typing import Optional, Dict, Any, ClassVar
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from web3 import Web3
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GetWalletBalanceInput(BaseModel):
    wallet_address: str = Field(description="The Ethereum wallet address to check the balance for")

class GetWalletBalanceTool(BaseTool):
    name: ClassVar[str] = "GetWalletBalance"
    description: ClassVar[str] = "Check the ETH balance of a specified wallet address"
    args_schema: ClassVar[type] = GetWalletBalanceInput
    return_direct: ClassVar[bool] = True

    def _initialize_web3(self) -> Web3:
        """Initialize Web3 connection"""
        provider_url = os.getenv('WEB3_PROVIDER_URL')
        if not provider_url:
            raise ValueError("WEB3_PROVIDER_URL environment variable is not set")
        return Web3(Web3.HTTPProvider(provider_url))

    def _run(
        self,
        wallet_address: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        """Check the wallet balance"""
        try:
            logger.info(f"Checking balance for address: {wallet_address}")
            
            # Initialize web3 connection
            w3 = self._initialize_web3()
            
            # Check if address is valid
            if not Web3.is_address(wallet_address):
                error_msg = f"Invalid Ethereum address: {wallet_address}"
                logger.error(error_msg)
                return {"status": "error", "message": error_msg}
            
            # Convert address to checksum format
            checksum_address = Web3.to_checksum_address(wallet_address)
            
            # Get balance in Wei
            balance_wei = w3.eth.get_balance(checksum_address)
            
            # Convert Wei to ETH
            balance_eth = w3.from_wei(balance_wei, 'ether')
            
            result = {
                "status": "success",
                "address": checksum_address,
                "balance_eth": float(balance_eth),
                "balance_wei": balance_wei
            }
            
            logger.info(f"Balance retrieved successfully: {result}")
            return result
            
        except Exception as e:
            error_msg = f"Error checking balance: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {"status": "error", "message": error_msg}

# Example usage
if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Create tool instance
    balance_tool = GetWalletBalanceTool()
    
    # Test address
    test_address = "0xD0f61049A8d89c9d24b7D6B54348a4FAfA7C2e01"
    
    # Get balance
    result = balance_tool._run(test_address)
    print(result)