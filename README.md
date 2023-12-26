
# Gemini Pro Client
## Overview

NOTE: THIS PROGRAM DOES NOT INCLUDE SUBSTANTIAL BASE PROMPTS. PLEASE DESIGN YOUR OWN FOR BEST RESULTS.

What is included is a Django-based code replicator and a chat interface: the rest must be dealt with by writing hand-crafted, or writing machine-crafted prompts, and saving them to the prompts directory.

The Gemini Pro Client is a Python script designed to interact with the Google Gemini AI model. It offers capabilities for generating text completions based on various input prompts. The script can operate in different modes, allowing users to either provide a single prompt for one-time text generation or engage in an interactive chat-like session where the model builds upon the ongoing conversation.

## Features

- **Single Prompt Generation**: Generate a text completion based on a single user-provided prompt.
**Interactive Chat Mode**: Engage in an interactive session where each new input from the user is considered in the context of the ongoing conversation.
**Load Existing Prompts**: Option to load and use prompts from a file.
- **Save Message Histories**: Automatically save the conversation history in an efficient and non-redundant manner.

## Installation

Before running the script, ensure you have Python installed and the required dependencies. Install the dependencies using:

```bash
pip install -r requirements.txt
```

## Usage

Run the script from the command line with optional flags to control its behavior:

```bash
python gemini-pro-client.py [options]
```

### Options

- `--base`: Use the base prompt only. If set, the script will use a minimal prompt for text generation. Default is False (i.e., extended context is used).
`--load_prompt <filename>`: Load a prompt from the specified file. This overrides the `--base` flag. Provide the filename of the prompt to be loaded from the `PROMPT_DIR` directory.
- `--chat_mode`: Enable interactive chat mode. In this mode, the script will continue to prompt for user input and provide model-generated responses, building a conversation history. The conversation will be saved upon exiting. Default is False.

## Example Commands

- Generate text with a user-provided prompt and extended context:
```bash
    python gemini-pro-client.py
```

- Generate text with a user-provided prompt only:
```bash
    python gemini-pro-client.py --base
```

- Load a prompt from a file and generate text:
```bash
    python gemini-pro-client.py --load_prompt example_prompt.txt
```

- Engage in interactive chat mode:
```bash
python gemini-pro-client.py --chat_mode
```

## Exiting Chat Mode

To exit chat mode, type `exit` or `quit` when prompted for user input. The script will save the conversation history and terminate.
