from typing import Optional
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from cdp import *
from pydantic import PrivateAttr
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CreateWalletTool(BaseTool):
    name: str = "CreateWallet"
    description: str = "Generate a new Ethereum wallet and return the address and wallet ID"
    return_direct: bool = True
    _cdp: Optional[Cdp] = PrivateAttr() 

    def __init__(self, cdp_instance: Cdp, **kwargs):
        super().__init__(**kwargs)
        self._cdp = cdp_instance  # Assign `cdp_instance` to `_cdp`
        logger.info(f"CDP instance initialized: {self._cdp}")

    def _run(self) -> str:
        """Execute the wallet creation"""
        try:
            logger.info("Running CreateWalletTool...")
                
            logger.info("CDP instance is set. Creating new wallet...")
            wallet = Wallet.create()
            wallet_address = wallet.default_address
            
            result = {
                "status": "success",
                "address": wallet_address,
            }
            
            logger.info(f"Wallet created successfully: {wallet_address}")
            return print(result)
            
        except Exception as e:
            error_msg = f"Failed to create wallet: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return json.dumps({"status": "error", "message": error_msg})
