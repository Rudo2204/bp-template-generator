import re
import sys
import os
import time
import subprocess
from bs4 import BeautifulSoup
from IPython.display import clear_output
from jikanpy import Jikan

jikan = Jikan()

#@markdown ###MAL Information
Anime_URL_OR_ID = '' #@param {type: "string"}
mal_pattern = re.compile('(anime)?/(\d{1,7})/(.+)?')
if re.match(r'\d+', Anime_URL_OR_ID):
  mal_id = Anime_URL_OR_ID
else:
  mal_id = re.findall(mal_pattern, Anime_URL_OR_ID)[0][1]
youtube_pattern = re.compile('(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})')

def get_mal_template(mal_id):
  # Fetch data
  anime_data = jikan.anime(mal_id)
  #@markdown ---
  #@markdown ###Anime Information
  Screenshot = "" #@param {type:"string"}
  if Screenshot != "":
    screenshot_list = Screenshot.split(" ")
    screenshot_enabled = True
  else:
    screenshot_enabled = False

  def get_info(anime_data, info):
    text = ''
    for i in range(len(anime_data[f'{info}'])):
      text += anime_data[info][i]['name'] + ', '
    return text[:-2]

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

  # Process data
  text_dump = "[center][img]{}[/img]\n".format(anime_data['image_url'])
  text_dump += "[color=rgb(250, 197, 28)][b][size=6]{} ({} - {})[/size][/b][/color]\n".format(anime_data['title'], anime_data['type'], anime_data['premiered'])
  text_dump += "[url={}][img]https://i.imgur.com/YJgzM4V.png[/img][/url][size=6][b] {}[/b]/10[/size]".format(anime_data['url'], anime_data['score'])
  text_dump += "[size=6] --- [img]https://i.imgur.com/sEpKj3O.png[/img]{}[/size][/center]\n".format(anime_data['scored_by'])
  text_dump += "[hr][/hr][indent][size=6][color=rgb(147, 101, 184)][b]Synopsis[/b][/color][/size][/indent]\n"
  text_dump += "[color=rgb(26, 188, 156)]{}\n[/color]".format(anime_data['synopsis'])
  try:
    text_dump += "[hr][/hr][indent][size=6][color=rgb(147, 101, 184)][b]Trailer[/b][/color][/size][/indent]\n"
    text_dump += "[media=youtube]{}[/media]\n".format(re.match(youtube_pattern, str(anime_data['trailer_url'])).group(6))
  except:
    pass
  if screenshot_enabled:
    text_dump += "[hr][/hr][indent][size=6][color=rgb(147, 101, 184)][b]Screenshot[/b][/color][/size][/indent]\n"
    text_dump += "[spoiler='Click here to view screenshots']\n"
    for i in screenshot_list:
      text_dump += "[img]{}[/img]\n".format(i)
    text_dump += "[/spoiler]"
  text_dump += "[hr][/hr][indent][size=6][color=rgb(147, 101, 184)][b]Anime Info[/b][/color][/size][/indent]\n"
  text_dump += "[LIST][*][color=rgb(251, 160, 38)]Rating:[/color] {}\n".format(anime_data['rating'])
  text_dump += "[*][color=rgb(251, 160, 38)]Type:[/color] {}\n".format(anime_data['type'])
  text_dump += "[*][color=rgb(251, 160, 38)]Episodes:[/color] {}\n".format(anime_data['episodes'])
  text_dump += "[*][color=rgb(251, 160, 38)]Status:[/color] {}\n".format(anime_data['status'])
  text_dump += "[*][color=rgb(251, 160, 38)]Aired:[/color] {}\n".format(anime_data['aired']['string'])
  text_dump += "[*][color=rgb(251, 160, 38)]Premiered:[/color] {}\n".format(anime_data['premiered'])
  text_dump += "[*][color=rgb(251, 160, 38)]Producers:[/color] {}\n".format(get_info(anime_data, 'producers'))
  text_dump += "[*][color=rgb(251, 160, 38)]Studios:[/color] {}\n".format(get_info(anime_data, 'studios'))
  text_dump += "[*][color=rgb(251, 160, 38)]Source:[/color] {}\n".format(anime_data['source'])
  text_dump += "[*][color=rgb(251, 160, 38)]Genres:[/color] {}\n".format(get_info(anime_data, 'genres'))
  text_dump += "[*][color=rgb(251, 160, 38)]Duration:[/color] {}\n".format(anime_data['duration'])
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

print(get_mal_template(mal_id))
