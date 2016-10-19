#coding:utf-8
from splinter import Browser
from bs4 import BeautifulSoup
import time
import re
import xlrd
import torndb

userEmail = '*****'
passPass = '*****'
rootUrl = 'http://www.welovewe.com/Data/'
playerfetching, playerfetched = set(), set()
countryfetching, countryfetched = set(), set()
clubfetching, clubfetched = set(), set()
player_id = 1

db_link = torndb.Connection(
			host = '127.0.0.1:3306', 
			database = 'welovewe', 
			user = 'root', 
			password = '*****'
		)

BIRTH_RE = re.compile(r'(\d{4})-(\d{2})-(\d{2})')
CARD_RE= re.compile(r'(^\D)(\d{2})')
COUNTRY_RE = re.compile(r'PlayerCountryList.aspx')
CLUB_RE = re.compile(r'PlayerClubList.aspx')

class Lovebrowser(object):

	def __init__(self):
		self._browser = Browser('chrome')
		self._browser.visit("http://www.welovewe.com/sns/register.aspx")
		self._browser.fill('ctl00$ContentPlaceHolder1$userEmail', userEmail)
		self._browser.fill('ctl00$ContentPlaceHolder1$userPass', passPass)
		self._browser.find_by_css('.button').first.click()

	@property
	def browser(self):
		return self._browser

MyBrowser = Lovebrowser()
browser = MyBrowser.browser


def getPlayerDetail(player):

	playerurl =rootUrl + player['url']
	browser.visit(playerurl)
	html = browser.html
	bs=BeautifulSoup(html,"html.parser")

	playerinfotab = bs.find("table", class_= "player_r").find_all('tr')

	birthtext = playerinfotab[2].find_all("td")[0].get_text()
	birth = BIRTH_RE.search(birthtext)

	birthday = birth.group()

	playerimage = bs.find("table", class_="player_r").find_all('tr')
	imagepath = playerimage[0].find_all('td')[0].img['src']
	imagepath = imagepath.strip(' .')
	player['player_img1'] = rootUrl + imagepath
	player['birthday'] = birthday



	playerAbilitytab = bs.find("table", class_="player_ability").find_all('tr')[1:]
	#player = {}

	player['player_cname'] = playerAbilitytab[0].find_all('td')[1].get_text()
	player['attack'] = playerAbilitytab[0].find_all('td')[3].get_text()
	player['accerleration'] = playerAbilitytab[0].find_all('td')[5].get_text()
	
	player['realname'] = playerAbilitytab[1].find_all('td')[1].get_text()
	player['dribble_accuracy'] = playerAbilitytab[1].find_all('td')[3].get_text()
	player['body_balance'] = playerAbilitytab[1].find_all('td')[5].get_text()

	player['fake_player'] = playerAbilitytab[2].find_all('td')[1].get_text()
	player['dribble_speed'] = playerAbilitytab[2].find_all('td')[3].get_text()
	player['aggression'] = playerAbilitytab[2].find_all('td')[5].get_text()

	player['live_name'] = playerAbilitytab[3].find_all('td')[1].get_text()
	player['short_pass_accuracy'] = playerAbilitytab[3].find_all('td')[3].get_text()
	player['jump'] = playerAbilitytab[3].find_all('td')[5].get_text()

	player['shirt_name'] = playerAbilitytab[4].find_all('td')[1].get_text()
	player['long_pass_accuracy'] = playerAbilitytab[4].find_all('td')[3].get_text()
	player['goal_keep'] = playerAbilitytab[4].find_all('td')[5].get_text()

	player['nationality'] = playerAbilitytab[5].find_all('td')[1].get_text()
	player['shot_accuracy'] = playerAbilitytab[5].find_all('td')[3].get_text()
	player['the_ball'] = playerAbilitytab[5].find_all('td')[5].get_text()

	player['nation_team'] = playerAbilitytab[6].find_all('td')[1].get_text()
	player['freekick_accuracy'] = playerAbilitytab[6].find_all('td')[3].get_text()
	player['rescue'] = playerAbilitytab[6].find_all('td')[5].get_text()

	player['club_name'] = playerAbilitytab[7].find_all('td')[1].get_text()
	player['swerve'] = playerAbilitytab[7].find_all('td')[3].get_text()
	player['response'] = playerAbilitytab[7].find_all('td')[5].get_text()

	player['age'] = playerAbilitytab[8].find_all('td')[1].get_text()
	player['header'] = playerAbilitytab[8].find_all('td')[3].get_text()
	player['mentality'] = playerAbilitytab[8].find_all('td')[5].get_text()

	player['defence'] = playerAbilitytab[9].find_all('td')[3].get_text()
	player['stamina'] = playerAbilitytab[9].find_all('td')[5].get_text()

	player['good_feet'] = playerAbilitytab[10].find_all('td')[1].get_text()
	player['grab_ball'] = playerAbilitytab[10].find_all('td')[3].get_text()
	player['resis2injury'] = playerAbilitytab[10].find_all('td')[5].get_text()

	player['game_style'] = playerAbilitytab[11].find_all('td')[1].get_text()
	player['shot_power'] = playerAbilitytab[11].find_all('td')[3].get_text()
	player['weak_foot_fre'] = playerAbilitytab[11].find_all('td')[5].get_text()

	player['top_speed'] = playerAbilitytab[12].find_all('td')[3].get_text()
	player['weak_foot_acc'] = playerAbilitytab[12].find_all('td')[5].get_text()


	playerPostab = bs.find("table", class_="player_position").find_all('tr')[1:]

	playerpos = {}
	for i in range(len(playerPostab)-1):
		key = playerPostab[i].find_all('td')[0].get_text()
		value = playerPostab[i].find_all('td')[1].get_text()
		playerpos[key] = value

	player['con_fitness'] = playerPostab[len(playerPostab)-1].find_all('td')[1].get_text()
	#player['fit_position'] = playerpos

	playerCardstab = bs.find("table", class_="player_cards").find_all('tr')[1:]

	play_style = []
	play_skill = []

	for i in range(len(playerCardstab)):
		code = playerCardstab[i].find_all('td')[1].get_text()
		name = playerCardstab[i].find_all('td')[2].get_text()
		code = CARD_RE.search(code)
		detailstr = code.group(2) + ' ' + name
		if code.group(1) == 'P':
			play_style.append(detailstr)
		else:
			play_skill.append(detailstr)


	_inserPlayer(player)
	_insertPlayerfit(playerpos, player['realname'])
	_insertPlayerstyle(play_style, player['realname'])
	_insertPlayerskill(play_skill, player['realname'])

	#更新player id
	global player_id
	player_id = player_id + 1

