from functions.settings import load_settings, load_language
import os
from functions.data_loader import load_full_stats, load_usercache
from collections import defaultdict
from operator import itemgetter

def get_top_players(stats_data, top_count):
    sorted_stats = sorted(stats_data.items(), key=itemgetter(1), reverse=True)
    return sorted_stats[:top_count]

def generate_stats_section(title, stats_data, top_count, translations):
    if not stats_data:
        return ""
        
    top_players = get_top_players(stats_data, top_count)
    
    html = f"""
    <div class="stats-section">
        <h2>{title}</h2>
        <div class="top-players">
            <table>
                <tr>
                    <th>{translations['table_headers']['place']}</th>
                    <th>{translations['table_headers']['player']}</th>
                    <th>{translations['table_headers']['score']}</th>
                </tr>
    """
    
    for i, (player, value) in enumerate(top_players, 1):
        html += f"""
                <tr>
                    <td>#{i}</td>
                    <td>{player}</td>
                    <td>{value:,}</td>
                </tr>
        """
    
    html += """
            </table>
        </div>
    </div>
    """
    return html

def collect_stats_for_category(stats, player_name, category):
    result = defaultdict(int)
    for item, count in stats.get(f'minecraft:{category}', {}).items():
        result[player_name] += count
    return result

def generate_page(folder='generated_page'):
    settings = load_settings()
    translations = load_language(settings.get('language', 'en'))
    server_name = settings.get('server_name', 'Minecraft Server')
    output_file = settings.get('report_name', 'stats.html')
    top_count = settings.get('top_players_count', 5)
    dark_mode = settings.get('dark_mode', True)
    show_stats = settings.get('show_stats', {})
    
    if dark_mode:
        colors = {
            'primary': '#0D1117',
            'secondary': '#161B22',
            'text': '#E6EDF3',
            'accent': '#58A6FF',
            'hover': 'rgba(255, 255, 255, 0.07)',
            'border': 'rgba(255, 255, 255, 0.12)'
        }
    else:
        colors = {
            'primary': '#FAFAFA',
            'secondary': '#E9ECEF',
            'text': '#212529',
            'accent': '#1D72B8',
            'hover': 'rgba(0, 0, 0, 0.03)',
            'border': 'rgba(0, 0, 0, 0.08)'
        }

    stats_folder = 'player_stats/'
    usercache_path = 'user_data/usercache.json'
    uuid_to_name = load_usercache(usercache_path)
    
    categories = {
        'mined': defaultdict(int),
        'broken': defaultdict(int),
        'crafted': defaultdict(int),
        'killed': defaultdict(int),
        'killed_by': defaultdict(int),
        'dropped': defaultdict(int),
        'picked_up': defaultdict(int),
        'used': defaultdict(int),
        'custom': defaultdict(int)
    }
    
    for stats_file in os.listdir(stats_folder):
        if stats_file.endswith('.json'):
            uuid = stats_file.replace('.json', '')
            path = os.path.join(stats_folder, stats_file)
            stats = load_full_stats(path)
            player_name = uuid_to_name.get(uuid, f'Unknown ({uuid})')
            
            for category in categories.keys():
                category_stats = collect_stats_for_category(stats, player_name, category)
                for player, count in category_stats.items():
                    categories[category][player] += count

    content = f"""
<!DOCTYPE html>
<html lang="{settings.get('language', 'en')}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{server_name} - {translations['page_title']}</title>
    <style>
        :root {{
            --primary-color: {colors['primary']};
            --secondary-color: {colors['secondary']};
            --text-color: {colors['text']};
            --accent-color: {colors['accent']};
            --hover-color: {colors['hover']};
            --border-color: {colors['border']};
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: var(--primary-color);
            color: var(--text-color);
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }}

        h1 {{
            text-align: center;
            color: var(--accent-color);
            margin-bottom: 40px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            grid-column: 1 / -1;
        }}

        .stats-section {{
            background-color: var(--secondary-color);
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        .stats-section h2 {{
            color: var(--accent-color);
            border-bottom: 2px solid var(--accent-color);
            padding-bottom: 10px;
            margin-top: 0;
            font-size: 1.5em;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
            font-size: 0.9em;
        }}

        th, td {{
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }}

        th {{
            background-color: rgba(0,0,0,0.2);
            color: var(--accent-color);
        }}

        tr:hover {{
            background-color: var(--hover-color);
        }}

        .top-players {{
            margin-top: 20px;
        }}

        @media (max-width: 600px) {{
            .container {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{server_name} - {translations['page_title']}</h1>
        
        {generate_stats_section(translations['stats_categories']['mined'], categories['mined'], top_count, translations) if show_stats.get('mined', True) else ''}
        {generate_stats_section(translations['stats_categories']['broken'], categories['broken'], top_count, translations) if show_stats.get('broken', True) else ''}
        {generate_stats_section(translations['stats_categories']['crafted'], categories['crafted'], top_count, translations) if show_stats.get('crafted', True) else ''}
        {generate_stats_section(translations['stats_categories']['killed'], categories['killed'], top_count, translations) if show_stats.get('killed', True) else ''}
        {generate_stats_section(translations['stats_categories']['killed_by'], categories['killed_by'], top_count, translations) if show_stats.get('killed_by', True) else ''}
        {generate_stats_section(translations['stats_categories']['dropped'], categories['dropped'], top_count, translations) if show_stats.get('dropped', True) else ''}
        {generate_stats_section(translations['stats_categories']['picked_up'], categories['picked_up'], top_count, translations) if show_stats.get('picked_up', True) else ''}
        {generate_stats_section(translations['stats_categories']['used'], categories['used'], top_count, translations) if show_stats.get('used', True) else ''}
        {generate_stats_section(translations['stats_categories']['custom'], categories['custom'], top_count, translations) if show_stats.get('custom', True) else ''}
    </div>
</body>
</html>
    """

    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, output_file)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Utworzono plik {filepath}")
