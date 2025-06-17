from functions.data_loader import display_stats_menu, import_all_from_folder
from functions.stats_web_generator import generate_page
from functions.settings import settings
from functions.utils import clear_console, copy_page_to_desktop, clear_data
import colorama
from colorama import Fore, Back, Style
import os

colorama.init()

def print_banner():
    banner = f"""{Fore.GREEN}  __  _____  __  _____   __         __   __  _   __   _    _  ___  ___  ___  
/' _/|_   _|/  \\|_   _|/' _/  __   /  \\ |  \\| | /  \\ | |  | ||_  || __|| _ \\ 
`._`. | | | /\\ | | |  `._`. |__| | /\\ || | ' || /\\ || |_ | | / / | _| | v / 
|___/ |_| |_||_| |_|  |___/      |_||_||_|\\__||_||_||___||_||___||___||_|_\\
{Style.RESET_ALL}"""
    print(banner)

def main_menu():
    stats_folder = 'player_stats/'
    usercache_path = 'user_data/usercache.json'

    while True:
        clear_console()
        print_banner()
        print(f"\n{Fore.CYAN}Select an option:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}1.{Style.RESET_ALL} Show stats")
        print(f"{Fore.YELLOW}2.{Style.RESET_ALL} Import player stats and usercache from single folder")
        print(f"{Fore.YELLOW}3.{Style.RESET_ALL} Generate page with stats")
        print(f"{Fore.YELLOW}4.{Style.RESET_ALL} Copy generated page to desktop")
        print(f"{Fore.YELLOW}5.{Style.RESET_ALL} Page settings")
        print(f"{Fore.YELLOW}6.{Style.RESET_ALL} Clear all data")
        print(f"{Fore.YELLOW}7.{Style.RESET_ALL} Exit")
        
        choice = input(f"\n{Fore.GREEN}Choose an option:{Style.RESET_ALL} ")
        clear_console()

        if choice == '1':
            display_stats_menu(stats_folder, usercache_path)
        elif choice == '2':
            source = input(f"{Fore.CYAN}Enter full path to folder with all .json files (stats + usercache):{Style.RESET_ALL} ").strip()
            import_all_from_folder(source)
        elif choice == '3':
            generate_page()
            print(f"{Fore.GREEN}Page generated successfully!{Style.RESET_ALL}")
        elif choice == '4':
            copy_page_to_desktop()
        elif choice == '5':
            settings()
        elif choice == '6':
            confirm = input(f"{Fore.RED}Are you sure you want to clear all data? (y/n):{Style.RESET_ALL} ").lower()
            if confirm == 'y':
                clear_data()
        elif choice == '7':
            print(f"{Fore.YELLOW}Exiting program. Goodbye!{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Invalid choice. Please enter a number between 1 and 7.{Style.RESET_ALL}\n")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

if __name__ == '__main__':
    main_menu()
