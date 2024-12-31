# chat-bridge

This bot serves as a bridge between Discord and Minecraft, allowing users to interact with the Minecraft server through Discord and vice versa. 
It utilizes the [discord.py](https://github.com/Rapptz/discord.py) library for Discord integration and [Mineflayer](https://github.com/PrismarineJS/mineflayer) for Minecraft integration.

## Prerequisites

Before running the bot, ensure you have the following installed:

- Git
- [Python 3.10+](https://www.python.org/downloads/)
- Minecraft account
- Discord Bot (Token)

## Installation

1. **Clone this repository and enter directory:**

   ```bash
   $ git clone git@github.com:yashpatolia/chat-bridge.git
   $ cd chat-bridge
   ```

2. **Rename `example.py` to `config.py`**
   
   ```bash
   $ cp example.py config.py
   ```

3. **Install required packages**

   ```bash
   $ pip install -r requirements.txt
   ```

4. **Edit `config.py` file**

   Once you have edited the config file with your settings, you can start the app
   ```bash
   $ python3 main.py
   ```

## License
Chat Bridge is open-sourced software licensed under the [MIT License](https://opensource.org/license/mit/).
   
