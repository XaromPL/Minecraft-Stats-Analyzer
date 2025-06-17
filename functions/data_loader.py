import json
import os
import shutil
from colorama import Fore, Style
from functions.utils import clear_console, load_json_file

def load_full_stats(file_path):
    return load_json_file(file_path, {}).get('stats', {})

def load_mined_blocks(file_path):
    stats = load_full_stats(file_path)
    return stats.get('minecraft:mined', {})

def load_killed_mobs(file_path):
    stats = load_full_stats(file_path)
    return stats.get('minecraft:killed', {})

def load_advancements(file_path):
    stats = load_full_stats(file_path)
    return stats.get('minecraft:custom', {})

def load_usercache(usercache_path):
    try:
        with open(usercache_path, 'r', encoding='utf-8') as f:
            usercache = json.load(f)
        return {entry['uuid']: entry['name'] for entry in usercache}
    except Exception as e:
        print(f"{Fore.RED}Error loading usercache: {e}{Style.RESET_ALL}")
        return {}

def display_stats_menu(stats_folder, usercache_path):
    while True:
        clear_console()
        print(f"{Fore.CYAN}Select stats to display:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}1.{Style.RESET_ALL} Show mined blocks stats")
        print(f"{Fore.YELLOW}2.{Style.RESET_ALL} Show killed mobs stats")
        print(f"{Fore.YELLOW}3.{Style.RESET_ALL} Show advancements")
        print(f"{Fore.YELLOW}4.{Style.RESET_ALL} Show crafted items stats")
        print(f"{Fore.YELLOW}5.{Style.RESET_ALL} Show used items stats")
        print(f"{Fore.YELLOW}6.{Style.RESET_ALL} Back to main menu")

        choice = input(f"\n{Fore.GREEN}Choose an option:{Style.RESET_ALL} ")
        clear_console()

        if choice == '1':
            display_mined_blocks(stats_folder, usercache_path)
        elif choice == '2':
            display_killed_mobs(stats_folder, usercache_path)
        elif choice == '3':
            display_advancements(stats_folder, usercache_path)
        elif choice == '4':
            display_crafted_items(stats_folder, usercache_path)
        elif choice == '5':
            display_used_items(stats_folder, usercache_path)
        elif choice == '6':
            break
        else:
            print(f"{Fore.RED}Invalid choice. Please enter a number between 1 and 6.{Style.RESET_ALL}")

        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

def display_mined_blocks(stats_folder, usercache_path):
    uuid_to_name = load_usercache(usercache_path)
    print(f"{Fore.CYAN}Mined blocks stats:{Style.RESET_ALL}\n")
    
    for filename in os.listdir(stats_folder):
        if filename.endswith('.json'):
            uuid = filename.replace('.json', '')
            path = os.path.join(stats_folder, filename)
            stats = load_full_stats(path)
            player_name = uuid_to_name.get(uuid, f'Unknown ({uuid})')
            
            if 'minecraft:mined' in stats:
                print(f"\n{Fore.YELLOW}{player_name}:{Style.RESET_ALL}")
                for item, count in stats['minecraft:mined'].items():
                    print(f"  {item}: {count}")

def display_crafted_items(stats_folder, usercache_path):
    uuid_to_name = load_usercache(usercache_path)
    print(f"{Fore.CYAN}Crafted items stats:{Style.RESET_ALL}\n")
    
    for filename in os.listdir(stats_folder):
        if filename.endswith('.json'):
            uuid = filename.replace('.json', '')
            path = os.path.join(stats_folder, filename)
            stats = load_full_stats(path)
            player_name = uuid_to_name.get(uuid, f'Unknown ({uuid})')
            
            if 'minecraft:crafted' in stats:
                print(f"\n{Fore.YELLOW}{player_name}:{Style.RESET_ALL}")
                for item, count in stats['minecraft:crafted'].items():
                    print(f"  {item}: {count}")

def display_used_items(stats_folder, usercache_path):
    uuid_to_name = load_usercache(usercache_path)
    print(f"{Fore.CYAN}Used items stats:{Style.RESET_ALL}\n")
    
    for filename in os.listdir(stats_folder):
        if filename.endswith('.json'):
            uuid = filename.replace('.json', '')
            path = os.path.join(stats_folder, filename)
            stats = load_full_stats(path)
            player_name = uuid_to_name.get(uuid, f'Unknown ({uuid})')
            
            if 'minecraft:used' in stats:
                print(f"\n{Fore.YELLOW}{player_name}:{Style.RESET_ALL}")
                for item, count in stats['minecraft:used'].items():
                    print(f"  {item}: {count}")

def display_killed_mobs(stats_folder, usercache_path):
    uuid_to_name = load_usercache(usercache_path)
    print(f"{Fore.CYAN}Killed mobs stats:{Style.RESET_ALL}\n")
    
    for filename in os.listdir(stats_folder):
        if filename.endswith('.json'):
            uuid = filename.replace('.json', '')
            path = os.path.join(stats_folder, filename)
            stats = load_full_stats(path)
            player_name = uuid_to_name.get(uuid, f'Unknown ({uuid})')
            
            if 'minecraft:killed' in stats:
                print(f"\n{Fore.YELLOW}{player_name}:{Style.RESET_ALL}")
                for mob, count in stats['minecraft:killed'].items():
                    print(f"  {mob}: {count}")

def display_advancements(stats_folder, usercache_path):
    uuid_to_name = load_usercache(usercache_path)
    print(f"{Fore.CYAN}Advancements stats:{Style.RESET_ALL}\n")
    
    for filename in os.listdir(stats_folder):
        if filename.endswith('.json'):
            uuid = filename.replace('.json', '')
            path = os.path.join(stats_folder, filename)
            stats = load_full_stats(path)
            player_name = uuid_to_name.get(uuid, f'Unknown ({uuid})')
            
            if 'minecraft:custom' in stats:
                print(f"\n{Fore.YELLOW}{player_name}:{Style.RESET_ALL}")
                for advancement, count in stats['minecraft:custom'].items():
                    print(f"  {advancement}: {count}")

def import_all_from_folder(source_folder):
    if not os.path.exists(source_folder):
        print(f"{Fore.RED}Error: Source folder does not exist.{Style.RESET_ALL}")
        return

    if not os.path.exists('player_stats'):
        os.makedirs('player_stats')
    if not os.path.exists('user_data'):
        os.makedirs('user_data')

    usercache_found = False
    files_copied = 0

    for file in os.listdir(source_folder):
        full_path = os.path.join(source_folder, file)
        if os.path.isfile(full_path) and file.endswith('.json'):
            if file.lower() == 'usercache.json':
                try:
                    shutil.copy2(full_path, os.path.join('user_data', 'usercache.json'))
                    usercache_found = True
                    print(f"{Fore.GREEN}Copied usercache.json{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}Failed to copy usercache.json: {e}{Style.RESET_ALL}")
            else:
                try:
                    shutil.copy2(full_path, os.path.join('player_stats', file))
                    files_copied += 1
                except Exception as e:
                    print(f"{Fore.RED}Failed to copy {file}: {e}{Style.RESET_ALL}")

    print(f"{Fore.GREEN}Copied {files_copied} player stats files.{Style.RESET_ALL}")
    if not usercache_found:
        print(f"{Fore.YELLOW}Warning: usercache.json not found in the source folder!{Style.RESET_ALL}")
