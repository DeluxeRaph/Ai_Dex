# Install virtualenv if you haven't already
pip3 install virtualenv

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the requirements
pip install cdp-sdk

# Now you can run using either python or python3
python cdp.py

# Depend
pip install langchain langchain-openai python-dotenv openai
pip install python-dotenv


# Ai Swapper

# Workflow
Ai Swapper is a multiple model agent that allows users to swap directly with a chat bot

# tech stack
langchain
Coinbase sdk

## Basic function

1. Ai swapper uses coinbase sdk to allows a user to interact with a  chat bot to create an ai power wallet 
2. The wallet has the ability to receive ERC-20 tokens
3. The user can the ask the chat bot the tokens in the current wallet 

## Swapping Mechinism

1. User with a fund wallet tells the chat bot it wants to swap asset ```a``` for ```b```
2. The bot checks the balance of the user to make sure they can swap the ```a``` token for n amount
3. The Chat bot has a swapping agaent that calls the Odos dex aggratoer and ask for ta quote for the proposed assets
4. The bot returns the quote in the chat
5. user choices yes or no to the quote
6. When Quote is approved the bot calls swap api on Odos
7. once swap is complete the bot returns the swap metadata


# Next set

Try to get a basic chat going in the frontend

## chat log
- Bot: "Howdy do you want to create a wallet"
- User: "Yes"
- Bot: "Calls create_wallet and returns address"
- Bot: "Do you wan to fund the wallet?"
- User: "Yes {sends USDC}"
- User: "Check Balance"
- Bot: "Nice, Your wallet is funded"
- Bot: "Would you like to make a swap?"
- User: "Yes swap my USDC for Base/Ether"
- Bot: "Great, I'm on it"
- Bot: Makes api call to Odos to get a qoute for a USDC Base Ether swap
- Bot: "Here's you swap qoute {quote}. Do you want to perform this swap?"
- User: "yes"
- Bot: Makes api call to Odos to swap the asset
- Bot: Returns swap metadata