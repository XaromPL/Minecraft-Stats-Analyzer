import os
import shutil
import json
from colorama import Fore, Style

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def copy_page_to_desktop():
    try:
        desktop = os.path.expanduser("~/Desktop")
        source_folder = 'generated_page'
        
        if not os.path.exists(source_folder):
            print(f"{Fore.RED}Error: Generated page not found!{Style.RESET_ALL}")
            return
            
        desktop_folder = os.path.join(desktop, 'Minecraft-Stats')
        os.makedirs(desktop_folder, exist_ok=True)
        
        for file in os.listdir(source_folder):
            source = os.path.join(source_folder, file)
            destination = os.path.join(desktop_folder, file)
            shutil.copy2(source, destination)
            
        print(f"{Fore.GREEN}Successfully copied page to: {desktop_folder}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error copying page: {e}{Style.RESET_ALL}")

def clear_data():
    try:
        for folder in ['player_stats', 'user_data', 'generated_page']:
            if os.path.exists(folder):
                shutil.rmtree(folder)
                os.makedirs(folder)
        print(f"{Fore.GREEN}All data has been cleared successfully!{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error while clearing data: {e}{Style.RESET_ALL}")

def ensure_directories_exist():
    directories = ['player_stats', 'user_data', 'generated_page', 'lang']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def load_json_file(file_path, default=None):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"{Fore.RED}Error loading {file_path}: {e}{Style.RESET_ALL}")
        return default if default is not None else {}