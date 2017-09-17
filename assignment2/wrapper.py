from bs4 import BeautifulSoup
import re
import codecs
import sys
import json

f = codecs.open(sys.argv[1])
output = codecs.open(sys.argv[2], "w")
# f = codecs.open("test.jl")
ii=0
for line in f:
    profile = dict()

    data = json.loads(line)

    url = data["url"]
    profile["name"] = url.split('/')[3].replace("-", " ").strip()

    html_doc = data["raw_content"]
    soup = BeautifulSoup(html_doc, 'html.parser')

    international_wins = soup(text=re.compile(r'International caps/goals'))
    if international_wins:
        international_win = international_wins[0].parent.parent
        if len(international_win.find_all('a')) == 2:
            profile["international honors"] = dict()
            profile["international honors"]["caps"] = int(international_win.find_all('a')[0].text)
            profile["international honors"]["goals"] = int(international_win.find_all('a')[1].text)

    if soup(text=re.compile(r'League level')):
        profile["league level"] = dict()
        league_level = soup(text=re.compile(r'League level'))[0].parent.next_sibling.next_sibling
        profile["league level"]["country"] = league_level.img.get("title").strip()
        profile["league level"]["level"] = league_level.text.strip()
        
    if soup.find("div", {"class": "dataErfolge hide-for-small"}):
        profile["club bonors"] = dict()
        club_wins = soup.find("div", {"class": "dataErfolge hide-for-small"})
        for a in club_wins.find_all('a'):
            profile["club bonors"][a.get("title").strip().lower()] = int(a.find("span", {"class": "dataErfolgAnzahl"}).text) if a.find("span", {"class": "dataErfolgAnzahl"}) else "none"


    player_data = soup.find("table", {"class":"auflistung"})

    for tr in player_data.find_all("tr"):
        if tr.th.text.strip().replace(":", "").lower() == "social media":
            profile["social media"] = dict()
            for a in tr.td.find_all('a'):
                profile["social media"][a.get('title').strip().lower()] = a.get('href')
        else:
            if tr.find_all("br"):
                profile[tr.th.text.strip().replace(":", "").lower()] = [x.replace(u"\u00A0", " ").strip() for x in tr.td.text.strip().split()]
            else:
                profile[tr.th.text.strip().replace(":", "").lower()] = tr.td.text.strip().replace(
                    u"\u00A0", " ") if tr.td.text.strip() != "-" else "unknown"

    if soup(text=re.compile(r'Main position:')) and soup(text=re.compile(r'Other position')):
        profile["detailed positions"] = dict()
        main_positions = soup(text=re.compile(r'Main position:'))[0].parent.parent.find_all('br')
        profile["detailed positions"]["main positions"] = []
        for br in main_positions:
            profile["detailed positions"]["main positions"].append(br.next_sibling.strip())
        other_positions = soup(text=re.compile(r'Other position'))[0].parent.parent.find_all('br')
        profile["detailed positions"]["other positions"] = []
        for br in other_positions:
            profile["detailed positions"]["other positions"].append(br.next_sibling.strip())

    if soup(text=re.compile(r'Current market value:')):
        profile["current market value"] = dict()
        value = soup(text=re.compile(r'Current market value'))[0].parent.find_next_sibling("div")
        profile["current market value"]["value"] = value.text.encode('utf-8').replace(
            "\xc3\xa2\xc2\x82\xc2\xac","EUR").strip()
        profile["current market value"]["last change"] = value.parent.find_next_sibling("div").find_all(
            "span")[1].text.strip()

    if soup(text=re.compile(r'Highest market value')):
        profile["highest market value"] = dict()
        value = soup(text=re.compile(r'Highest market value'))[0].parent.find_next_sibling("div")
        profile["highest market value"]["value"] = value.contents[0].encode('utf-8').replace(
            "\xc3\xa2\xc2\x82\xc2\xac","EUR").strip()
        profile["highest market value"]["reach date"] = value.span.text.strip()

    if soup(text=re.compile(r'Transfer history')):
        profile["transfer history"] = list()
        table = soup(text=re.compile(r'Transfer history'))[0].parent.parent.table
        # categories = [x.text.strip().lower() for x in table.thead.find_all("th")]
        records = table.tbody.find_all("tr", {"class": "zeile-transfer"})
        for record in records:
            this_record = dict()
            elements = record.find_all("td")
            this_record["season"] = elements[0].text.strip() if elements[0].text else "unknown"
            this_record["date"] = elements[1].text.strip() if elements[1].text else "unknown"
            this_record["moving from"] = dict()
            this_record["moving from"]["country"] = elements[3].img.get("title").strip() if elements[3].img else "unknown"
            this_record["moving from"]["club"] = elements[5].text.strip() if elements[5].text else "unknown"
            this_record["moving to"] = dict()
            this_record["moving to"]["country"] = elements[7].img.get("title").strip() if elements[7].img else "unknown"
            this_record["moving to"]["club"] = elements[9].text.strip() if elements[9].text else "unknown"
            if not (elements[10].text.strip() == "-" or elements[10].text.strip() == "?"):
                this_record["market value"] = elements[10].text.encode('utf-8').replace("\xc3\xa2\xc2\x82\xc2\xac", "EUR").strip() 
            else:
                this_record["market value"] = "unknown"
            if not (elements[10].text.strip() == "-" or elements[10].text.strip() == "?"):
                this_record["transfer fee"] = elements[11].text.encode('utf-8').replace("\xc3\xa2\xc2\x82\xc2\xac", "EUR").strip()
            else:
                this_record["transfer fee"] = "unknown"
            profile["transfer history"].append(this_record)

    if soup(text=re.compile(r'Comparable players')):
        profile["comparable players"] = list()
        compare_players = soup(text=re.compile(r'Comparable players'))[0].parent.parent.tbody
        for idx, child in enumerate(compare_players.children):
            if idx % 2 == 1:
                profile["comparable players"].append(child.a.text.strip())
                
    # data["knowledge_graph"] = profile
    json.dump(profile, output)
    print ii
    ii += 1
    output.write("\n")

f.close()
output.close()



