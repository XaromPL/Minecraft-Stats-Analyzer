import json
import os
import shutil

def load_stats(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get("stats", {}).get("minecraft:mined", {})
    except Exception as e:
        print(f"Error loading stats from {file_path}: {e}")
        return {}

def load_usercache(usercache_path):
    try:
        with open(usercache_path, 'r', encoding='utf-8') as f:
            usercache = json.load(f)
        return {entry['uuid']: entry['name'] for entry in usercache}
    except Exception as e:
        print(f"Error loading usercache: {e}")
        return {}

def display_player_stats(stats_folder, usercache_path):
    uuid_to_name = load_usercache(usercache_path)
    if not uuid_to_name:
        print("No valid usercache found.")
        return

    player_stats = {}

    for filename in os.listdir(stats_folder):
        if filename.endswith(".json"):
            uuid = filename.replace(".json", "")
            path = os.path.join(stats_folder, filename)
            mined = load_stats(path)
            total_blocks = sum(mined.values())
            player_name = uuid_to_name.get(uuid, f"Unknown ({uuid})")
            player_stats[player_name] = player_stats.get(player_name, 0) + total_blocks

    if not player_stats:
        print("No block mining data found in any file.")
        return

    total_all_players = 0
    print("\nBlocks mined per player:")
    for player_name, total in player_stats.items():
        print(f" - {player_name}: {total}")
        total_all_players += total

    print(f"\nTotal blocks mined by all players: {total_all_players}\n")

def import_all_from_folder(source_folder):
    if not os.path.exists(source_folder):
        print("Error: Source folder does not exist.")
        return

    if not os.path.exists("player_stats"):
        os.makedirs("player_stats")
    if not os.path.exists("user_data"):
        os.makedirs("user_data")

    usercache_found = False
    files_copied = 0

    for file in os.listdir(source_folder):
        full_path = os.path.join(source_folder, file)
        if os.path.isfile(full_path) and file.endswith(".json"):
            if file.lower() == "usercache.json":
                try:
                    shutil.copy2(full_path, os.path.join("user_data", "usercache.json"))
                    usercache_found = True
                    print(f"Copied usercache.json")
                except Exception as e:
                    print(f"Failed to copy usercache.json: {e}")
            else:
                try:
                    shutil.copy2(full_path, os.path.join("player_stats", file))
                    files_copied += 1
                except Exception as e:
                    print(f"Failed to copy {file}: {e}")

    print(f"Copied {files_copied} player stats files.")
    if not usercache_found:
        print("Warning: usercache.json not found in the source folder!")

def main_menu():
    stats_folder = "player_stats/"
    usercache_path = "user_data/usercache.json"

    while True:
        print("=== Minecraft Stats Analyzer ===")
        print("1. Show mining stats")
        print("2. Import player stats and usercache from single folder")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            display_player_stats(stats_folder, usercache_path)
        elif choice == "2":
            source = input("Enter full path to folder with all .json files (stats + usercache): ").strip('"')
            import_all_from_folder(source)
        elif choice == "3":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.\n")

if __name__ == "__main__":
    main_menu()
