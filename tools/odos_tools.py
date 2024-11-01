from typing import Optional, Dict, Any, ClassVar
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
import requests
import logging
from decimal import Decimal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_WALLET = "0xD0f61049A8d89c9d24b7D6B54348a4FAfA7C2e01"  # Zero address for quotes

class OdosQuoteInput(BaseModel):
    input_token: str = Field(description="The address of the input token")
    output_token: str = Field(description="The address of the output token")
    amount: str = Field(description="The amount to swap in the token's smallest unit (e.g., Wei)")
    user_address: str = Field(default=DEFAULT_WALLET, description="The user's wallet address")
    chain_id: int = Field(default=8453, description="The chain ID (default: 8453 for Base)")

class OdosQuoteTool(BaseTool):
    name: ClassVar[str] = "GetOdosQuote"
    description: ClassVar[str] = "Get a quote for swapping tokens using the Odos API"
    args_schema: ClassVar[type] = OdosQuoteInput
    return_direct: ClassVar[bool] = True

    def _run(
        self,
        input_token: str,
        output_token: str,
        amount: str,
        user_address: str = DEFAULT_WALLET,
        chain_id: int = 8453,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        """Get a quote from Odos API"""
        try:
            logger.info(f"Getting Odos quote for swap from {input_token} to {output_token}")
            logger.info(f"Amount: {amount}, User Address: {user_address}")
            
            # Ensure we're using a valid address
            if not user_address or user_address == "your_ethereum_wallet_address":
                user_address = DEFAULT_WALLET
            
            quote_url = "https://api.odos.xyz/sor/quote/v2"
            
            # Ensure amount is formatted as a string with no decimals
            cleaned_amount = str(int(Decimal(amount)))
            
            quote_request = {
                "chainId": chain_id,
                "inputTokens": [{
                    "tokenAddress": input_token,
                    "amount": cleaned_amount
                }],
                "outputTokens": [{
                    "tokenAddress": output_token,
                    "proportion": 1
                }],
                "slippageLimitPercent": 1.0,
                "userAddr": user_address,
                "disableRFQs": True,
                "compact": True
            }
            
            logger.info(f"Sending quote request: {quote_request}")
            
            response = requests.post(
                quote_url,
                headers={"Content-Type": "application/json"},
                json=quote_request
            )
            
            response.raise_for_status()
            
            quote_data = response.json()
            logger.info(f"Received quote data: {quote_data}")

            # Handle both compact and full response formats
            output_amount = None
            if "outAmounts" in quote_data and len(quote_data["outAmounts"]) > 0:
                output_amount = quote_data["outAmounts"][0]
            elif "outputTokens" in quote_data and len(quote_data["outputTokens"]) > 0:
                output_amount = quote_data["outputTokens"][0].get("amount")

            return {
                "status": "success",
                "quote": quote_data,
                "pathId": quote_data.get("pathId"),
                "inputAmount": cleaned_amount,
                "outputAmount": output_amount,
                "estimatedGas": quote_data.get("gasEstimate", 0)
            }
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to get quote: {e.response.text if hasattr(e, 'response') else str(e)}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}
        except Exception as e:
            error_msg = f"Error getting Odos quote: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {"status": "error", "message": error_msg}

class OdosExecuteInput(BaseModel):
    user_address: str = Field(description="The user's wallet address")
    path_id: str = Field(description="The pathId received from the quote")
    chain_id: int = Field(default=8453, description="The chain ID (default: 8453 for Base)")

class OdosExecuteTool(BaseTool):
    name: ClassVar[str] = "ExecuteOdosSwap"
    description: ClassVar[str] = "Execute a token swap using the Odos API"
    args_schema: ClassVar[type] = OdosExecuteInput
    return_direct: ClassVar[bool] = True

    def _run(
        self,
        user_address: str,
        path_id: str,
        chain_id: int = 8453,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        """Assemble and execute the swap transaction"""
        try:
            if not user_address or user_address == "your_ethereum_wallet_address":
                raise ValueError("A valid wallet address is required for execution")

            logger.info(f"Assembling Odos swap transaction for pathId: {path_id}")
            
            assemble_url = "https://api.odos.xyz/sor/assemble/v2"
            
            assemble_request = {
                "userAddr": user_address,
                "pathId": path_id,
                "chainId": chain_id,
                "simulate": True
            }
            
            logger.info(f"Sending assemble request: {assemble_request}")
            
            response = requests.post(
                assemble_url,
                headers={"Content-Type": "application/json"},
                json=assemble_request
            )
            
            response.raise_for_status()
            
            transaction_data = response.json()
            logger.info("Transaction assembled successfully")
            return {
                "status": "success",
                "transaction": transaction_data
            }
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to assemble transaction: {e.response.text if hasattr(e, 'response') else str(e)}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}
        except Exception as e:
            error_msg = f"Error assembling transaction: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {"status": "error", "message": error_msg}