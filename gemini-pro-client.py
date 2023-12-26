# System imports
import argparse
import os
from dotenv import load_dotenv

# Formatting imports
from IPython.display import Markdown
from termcolor import colored

# Google gemini interface imports
import google.generativeai as genai

# Load necessary constants from constants.py
from constants import CODE_BASE, CODE_SYS_MESSAGE, USER_MESSAGE_ONE, \
    ASSISTANT_MESSAGE_ONE, ASSISTANT_MESSAGE_TWO, ASSISTANT_MESSAGE_THREE, PROMPT_DIR

# utils.py imports
from utils import save_prompt_if_unique, load_prompt_content, save_message_history
from message import Message

# Set up argument parser
parser = argparse.ArgumentParser(description='Process flags for model prompt.')

# Argument definitions using 'store_true' for boolean flags
parser.add_argument('--base', action='store_true', help='Use base prompt only (default: True)')
parser.add_argument('--load_prompt', type=str, help='Load prompt from a file. Overrides --base flag.')
parser.add_argument('--chat_mode', action='store_true', help='Enable chat mode (default: False)')
args = parser.parse_args()

load_dotenv()
GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

# Load prompt or get new prompt based on flags
if args.load_prompt:
    prompt_file_path = os.path.join(PROMPT_DIR, args.load_prompt)
    if not os.path.exists(prompt_file_path):
        print(f"Prompt file '{args.load_prompt}' not found in directory '{PROMPT_DIR}'. Exiting program.")
        exit(1)
    full_prompt = load_prompt_content(prompt_file_path)
else:
    base_flag = args.base == 'True'
    chat_mode = args.chat_mode == 'True'
    prompt_to_model = input("Enter a prompt for text-completion: ")

    context_messages = [
        Message('SYSTEM', CODE_SYS_MESSAGE),
        Message('USER', USER_MESSAGE_ONE),
        Message('EXPERT_1', ASSISTANT_MESSAGE_ONE),
        Message('EXPERT_2', ASSISTANT_MESSAGE_TWO),
        Message('EXPERT_3', ASSISTANT_MESSAGE_THREE),
        Message('USER', CODE_BASE),
        Message('USER', prompt_to_model)
    ] if not base_flag else [Message('USER', prompt_to_model)]
    
    full_prompt = "\n\n".join(str(message) for message in context_messages)
    save_prompt_if_unique(PROMPT_DIR, full_prompt)

# Initialize relevant loop vars
last_expert = 3
message_history = []

# Function to perform a single generation
def generate_response(prompt):
    print(colored('Prompt to model: ' + prompt, 'magenta'))
    response = model.generate_content(prompt)
    markdown_formatted_obj = Markdown(response.text)
    model_output = markdown_formatted_obj.data
    print(colored("Model output: " + "\n\n" + model_output, 'green'))
    return model_output

# Begin message history with user prompt
message_history.append(Message('USER', full_prompt))

# Single generation if chat mode is not enabled
if not args.chat_mode:
    model_output = generate_response(full_prompt)
    message_history.append(Message('EXPERT_1', model_output))  # Assuming default expert
    save_message_history(os.path.join("message_histories", "message_history_N.txt"), message_history)
    exit(0)

# Chat mode loop
while args.chat_mode:
    model_output = generate_response(full_prompt)

    # Append model response to the conversation and history
    expert_label = f"EXPERT_{(last_expert % 3) + 1}"
    last_expert += 1
    full_prompt += "\n\n" + str(Message(expert_label, model_output))
    message_history.append(Message(expert_label, model_output))

    # Get new user input
    user_input = input("Enter your response (or type 'exit' to quit): ")
    if user_input.lower() in ['exit', 'quit']:
        save_message_history(os.path.join("message_histories", "message_history_N.txt"), message_history)
        break
    full_prompt += "\n\n" + str(Message('USER', user_input))
    message_history.append(Message('USER', user_input))