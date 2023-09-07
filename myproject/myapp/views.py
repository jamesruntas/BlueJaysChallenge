from django.shortcuts import render
import xml.etree.ElementTree as ET
from .models import GameData
import requests
import statsapi
import json
import os
from datetime import datetime
from datetime import timedelta


import feedparser

def index(request):
    # Fetching news entries
    news_entries = fetch_mlb_news()
    # Fetching MLB standings
    standings_data = fetch_mlb_standing()

    
    current_directory = os.path.dirname(os.path.abspath(__file__))
    team_logos_path = os.path.join(current_directory, 'static', 'teamLogos.json')
    team_ids_path = os.path.join(current_directory, 'static', 'team_ids.json')

    with open(team_logos_path, 'r') as file:
        TEAM_LOGO_URLS = json.load(file)

    with open(team_ids_path, 'r') as file:
        TEAM_IDS_DATA = json.load(file)

    for division in standings_data.values():
        for team in division['teams']:
            team['logo_url'] = TEAM_LOGO_URLS.get(team['name'], '')
            team['abbreviation'] = TEAM_IDS_DATA.get(str(team['team_id']), {}).get('abbreviation', '')



    context = {
        'news_entries': news_entries,
        'standings_data': standings_data,
    }

  
    return render(request, 'index.html', context)


def sidebar(request):
    # Fetching MLB standings
    standings_data = fetch_mlb_standing()

    
    current_directory = os.path.dirname(os.path.abspath(__file__))
    team_logos_path = os.path.join(current_directory, 'static', 'teamLogos.json')
    team_ids_path = os.path.join(current_directory, 'static', 'team_ids.json')

    with open(team_logos_path, 'r') as file:
        TEAM_LOGO_URLS = json.load(file)

    with open(team_ids_path, 'r') as file:
        TEAM_IDS_DATA = json.load(file)

    for division in standings_data.values():
        for team in division['teams']:
            team['logo_url'] = TEAM_LOGO_URLS.get(team['name'], '')
            team['abbreviation'] = TEAM_IDS_DATA.get(str(team['team_id']), {}).get('abbreviation', '')



    context = {
        'standings_data': standings_data,
    }

  
    return render(request, 'standings.html', context)

def fetch_mlb_standing():
    current_date = datetime.now().strftime('%m/%d/%Y')
    standings_data = statsapi.standings_data(leagueId="103,104", division="all", include_wildcard=True, date=current_date)

    for division in standings_data.values():
        for team in division['teams']:
            team['last_10'] = get_last_10_games(team['team_id'])

    return standings_data

def get_last_10_games(team_id):
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=15)  # 15 days back

    # Try to get the data from the database
    cached_data = GameData.objects.filter(team_id=team_id, date__range=[start_date, end_date]).order_by('-date')

    if cached_data.exists():
        games = [entry.game_data for entry in cached_data]
    else:
        games = statsapi.schedule(start_date=start_date.strftime('%Y-%m-%d'), end_date=end_date.strftime('%Y-%m-%d'), team=team_id)
        
        # Save this data to the database
        for game in games:
            GameData.objects.create(team_id=team_id, date=datetime.strptime(game['game_date'], '%Y-%m-%d').date(), game_data=game)
    
    # Filtering games that are 'Final'
    past_games = [game for game in games if "(Final)" in game['summary']]

    # Determine the outcomes for the team
    outcomes = []
    for game in past_games[-10:]:
        winning_team_id = game['home_id'] if game['home_name'] == game['winning_team'] else game['away_id']

        if team_id == winning_team_id:
            outcomes.append('W')
        else:
            outcomes.append('L')
    
    wins = outcomes.count('W')
    losses = outcomes.count('L')

    return f"{wins}-{losses}"

