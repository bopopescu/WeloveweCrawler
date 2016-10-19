#coding=utf-8
import logging
import os

LOG = logging.getLogger()

try:
	import torndb
	import xlrd
except ImportError, e:
	LOG.error('%s, please install it before running', e)
	sys.exit(1)

db_link = torndb.Connection(
			host = '127.0.0.1:3306', 
			database = 'welovewe', 
			user = 'root', 
			password = 'tafee231400'
		)

class MySqlApi(object):

	@classmethod
	def insertCountry2Db(cls):
		res = _insert2Db('country')
		return res

	@classmethod
	def insertLeague2Db(cls):
		res = _insert2Db('league')
		return res

	@classmethod
	def insertClub2Db(cls):
		res = _insert2Db('club')
		return res

	@classmethod
	def insertPlayer2Db(cls):

		excelpath = _getExcelpath()
		wb = xlrd.open_workbook(excelpath)
		sh = wb.sheet_by_name(u'球员属性')

		for rownum in range(sh.nrows):
			if rownum in (0, 1):
				continue

			rowvalue = sh.row_values(rownum)
			if rowvalue[0] not in (None, ''):
				player_id = rowvalue[0]
				realname = rowvalue[16]

				#更新player表
				try:
					_inserPlayer(rowvalue)
				except Exception as e:
					LOG.error(e)
					res = { 'code': -1, 'msg': u'球员更新失败'}
					return res

			#更新player_fit表
			if rowvalue[49] not in (None, ''):
				try:
					values = [player_id, realname, rowvalue[49], rowvalue[50]]
					_insertPlayerproperty('player_fit', values)
				except Exception as e:
					LOG.error(e)
					res = { 'code': -1, 'msg': u'球员适合位置数据表更新失败'}
					return res

			#更新player_style表
			if rowvalue[52] not in (None, ''):
				style = rowvalue[52].strip()
				sytle_id, sytle_name = style.split(' ')
				try:
					values = [player_id, realname, sytle_id, sytle_name]
					_insertPlayerproperty('player_style', values)
				except Exception as e:
					LOG.error(e)
					res = { 'code': -1, 'msg': u'球员踢球风格表更新失败'}
					return res

			#更新player_skill表
			if rowvalue[53] not in (None, ''):
				skill = rowvalue[53].strip()
				skill_id, skill_name = skill.split(' ')
				try:
					values = [player_id, realname, skill_id, skill_name]
					_insertPlayerproperty('player_skill', values)
				except Exception as e:
					LOG.error(e)
					res = { 'code': -1, 'msg': u'球员足球技巧表更新失败'}
					return res

		res = { 'code': 0, 'msg': u'球员更新成功'}
		return res

def _getExcelpath():
	rootpath = os.path.dirname(os.path.abspath("__file__"))
	excelpath = os.path.join(rootpath, u'实况足球2017数据库表.xlsx')
	return excelpath

def _insert2Db(tablename):
	excelpath = _getExcelpath()
	sheetdic = {'club': u'国家与俱乐部',
				'country': u'国家与俱乐部',
				'league': u'国家与俱乐部'}
	tablepos = {'country': (9, 10),
				'league': (13, 14),
				'club': (17, 18)}
	sheetname = sheetdic.get(tablename)
	filterpos = tablepos.get(tablename)
	wb = xlrd.open_workbook(excelpath)
	sh = wb.sheet_by_name(sheetname)

	for rownum in range(sh.nrows):
		if rownum in (0, 1):
			continue

		rowvalue = sh.row_values(rownum)
		if rowvalue[filterpos[0]] in (None, '') and rowvalue[filterpos[1]] in (None, ''):
			break
		try:
			sql = "INSERT INTO " + tablename + " VALUES %s "
			values = rowvalue[filterpos[0]:(filterpos[0] + 4)]
			values.insert(0, '0')
			id = db_link.insert(sql, values)
		except Exception as e:
			LOG.error(e)
			msg = u'%s更新失败' % tablename
			res = { 'code': -1, 'msg': msg }
			return res
	msg = u'%s更新成功' % tablename
	res = { 'code': 0, 'msg': msg}
	return res

#更新player表
def _inserPlayer(rowvalue):
	playerlist = rowvalue[0:49]
	playerlist.append(rowvalue[51])
	playerlist.insert(0, '0')
	sql = "INSERT INTO player VALUES %s"
	id = db_link.insert(sql, playerlist)

#更新player属性表
def _insertPlayerproperty(tablename, values):
	sql = "INSERT INTO " + tablename + " VALUES %s "
	values.insert(0, '0')
	id = db_link.insert(sql, values)

if __name__=='__main__':
	try:
		res1 = MySqlApi.insertCountry2Db()
		res2 = MySqlApi.insertLeague2Db()
		res3 = MySqlApi.insertClub2Db()
		res4 = MySqlApi.insertPlayer2Db()
	except Exception as e:
		LOG.error(e)

	if not res1['code'] and not res2['code'] and not res3['code'] and not res4['code']:
		print "success"
	else:
		print "fail"