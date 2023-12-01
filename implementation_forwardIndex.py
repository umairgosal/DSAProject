import json
import os
from class_forwardIndex import ForwardIndex
from utils.utils import process_content_generator, generate_unique_doc_id

def load_config(config_path='config.json'):
    # Load configuration from a JSON file or use default configuration if the file is not found
    if os.path.exists(config_path):
        with open(config_path, 'r') as config_file:
            return json.load(config_file)
    else:
        print(f"Config file {config_path} not found. Using default configuration.")
        return {}

def build_forward_index(folder_path, forward_index):
    # Build the forward index by processing JSON files in the specified folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.endswith('.json'):
            extract_content_and_id_from_json(file_path, forward_index)

def extract_content_and_id_from_json(file_path, forward_index):
    # Extract content and document ID from a JSON file and add the document to the forward index
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list):
                for obj_index, obj in enumerate(data):
                    content_item = obj.get('content', '')
                    if content_item:
                        # Generate a unique document ID based on the file name and object index
                        file_name = os.path.splitext(os.path.basename(file_path))[0]
                        article_id = generate_unique_doc_id(file_name, obj_index)
                        
                        # Process the content and add the document to the forward index
                        tokens = process_content_generator(content_item)
                        forward_index.add_document(article_id, tokens)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file {file_path}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred in file {file_path}: {e}")
