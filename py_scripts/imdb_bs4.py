import urllib.request
import json
import re
import requests
import sys
import subprocess
import os
import time
from bs4 import BeautifulSoup

# Variables
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0'}
#@markdown ###Insert your API key
api_key = '' #@param {type:"string"}
#@markdown ---
#@markdown ###IMDB Information
IMDB_URL_OR_ID = '' #@param {type:"string"}
imdb_pattern = re.compile('(tt\d{7,8})')
youtube_pattern = re.compile('(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})')
imdb_id = re.findall(imdb_pattern, IMDB_URL_OR_ID)[0]

def get_imdb_template(imdb_id):
  imdb_url = f'http://www.omdbapi.com/?i={imdb_id}&apikey={api_key}&r=json&plot=full'
  #@markdown ---
  #@markdown ###Movie Information
  Trailer = "" #@param {type:"string"}
  Screenshot = "" #@param {type:"string"}
  youtube_match = re.match(youtube_pattern, Trailer)
  if Trailer != "":
    if not youtube_match:
      clear_output()
      print('Your trailer link is invalid. Please only put in youtube link!')
      sys.exit()
    else:
      trailer_enabled = True
  else:
    trailer_enabled = False

  if Screenshot != "":
    screenshot_list = Screenshot.split(" ")
    screenshot_enabled = True
  else:
    screenshot_enabled = False

  Path = "" #@param {type:"string"}
  if Path == "":
    mediainfo_enabled = False
  else:
    mediainfo_enabled = True
    tmp = subprocess.Popen('mediainfo --Logfile=/root/.nfo "{}"'.format(Path), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    time.sleep(5) # Wait 5s for the nfo file to populate properly
    with open('/root/.nfo', 'r', encoding='utf-8') as nfo_file:
      nfo = nfo_file.readlines()
      del nfo[1]
      nfo[1] = "Complete name                            : {}\n".format(os.path.basename(Path))
      nfo = ''.join(nfo)

  Link = "" #@param {type:"string"}
  if Link == "":
    print("You forgot putting in the link to download!")
    sys.exit()

  #@markdown ---
  #@markdown ###Forum Requirements
  Likes = 0 #@param {type: "number"}
  Posts = 0 #@param {type: "number"}
  Thanks = True #@param {type:"boolean"}

  def get_story_line(imdb_id):
    url = 'https://www.imdb.com/title/{}'.format(imdb_id)
    r = requests.get(url, headers=headers)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')
    story_line = soup.find_all('div', class_='inline canwrap')[0].find('span').text.lstrip()
    return story_line

  # Fetch data
  with urllib.request.urlopen(imdb_url) as imdb_url:
    imdb_data = json.loads(imdb_url.read().decode())

  # Process data
  text_dump = "[center][img]{}[/img]\n".format(imdb_data['Poster'])
  text_dump += "[color=rgb(250, 197, 28)][b][size=6]{} ({})[/size][/b][/color]\n".format(imdb_data['Title'], imdb_data['Year'])
  text_dump += "[url=https://www.imdb.com/title/{}][img]https://i.imgur.com/rcSipDw.png[/img][/url][size=6][b] {}[/b]/10[/size]".format(imdb_id, imdb_data['imdbRating'])
  text_dump += "[size=6] --- [img]https://i.imgur.com/sEpKj3O.png[/img]{}[/size][/center]\n".format(imdb_data['imdbVotes'])
  text_dump += "[hr][/hr][indent][size=6][color=rgb(147, 101, 184)][b]Plot Summary[/b][/color][/size][/indent]\n"
  text_dump += "[color=rgb(26, 188, 156)]{}\n[/color]".format(get_story_line(imdb_id))
  if trailer_enabled:
    text_dump += "[hr][/hr][indent][size=6][color=rgb(147, 101, 184)][b]Trailer[/b][/color][/size][/indent]\n"
    text_dump += "[media=youtube]{}[/media]\n".format(youtube_match.group(6))
  if screenshot_enabled:
    text_dump += "[hr][/hr][indent][size=6][color=rgb(147, 101, 184)][b]Screenshot[/b][/color][/size][/indent]\n"
    text_dump += "[spoiler='Click here to view screenshots']\n"
    for i in screenshot_list:
      text_dump += "[img]{}[/img]\n".format(i)
    text_dump += "[/spoiler]"
  text_dump += "[hr][/hr][indent][size=6][color=rgb(147, 101, 184)][b]Movie Info[/b][/color][/size][/indent]\n"
  text_dump += "[LIST][*][color=rgb(251, 160, 38)]Rating:[/color] {}\n".format(imdb_data['Rated'])
  text_dump += "[*][color=rgb(251, 160, 38)]Genre:[/color] {}\n".format(imdb_data['Genre'])
  text_dump += "[*][color=rgb(251, 160, 38)]Directed By:[/color] {}\n".format(imdb_data['Director'])
  text_dump += "[*][color=rgb(251, 160, 38)]Written By:[/color] {}\n".format(imdb_data['Writer'])
  text_dump += "[*][color=rgb(251, 160, 38)]Starring:[/color] {}\n".format(imdb_data['Actors'])
  text_dump += "[*][color=rgb(251, 160, 38)]Release Date:[/color] {}\n".format(imdb_data['Released'])
  try:
    text_dump += "[*][color=rgb(251, 160, 38)]Runtime:[/color] {}\n".format(imdb_data['Runtime'])
  except:
    text_dump += "[*][color=rgb(251, 160, 38)]Runtime:[/color] N/A\n"
  try:
    text_dump += "[*][color=rgb(251, 160, 38)]On Disk/Streaming:[/color] {}\n".format(imdb_data['DVD'])
  except:
    text_dump += "[*][color=rgb(251, 160, 38)]On Disk/Streaming:[/color] N/A\n"
  try:
    text_dump += "[*][color=rgb(251, 160, 38)]Box Office:[/color] {}\n".format(imdb_data['BoxOffice'])
  except:
    text_dump += "[*][color=rgb(251, 160, 38)]Box Office:[/color] N/A\n"
  text_dump += "[*][color=rgb(251, 160, 38)]Awards:[/color] {}\n".format(imdb_data['Awards'])
  try:
    text_dump += "[*][color=rgb(251, 160, 38)]Studio:[/color] {}[/LIST]\n".format(imdb_data['Production'])
  except:
    text_dump += "[*][color=rgb(251, 160, 38)]Studio:[/color] N/A[/LIST]\n"
  if mediainfo_enabled:
    text_dump += "[hr][/hr][indent][size=6][color=rgb(147, 101, 184)][b]Media Info[/b][/color][/size][/indent]\n"
    text_dump += "[spoiler='Click here to view Media Info'][code]{}[/code][/spoiler]\n".format(nfo)
  text_dump += "[hr][/hr][center][size=6][color=rgb(209, 72, 65)][b]Download Link[/b][/color][/size][/center]\n"
  if Thanks:
    if Likes != 0 and Posts == 0:
      text_dump += "[center][thanks][likes={}]{}[/likes][/thanks][/center]".format(Likes, Link)
    elif Likes == 0 and Posts != 0:
      text_dump += "[center][thanks][posts={}]{}[/posts][/thanks][/center]".format(Posts, Link)
    elif Likes != 0 and Posts != 0:
      text_dump += "[center][thanks][likes={}][posts={}]{}[/posts][/likes][/thanks][/center]".format(Likes, Posts, Link)
    else:
      text_dump += "[center][thanks]{}[/thanks][/center]".format(Link)
  else:
    if Likes != 0 and Posts == 0:
      text_dump += "[center][likes={}]{}[/likes][/center]".format(Likes, Link)
    elif Likes == 0 and Posts != 0:
      text_dump += "[center][posts={}]{}[/posts][/center]".format(Posts, Link)
    elif Likes != 0 and Posts != 0:
      text_dump += "[center][likes={}][posts={}]{}[/posts][/likes][/center]".format(Likes, Posts, Link)
    else:
      text_dump += "[center]{}[/center]".format(Link)

  return text_dump

print(get_imdb_template(imdb_id))
