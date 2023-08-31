from django.shortcuts import render

import requests

import feedparser

def index(request):
    news_entries = fetch_mlb_news()
    context = {
        'news_entries': news_entries
    }
    return render(request, 'index.html', context)





import xml.etree.ElementTree as ET
import requests

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
            print("Image URL:", image)
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
    all_entries = fetch_mlb_news(all=True)  # See modification in next step
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



