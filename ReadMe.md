# AI Dex

AI Dex is an intelligent, multi-model agent designed for the QuickNode Hackathon. It provides users with the ability to create, manage, and swap cryptocurrency assets directly through an interactive chatbot interface powered by advanced language models. The project leverages the power of the Coinbase SDK and the Odos DEX aggregator to enable seamless wallet interactions and token swaps.

## Table of Contents
- [AI Dex](#ai-dex)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Setup Instructions](#setup-instructions)
  - [Tech Stack](#tech-stack)
  - [Basic Functionality](#basic-functionality)
    - [Wallet Creation](#wallet-creation)
    - [Wallet Interaction](#wallet-interaction)
  - [Swapping Mechanism](#swapping-mechanism)
  - [Workflow](#workflow)
  - [Next Steps](#next-steps)
  - [Example Chat Log](#example-chat-log)

## Installation

### Prerequisites
Ensure you have Python 3 installed. If not, download and install it from [python.org](https://www.python.org/).

### Setup Instructions
1. Install `virtualenv` if you haven't already:
    ```bash
    pip3 install virtualenv
    ```

2. Create a virtual environment:
    ```bash
    python3 -m venv venv
    ```

3. Activate the virtual environment:
    - **On Unix or MacOS**:
        ```bash
        source venv/bin/activate
        ```
    - **On Windows**:
        ```bash
        venv\Scripts\activate
        ```

4. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

   **Note**: If you don't have a `requirements.txt` file, you can install the packages individually:
    ```bash
    pip install cdp-sdk langchain langchain-openai python-dotenv openai
    ```

5. Run the project:
    ```bash
    python main.py
    ```

## Tech Stack
- **LangChain**: Used for building advanced conversational AI.
- **Coinbase SDK**: Provides wallet functionalities and enables ERC-20 token interactions.
- **Odos DEX Aggregator**: Used for fetching token swap quotes and executing swaps.

## Basic Functionality

### Wallet Creation
- The chatbot interacts with users to create an AI-powered wallet using the Coinbase SDK.
- The wallet can receive ERC-20 tokens, and users can check their balance at any time.

### Wallet Interaction
- Users can inquire about the tokens held within their wallet via the chatbot.

## Swapping Mechanism
1. The user initiates a swap by specifying the asset they want to swap (asset A) for another asset (asset B).
2. The bot checks the user's wallet balance to ensure there are sufficient funds for the swap.
3. The bot calls the Odos DEX aggregator's API to get a quote for the swap.
4. The bot presents the swap quote to the user in the chat.
5. The user confirms or declines the quote.
6. If approved, the bot executes the swap using the Odos API.
7. The bot returns the swap metadata to the user once the transaction is complete.

## Workflow
1. The user begins by chatting with the bot.
2. The bot guides the user through wallet creation and funding.
3. The user can check their wallet balance and request a token swap.
4. The bot verifies funds, fetches a swap quote from Odos, and presents it.
5. The user approves or denies the swap.
6. Successful swaps return complete metadata to the user for confirmation.

## Next Steps
- Integrate a frontend to facilitate real-time chat interactions.
- Enhance the user experience by adding swap history tracking and notifications.

## Example Chat Log
```sql
- Bot: "Howdy, do you want to create a wallet?"
- User: "Yes"
- Bot: (Calls `create_wallet` and returns the wallet address)
- Bot: "Do you want to fund the wallet?"
- User: "Yes {sends USDC}"
- User: "Check Balance"
- Bot: "Nice, your wallet is funded."
- Bot: "Would you like to make a swap?"
- User: "Yes, swap my USDC for Base/Ether."
- Bot: "Great, I'm on it."
- Bot: (Makes an API call to Odos to get a quote for a USDC to Base Ether swap)
- Bot: "Here's your swap quote: {quote}. Do you want to perform this swap?"
- User: "Yes"
- Bot: (Makes an API call to Odos to execute the swap)
- Bot: (Returns swap metadata)
