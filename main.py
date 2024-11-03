# main.py
from dotenv import load_dotenv
import os
from cdp import *
from langchain_openai import ChatOpenAI
from tools.create_wallet import CreateWalletTool
from tools.check_balance import GetWalletBalanceTool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.prebuilt import create_react_agent
from tools.odos_tools import OdosQuoteTool, OdosExecuteTool
import logging
from typing import List, Tuple
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Token configuration
TOKEN_CONFIG = {
    'USDC': {
        'address': '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
        'decimals': 6
    },
    'AERO': {
        'address': '0x940181a94A35A4569E4529A3CDfB74e38FD98631',
        'decimals': 18
    }
}

class AgentChat:
    def __init__(self):
        self.conversation_history: List[Tuple[str, str]] = []
        self.setup_agent()

    def setup_agent(self):
        """Initialize the agent and all necessary components"""
        try:
            # Load environment variables
            load_dotenv()
            
            # Configure CDP SDK
            self.cdp_instance = Cdp.configure_from_json("./secrets/cdp_api_key.json")
            logger.info("CDP SDK configured successfully")
            
            # Initialize the LLM
            self.llm = ChatOpenAI(
                model="gpt-4",
                temperature=0.7,
                api_key=os.getenv("OPENAI_API_KEY")
            )
            logger.info("LLM initialized successfully")
            
            # Initialize tools
            self.wallet_tool = CreateWalletTool(cdp_instance=self.cdp_instance)
            self.balance_tool = GetWalletBalanceTool()
            self.quote_tool = OdosQuoteTool()
            self.execute_tool = OdosExecuteTool()
            
            # Create prompt template with improved swap handling
            self.prompt = ChatPromptTemplate.from_messages([
                ("system", f"""You are a helpful assistant that helps users create and manage cryptocurrency wallets 
                and execute token swaps. Follow these guidelines based on the user's request:

                For swap requests:
                1. When user asks for a swap:
                   - Parse the input amount and tokens carefully
                   - Convert human-readable amounts to proper decimals based on the token
                   - For USDC swaps, use address: {TOKEN_CONFIG['USDC']['address']}
                   - For AERO swaps, use address: {TOKEN_CONFIG['AERO']['address']}
                   - Use chain ID 8453 (Base)
                   - Amount should be converted to proper decimals (ETH: 18, USDC: 6)
                   - Get the quote using the quote_tool
                   - Present the quote clearly showing input and output amounts
                   - Include the quote ID for execution
                
                For balance checks:
                1. Only check balance when:
                   - User explicitly asks for a balance
                   - Verifying funds before executing a confirmed swap

                When converting amounts:
                - ETH and most tokens: multiply by 10^18
                - USDC: multiply by 10^6

                Always be clear about fees and risks. Present information in a clear, readable format."""),
                MessagesPlaceholder(variable_name="messages"),
                ("human", "Handle user requests efficiently while maintaining safety.")
            ])
            
            # Create the agent
            self.agent = create_react_agent(
                self.llm,
                [self.wallet_tool, self.balance_tool, self.quote_tool, self.execute_tool],
                state_modifier=self.prompt
            )
            logger.info("Agent created successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize agent: {str(e)}", exc_info=True)
            raise

    def convert_amount_to_decimals(self, amount: float, token: str) -> int:
        """Convert human readable amount to token decimals"""
        token_upper = token.upper()
        if token_upper not in TOKEN_CONFIG:
            raise ValueError(f"Unsupported token: {token}")
        
        decimals = TOKEN_CONFIG[token_upper]['decimals']
        return int(amount * (10 ** decimals))

    def format_response(self, response: str) -> str:
        """Format the response to be more readable"""
        try:
            # Try to parse as JSON for better formatting
            data = json.loads(response)
            if isinstance(data, dict):
                return "\n".join(f"{k}: {v}" for k, v in data.items())
        except:
            pass
        return response

    def get_agent_response(self, user_input: str) -> str:
        """Get response from agent for user input"""
        try:
            # Add user message to history
            self.conversation_history.append(("user", user_input))
            
            # Create messages list for agent
            messages = [("user" if role == "user" else "assistant", content) 
                       for role, content in self.conversation_history]
            
            # Get agent response
            result = self.agent.invoke({"messages": messages})
            
            # Extract and format agent's response
            agent_response = result["messages"][-1].content
            formatted_response = self.format_response(agent_response)
            self.conversation_history.append(("assistant", formatted_response))
            
            return formatted_response
            
        except Exception as e:
            logger.error(f"Error getting agent response: {str(e)}", exc_info=True)
            return f"An error occurred: {str(e)}"

def main():
    print("\nWelcome to the Crypto Agent Chat!")
    print("Type 'quit' or 'exit' to end the conversation.")
    print("\nAvailable commands:")
    print("- Check balance: 'balance <address>'")
    print("- Get swap quote: 'swap <amount> <from_token> to <to_token>'")
    print("- Execute swap: 'execute <quote_id>'")
    print("\nSupported tokens:")
    for token, details in TOKEN_CONFIG.items():
        print(f"- {token}")
    print("="*50)
    
    # Initialize the chat agent
    chat = AgentChat()
    
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            # Check for exit command
            if user_input.lower() in ['quit', 'exit']:
                print("\nGoodbye!")
                break
                
            # Skip empty input
            if not user_input:
                continue
                
            # Get and print agent response
            response = chat.get_agent_response(user_input)
            print("\nAgent:", response)
            print("\n" + "="*50)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            logger.error(f"Error in main loop: {str(e)}", exc_info=True)
            print(f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    main()