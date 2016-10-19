#coding=utf-8
import logging
import torndb
import os
import xlrd

from tornado.gen import coroutine, Return
from gpspic.db import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE

LOG = logging.getLogger()
global db_link 

db_link = torndb.Connection(
			host = MYSQL_HOST, 
			database = MYSQL_DATABASE, 
			user = MYSQL_USER, 
			password = MYSQL_PASSWORD
		)

class MySqlApi(object):

	@classmethod
	@coroutine
	def insertCountry2Db(cls):
		res = _insert2Db('country')
		raise Return(res)

	@classmethod
	@coroutine
	def insertLeague2Db(cls):
		res = _insert2Db('league')
		raise Return(res)

	@classmethod
	@coroutine
	def insertClub2Db(cls):
		res = _insert2Db('club')
		raise Return(res)

	@classmethod
	@coroutine
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
					raise Return(res)

			#更新player_fit表
			if rowvalue[49] not in (None, ''):
				try:
					values = [player_id, realname, rowvalue[49], rowvalue[50]]
					_insertPlayerproperty('player_fit', values)
				except Exception as e:
					LOG.error(e)
					res = { 'code': -1, 'msg': u'球员适合位置数据表更新失败'}
					raise Return(res)

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
					raise Return(res)

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
					raise Return(res)

		res = { 'code': 0, 'msg': u'球员更新成功'}
		raise Return(res)

def _getExcelpath():
	pardir = os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))
	rootpath, _ = os.path.split(pardir)
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
