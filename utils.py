import os
import re
import hashlib

def save_prompt_if_unique(prompt_dir, full_prompt):
    """
    Saves the given prompt to the prompt directory as the next numbered file, 
    only if it's not a duplicate of the last saved prompt.

    :param prompt_dir: Directory where the prompts are saved
    :param full_prompt: The full prompt string to save
    """
    # Ensure the directory exists
    os.makedirs(prompt_dir, exist_ok=True)

    # Find the highest numbered prompt file
    highest_num = 0
    for filename in os.listdir(prompt_dir):
        match = re.match(r'prompt(\d+)\.txt', filename)
        if match:
            num = int(match.group(1))
            if num > highest_num:
                highest_num = num

    # Read the content of the highest prompt file, if it exists
    last_prompt_content = ""
    if highest_num > 0:
        with open(os.path.join(prompt_dir, f'prompt{highest_num}.txt'), 'r') as file:
            last_prompt_content = file.read()

    # Check for duplicates and save if unique
    if full_prompt != last_prompt_content:
        new_prompt_num = highest_num + 1
        with open(os.path.join(prompt_dir, f'prompt{new_prompt_num}.txt'), 'w') as file:
            file.write(full_prompt)
        print(f"Prompt saved as 'prompt{new_prompt_num}.txt'")
    else:
        print("Duplicate prompt. Not saved.")

def generate_hash(content):
    """
    Generates a SHA-256 hash of the given content.

    :param content: Content to hash
    :return: SHA-256 hash of the content
    """
    return hashlib.sha256(content.encode()).hexdigest()


def load_prompt_content(filepath):
    """
    Loads the content of a prompt file.

    :param filepath: Path to the prompt file
    :return: Content of the prompt file
    """
    with open(filepath, 'r') as file:
        return file.read()
    
def save_message_history(message_dir, messages):
    """
    Saves the given message history to the message directory as the next numbered file,
    only if it's not a duplicate of the last saved message history.

    :param message_dir: Directory where the message histories are saved
    :param messages: The message history list to save
    """
    # Ensure the directory exists
    os.makedirs(message_dir, exist_ok=True)

    # Convert messages to a string
    messages_str = "\n\n".join(str(msg) for msg in messages)
    current_hash = generate_hash(messages_str)

    # Hash set for checking duplicates
    existing_hashes = set()

    # Populate the hash set with hashes of existing files
    for filename in os.listdir(message_dir):
        if filename.startswith("message_history_") and filename.endswith(".txt"):
            with open(os.path.join(message_dir, filename), 'r') as file:
                file_content = file.read()
                existing_hashes.add(generate_hash(file_content))

    # Check for duplicates using the hash
    if current_hash not in existing_hashes:
        new_message_num = len(existing_hashes) + 1
        with open(os.path.join(message_dir, f'message_history_{new_message_num}.txt'), 'w') as file:
            file.write(messages_str)
        print(f"Message history saved as 'message_history_{new_message_num}.txt'")
    else:
        print("Duplicate message history. Not saved.")