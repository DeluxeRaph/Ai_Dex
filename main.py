# main.py
from dotenv import load_dotenv
import os
from cdp import *
from langchain_openai import ChatOpenAI
from tools.create_wallet import CreateWalletTool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.prebuilt import create_react_agent
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        # Load environment variables
        load_dotenv()
        
        # Configure CDP SDK
        cdp_instance = Cdp.configure_from_json("./secrets/cdp_api_key.json")

        logger.info("CDP SDK configured successfully")
        
        # Initialize the LLM
        llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        logger.info("LLM initialized successfully")
        
        # Initialize the CreateWalletTool
        wallet_tool = CreateWalletTool(cdp_instance=cdp_instance)
        
        # Create a system prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant that helps users create and manage cryptocurrency wallets."),
            MessagesPlaceholder(variable_name="messages"),
            ("human", "Remember to be careful and clear when working with wallet operations.")
        ])
        
        # Create the agent
        agent = create_react_agent(
            llm,
            [wallet_tool],
            state_modifier=prompt
        )
        logger.info("Agent created successfully")
        
        # Test wallet creation
        logger.info("\nTesting wallet creation...")
        
        result = agent.invoke({
            "messages": [
                ("user", "Create a new wallet for me")
            ]
        })
        
        logger.info("\nResult:")
        logger.info(result)
        
    except Exception as e:
        logger.error(f"\nAn error occurred: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main()