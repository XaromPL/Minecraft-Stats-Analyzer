import json
import os
from colorama import Fore, Style

def load_language(lang_code):
    try:
        with open(f'lang/{lang_code}.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        print(f"{Fore.RED}Warning: Language file for {lang_code} not found, using English{Style.RESET_ALL}")
        with open('lang/en.json', 'r', encoding='utf-8') as f:
            return json.load(f)

def get_available_languages():
    languages = []
    for file in os.listdir('lang'):
        if file.endswith('.json'):
            languages.append(file[:-5])
    return languages

def settings(file="settings.json"):
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            config = json.load(f)
    else:
        config = {
            "report_name": "stats.html",
            "server_name": "Minecraft Server",
            "top_players_count": 5,
            "dark_mode": True,
            "language": "en",
            "show_stats": {
                "mined": True,
                "broken": True,
                "crafted": True,
                "killed": True,
                "killed_by": True,
                "dropped": True,
                "picked_up": True,
                "used": True,
                "custom": True
            }
        }
        with open(file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
        print(f"{Fore.GREEN}Created default settings file: {file}{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}Current settings:{Style.RESET_ALL}")
    for key, val in config.items():
        if key != "show_stats":
            print(f" {Fore.YELLOW}-{Style.RESET_ALL} {key}: {val}")
    print(f" {Fore.YELLOW}-{Style.RESET_ALL} show_stats:")
    for stat, enabled in config["show_stats"].items():
        print(f"   {Fore.YELLOW}*{Style.RESET_ALL} {stat}: {enabled}")

    change = input(f"\n{Fore.GREEN}Do you want to change any setting? (y/n):{Style.RESET_ALL} ").lower()
    if change == 'y':
        print(f"\n{Fore.CYAN}Available settings:{Style.RESET_ALL}")
        settings_list = ["report_name", "server_name", "top_players_count", "dark_mode", "language", "show_stats"]
        
        for i, setting in enumerate(settings_list, 1):
            print(f"{Fore.YELLOW}{i}.{Style.RESET_ALL} {setting}")
        
        try:
            choice = int(input(f"\n{Fore.GREEN}Enter setting number to change (1-6):{Style.RESET_ALL} "))
            if 1 <= choice <= len(settings_list):
                setting_name = settings_list[choice-1]
                
                if setting_name == "language":
                    print(f"\n{Fore.CYAN}Available languages:{Style.RESET_ALL}")
                    languages = get_available_languages()
                    for i, lang in enumerate(languages, 1):
                        print(f"{Fore.YELLOW}{i}.{Style.RESET_ALL} {lang}")
                    lang_choice = int(input(f"\n{Fore.GREEN}Choose language number:{Style.RESET_ALL} "))
                    if 1 <= lang_choice <= len(languages):
                        config["language"] = languages[lang_choice-1]
                        print(f"{Fore.GREEN}Language set to: {config['language']}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Invalid choice, keeping current language{Style.RESET_ALL}")
                
                elif setting_name == "show_stats":
                    stat_to_change = input(f"{Fore.GREEN}Enter stat name to toggle (e.g. mined, killed):{Style.RESET_ALL} ")
                    if stat_to_change in config["show_stats"]:
                        config["show_stats"][stat_to_change] = not config["show_stats"][stat_to_change]
                        print(f"{Fore.GREEN}Toggled {stat_to_change} to: {config['show_stats'][stat_to_change]}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Invalid stat name{Style.RESET_ALL}")
                
                else:
                    new_value = input(f"{Fore.GREEN}Enter new value for '{setting_name}':{Style.RESET_ALL} ")
                    orig_type = type(config[setting_name])
                    
                    if orig_type == bool:
                        new_value = new_value.lower() in ("yes", "true", "1", "y")
                    else:
                        try:
                            new_value = orig_type(new_value)
                        except Exception:
                            print(f"{Fore.RED}Failed to convert value type, keeping it as string{Style.RESET_ALL}")

                    config[setting_name] = new_value
                    print(f"{Fore.GREEN}Setting updated successfully{Style.RESET_ALL}")

                with open(file, "w", encoding="utf-8") as f:
                    json.dump(config, f, indent=4)
            else:
                print(f"{Fore.RED}Invalid choice{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number{Style.RESET_ALL}")

    return config

def load_settings(file="settings.json"):
    with open(file, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config