def fetch_mlb_news(all = False):
    
    MLB_RSS_URL = "https://www.mlb.com/feeds/news/rss.xml"
    response = requests.get(MLB_RSS_URL)
    root = ET.fromstring(response.content)

    entries_with_images = []

    for item in root.findall('.//item'):
        title = item.find('title').text
        link = item.find('link').text
        image_element = item.find('image')

        # Extract the author and date
        author = item.find('{http://purl.org/dc/elements/1.1/}creator')
        pubDate = item.find('pubDate')

        if image_element is not None and 'href' in image_element.attrib:
            image = image_element.attrib['href']
            entries_with_images.append({
                'title': title,
                'link': link,
                'image_href': image,
                'author': author.text if author is not None else "",
                'pubDate': pubDate.text if pubDate is not None else ""
            })
        else:
            print("No image in this entry")

    return entries_with_images if all else entries_with_images[:4]

def all_articles(request):
    all_entries = fetch_mlb_news(all=True)  
    return render(request, 'all_articles.html', {'entries': all_entries})

def division_standings(request):
    MLB_TEAMS_URL = "https://statsapi.mlb.com/api/v1/teams?sportId=1"
    MLB_STANDINGS_URL = "https://statsapi.mlb.com/api/v1/standings?leagueId=103,104"

    response_teams = requests.get(MLB_TEAMS_URL)
    response_standings = requests.get(MLB_STANDINGS_URL)
    
    teams = response_teams.json().get('teams', [])
    standings = response_standings.json().get('records', [])
    
    divisions = {}
    for division_standings in standings:
        division_name = division_standings.get('division', {}).get('name')
        team_records = [
            {
                'team_name': team['team']['name'],
                'wins': team['leagueRecord']['wins'],
                'losses': team['leagueRecord']['losses']
            }
            for team in division_standings.get('teamRecords', [])
        ]
        divisions[division_name] = team_records

    context = {'divisions': divisions}
    
    news_entries = fetch_mlb_news()
    
    context = {'divisions': divisions, 'news_entries': news_entries[:5]}  # Limit to 5 recent news
    
    return render(request, 'mlb_stats/division_standings.html', context)

def team_info(request, team_id):

    context = {}
    context['roster'] = get_team_roster(team_id)
    context['hitting_fields'] = ["gamesPlayed", "groundOuts", "airOuts", "runs", "doubles", "triples", 
    "homeRuns", "strikeOuts", "baseOnBalls", "intentionalWalks", "hits",
    "hitByPitch", "avg", "atBats", "obp", "slg", "ops", "caughtStealing", 
    "stolenBases", "stolenBasePercentage", "groundIntoDoublePlay", "numberOfPitches",
    "plateAppearances", "totalBases", "rbi", "leftOnBase", "sacBunts", "sacFlies", 
    "babip", "groundOutsToAirouts", "catchersInterference", "atBatsPerHomeRun"]
    context['pitching_fields'] = ["gamesPlayed", "gamesStarted", "groundOuts", "airOuts", "runs", "doubles", 
    "triples", "homeRuns", "strikeOuts", "baseOnBalls", "intentionalWalks", 
    "hits", "hitByPitch", "avg", "atBats", "obp", "slg", "ops", "caughtStealing", 
    "stolenBases", "stolenBasePercentage", "groundIntoDoublePlay", "numberOfPitches", 
    "era", "inningsPitched", "wins", "losses", "saves", "saveOpportunities", "holds", 
    "blownSaves", "earnedRuns", "whip", "battersFaced", "outs", "gamesPitched", 
    "completeGames", "shutouts", "strikes", "strikePercentage", "hitBatsmen", "balks", 
    "wildPitches", "pickoffs", "totalBases", "groundOutsToAirouts", "winPercentage", 
    "pitchesPerInning", "gamesFinished", "strikeoutWalkRatio", "strikeoutsPer9Inn", 
    "walksPer9Inn", "hitsPer9Inn", "runsScoredPer9", "homeRunsPer9", "inheritedRunners", 
    "inheritedRunnersScored", "catchersInterference", "sacBunts", "sacFlies"]
    context['fielding_fields'] = ["gamesPlayed", "gamesStarted", "assists", "putOuts", "errors", "chances", 
    "fielding", "rangeFactorPerGame", "rangeFactorPer9Inn", "innings", "games", 
    "doublePlays", "triplePlays", "throwingErrors"]
    

    # Fetch the last completed game
    last_completed_game = statsapi.last_game(team_id)

    if last_completed_game:
        game_pk = last_completed_game
        # Fetch highlights for the game
        game_highlights = statsapi.game_highlight_data(game_pk)
        context['game_highlights'] = game_highlights
    else:
        context['game_highlights'] = None

    return render(request, 'team_info.html', context)