#更新player表
def _inserPlayer(player):

	playerlist = [player_id, player['club_player_id'], player['country_player_id'],
				  player['player_img1'], '', player['nationality'], player['nation_team'],
				  player['constellation'], player['default_location'], player['comprehensive_value'],
				  player['age'], player['height'], player['weight'], player['birthday'],
				  '', player['player_cname'], player['realname'], player['fake_player'],
				  player['live_name'], player['shirt_name'], player['club_name'],
				  player['good_feet'], player['game_style'], player['attack'],
				  player['dribble_accuracy'], player['dribble_speed'], player['short_pass_accuracy'],
				  player['long_pass_accuracy'], player['shot_accuracy'], player['freekick_accuracy'],
				  player['swerve'], player['header'], player['defence'], player['grab_ball'],
				  player['shot_power'], player['top_speed'], player['accerleration'],
				  player['body_balance'], player['aggression'], player['jump'],
				  player['goal_keep'], player['the_ball'], player['rescue'], player['response'],
				  player['mentality'], player['stamina'], player['resis2injury'],
				  player['weak_foot_fre'], player['weak_foot_acc'], player['con_fitness']]

	playerlist.insert(0, '0')
	sql = "INSERT INTO player VALUES %s"
	id = db_link.insert(sql, playerlist)

#更新player_fit表	
def _insertPlayerfit(playerpos, realname):
	
	sql = "INSERT INTO player_fit VALUES %s"
	for (key, value) in playerpos.items():
		fitlist = [player_id, realname, key, value]
		fitlist.insert(0, '0')
		id = db_link.insert(sql, fitlist)

#更新player_style表
def _insertPlayerstyle(play_style, realname):
	
	sql = "INSERT INTO player_style VALUES %s"
	for i in range(len(play_style)):
		sytle_id, sytle_name = play_style[i].split(' ')
		stylelist = [player_id, realname, sytle_id, sytle_name]
		stylelist.insert(0, '0')
		id = db_link.insert(sql, stylelist)

