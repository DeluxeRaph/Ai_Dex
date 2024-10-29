import os
import json
import time
from cdp import *
from typing import Dict, Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

# Configure CDP SDK
Cdp.configure_from_json("./secrets/cdp_api_key.json")
print("CDP SDK has been successfully configured from JSON file.")

# Initialize the LLM with the OpenAI API key from the environment
llm = ChatOpenAI(model="gpt-4o-mini", temperature=1, api_key=os.getenv("OPENAI_API_KEY"))

class AiSwapper:
    def __init__(self):
        self.wallet_address = None
        self.cdp = Cdp()

    def create_wallet(self) -> str:
        """Create a new wallet and return its address"""
        try:
            wallet = self.cdp.create_wallet()
            self.wallet_address = wallet.address
            return self.wallet_address
        except Exception as e:
            raise Exception(f"Failed to create wallet: {str(e)}")

    def check_balance(self) -> Dict:
        """Check wallet balance"""
        try:
            if not self.wallet_address:
                raise Exception("No wallet created yet")
            return self.cdp.get_balances(self.wallet_address)
        except Exception as e:
            raise Exception(f"Failed to get balance: {str(e)}")

######

# Want to swap tokens

# check balance

# make api call for the token pairs on odos dex aggreator

# Get qoute for swap

# make confirm swap

# receive swapped tokens

# check balance