def update_team_roster(team_id):


    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    TEAM_INFO_PATH = os.path.join(BASE_DIR, 'static', 'team_info.json')
    
    # Load current data from team_info.json
    with open(TEAM_INFO_PATH, "r") as file:
        all_teams_data = json.load(file)

    # If the team_id already exists, we skip further processing and return the existing data
    #if str(team_id) in all_teams_data:
    #    return all_teams_data[str(team_id)]

    # Fetch the roster data
    roster_data = statsapi.roster(team_id)
    lines = roster_data.split('\n')

    players = []
    for line in lines:
        parts = line.split('  ', 2)
        if len(parts) != 3:
            continue

        number, position, name = parts
        number = number[1:]

        # Extract the last name from the full name
        last_name = name.split()[-1]

        # Look up player based on last name
        player_lookup = statsapi.lookup_player(last_name + ',', gameType="R", season=2023)
        
        if not player_lookup:
            print(f"Could not find player with name {name}.")
            continue

        player_id = player_lookup[0]['id']

        try:
            # Fetch stats for the player for the current season
            hitting_string = statsapi.player_stats(player_id, 'hitting', 'season')
            pitching_string = statsapi.player_stats(player_id, 'pitching', 'season')
            fielding_string = statsapi.player_stats(player_id, 'fielding', 'season')

            hitting_stats = process_stat_string(hitting_string)
            pitching_stats = process_stat_string(pitching_string)
            fielding_stats = process_stat_string(fielding_string)

        except TypeError:
            print(f"Error retrieving stats for {name}.")
            hitting_stats, pitching_stats, fielding_stats = None, None, None

        players.append({
            "id": player_id,
            "name": name,
            "position": position,
            "number": number,
            "team_id": team_id,
            "hitting": hitting_stats,
            "pitching": pitching_stats,
            "fielding": fielding_stats
        })
    
    all_teams_data[str(team_id)] = players

    with open(TEAM_INFO_PATH, "w") as file:
        json.dump(all_teams_data, file, indent=4)

    return players

def get_team_roster(team_id):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    TEAM_INFO_PATH = os.path.join(BASE_DIR, 'static', 'team_info.json')
    
    # Load current data from team_info.json
    with open(TEAM_INFO_PATH, "r") as file:
        all_teams_data = json.load(file)

    return all_teams_data[str(team_id)]

def process_stat_string(stat_string):
    lines = stat_string.split('\n')
    stat_dict = {}
    for line in lines:
        parts = line.split(':')
        if len(parts) == 2:
            key, value = parts[0].strip(), parts[1].strip()
            stat_dict[key] = value
    return stat_dict

import statsapi

def leaderboards(request):
    # Fetch HR Leaders
    hr_leaders = statsapi.league_leader_data(
        leaderCategories='homeRuns',
        season=2023, 
        limit=10,
        statGroup='hitting'
    )
    
    # Fetch OPS Leaders
    ops_leaders = statsapi.league_leader_data(
        leaderCategories='onBasePlusSlugging',
        season=2023,
        limit=10,
        statGroup='hitting'
    )
    
    # Fetch ERA Leaders
    era_leaders = statsapi.league_leader_data(
        leaderCategories='earnedRunAverage',
        season=2023,
        limit=10,
        statGroup='pitching'
    )
    
    # Fetch Strikeout Leaders
    strikeout_leaders = statsapi.league_leader_data(
        leaderCategories='strikeOuts',
        season=2023,
        limit=10,
        statGroup='pitching'
    )
    
    # Pass the data to the template
    context = {
        'hr_leaders': hr_leaders,
        'ops_leaders': ops_leaders,
        'era_leaders': era_leaders,
        'strikeout_leaders': strikeout_leaders,
    }
    
    return render(request, 'leaderboards.html', context)




    