#更新player_skill表
def _insertPlayerskill(play_skill, realname):
	
	sql = "INSERT INTO player_skill VALUES %s"
	for i in range(len(play_skill)):
		skill_id, skill_name = play_skill[i].split(' ')
		skilllist = [player_id, realname, skill_id, skill_name]
		skilllist.insert(0, '0')
		id = db_link.insert(sql, skilllist)


def getPlayerCountryList(url):

	playerurl =rootUrl + url
	browser.visit(playerurl)
	html = browser.html
	bs=BeautifulSoup(html,"html.parser")

	playerlisttab = bs.find("div", id= "playerListTab").table.find_all('tr')[1:]

	for i in range(len(playerlisttab)):
		tds = playerlisttab[i].find_all('td')
		player = {}
		player['country_player_id'] = tds[0].get_text()
		player['url'] = tds[1].a['href']
		player['constellation'] = tds[3].get_text()
		player['default_location'] = tds[4].get_text()
		player['comprehensive_value'] = tds[5].get_text()
		player['height'] = tds[7].get_text()
		player['weight'] = tds[8].get_text()
		player['club_player_id'] = ''
		club_name = tds[2].get_text()

		if (player['url'] in playerfetching) or (club_name.strip() != u"Free Agents"):
			continue

		print('fetching %s' % player['url'])
		playerfetching.add(player['url'])
		getPlayerDetail(player)
		playerfetched.add(player['url'])

def getPlayerClubList(url):

	playerurl =rootUrl + url
	browser.visit(playerurl)
	html = browser.html
	bs=BeautifulSoup(html,"html.parser")

	playerlisttab = bs.find("div", id= "playerListTab").table.find_all('tr')[1:]

	for i in range(len(playerlisttab)):
		tds = playerlisttab[i].find_all('td')
		player = {}
		player['club_player_id'] = tds[0].get_text()
		player['url'] = tds[1].a['href']
		player['constellation'] = tds[4].get_text()
		player['default_location'] = tds[5].get_text()
		player['comprehensive_value'] = tds[6].get_text()
		player['height'] = tds[8].get_text()
		player['weight'] = tds[9].get_text()

		countryplayer = tds[3].get_text().strip()
		player_name = tds[1].a.get_text().strip()
		#countryplayer.strip()

		if player['url'] in playerfetching:
			continue

		if countryplayer != u'—':
			countryurl = tds[3].a['href']
			country_player_id = getCountryPlayerid(countryurl, player_name)
		else:
			country_player_id = ''
		player['country_player_id'] = country_player_id 

		print('fetching %s' % player['url'])
		playerfetching.add(player['url'])
		getPlayerDetail(player)
		playerfetched.add(player['url'])

def getCountryPlayerid(url, player_name):

	playerurl =rootUrl + url
	browser.visit(playerurl)
	html = browser.html
	bs=BeautifulSoup(html,"html.parser")

	namenode = bs.find('a', text = re.compile(player_name))
	parentnode = namenode.parent.parent
	country_player_id = parentnode.find_all('td')[0].get_text()
	return country_player_id


def mainhandler(url):

	mainurl = rootUrl + url
	browser.visit(mainurl)
	html = browser.html
	bs = BeautifulSoup(html, "html.parser")

	countrylist = bs.find_all(href = COUNTRY_RE)
	clublist = bs.find_all(href = CLUB_RE)

	根据国家更新球员数据
	for i in range(len(countrylist)):

		# if i >= 3:
		# 	break
		href = countrylist[i]['href']
		if href in countryfetching:
			continue

		print('fetching %s' % href)
		countryfetching.add(href)
		getPlayerCountryList(href)

	#根据俱乐部更新球员数据
	for i in range(len(clublist)):

		# if i >= 3:
		# 	break
		href = clublist[i]['href']
		if href in clubfetching:
			continue

		print('fetching %s' % href)
		clubfetching.add(href)
		getPlayerClubList(href)

def _getExcelpath():
	rootpath = os.path.dirname(os.path.abspath("__file__"))
	excelpath = os.path.join(rootpath, u'实况足球2017数据库表.xlsx')
	return excelpath

     
if __name__=="__main__":
	#cookie_test()
	#getPlayerDetail("PlayerDetail.aspx?id=943&flag=1")
	#getPlayerCountryList('PlayerCountryList.aspx?id=88')
	#getPlayerClubList('PlayerClubList.aspx?id=153')
	mainhandler('Players.aspx')





