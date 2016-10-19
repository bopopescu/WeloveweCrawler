#coding=utf-8
import os
import random
import hashlib
import logging
import time
import urllib
import json
import traceback
import hashlib
import datetime
import Geohash
import xlrd

from tornado.gen import coroutine

from conf import settings
from api import ApiHandler
from urllib import urlencode
from view import api_define, handler_define, Param, API_TYPE_COLLECT
from utils.password_enc import decode_password
from utils.htmlparse import parse_html
from utils.auth import auth_required
from lib.passport.passport import PassportUserApi, UisUserApi
from lib.cmsapi.async_cmsapi import CMSApi
from lib.stream.livestream import LiveStreamApi
from gpspic.db.db import MySqlApi

LOG = logging.getLogger()


@handler_define
class insertCountryhandler(ApiHandler):

    @coroutine
    @api_define('insert country to db', '/insert/country',
                params=[],
                filters=[],description=u'更新国家')
    def get(self):

        res =  yield MySqlApi.insertCountry2Db()
        self.write(res)

@handler_define
class insertLeaguehandler(ApiHandler):

    @coroutine
    @api_define('insert league to db', '/insert/league',
                params=[],
                filters=[],description=u'更新联赛')
    def get(self):
        res =  yield MySqlApi.insertLeague2Db()
        self.write(res)

@handler_define
class insertClubhandler(ApiHandler):

    @coroutine
    @api_define('insert club to db', '/insert/club',
                params=[],
                filters=[],description=u'更新俱乐部')
    def get(self):
        res =  yield MySqlApi.insertClub2Db()
        self.write(res)

@handler_define
class insertPlayerhandler(ApiHandler):

    @coroutine
    @api_define('insert player to db', '/insert/player',
                params=[],
                filters=[],description=u'更新球员')
    def get(self):
        res =  yield MySqlApi.insertPlayer2Db()
        self.write(res)




# @handler_define
# class UserLoginHandler(ApiHandler):

#     @coroutine
#     @api_define('user login', '/gpspic/user/login',
#                 params=[
#                     Param('loginname', True, str, None, 'honglu_life@163.com', '登录名'),
#                     Param('passwd', True, str, None, 'hong@119', '密码'),
#                     Param('remember', True, int, None, 0, '是否记住我（0|1）'),
#                     Param('enc', False, str, '0', '0', '用户密码是否加密，1是，0否，默认是否'),
#                     Param('pc', False, int, 0, 24, '填充字符的个数，默认为0'),
#                     Param('codeid', False, str, None, '', '获取登陆验证码图片接口返回的codeId值'),
#                     Param('vcode', False, str, None, '', '用户输入的验证码信息（内网不进行验证码检查）'),
#                 ],
#                 filters=[], description=u'用户登陆接口(用户状态，0：审核中，1：正常)',
#                 api_type=API_TYPE_COLLECT,
#                 source_wiki='http://wiki.corp.tudou.com:8080/confluence/pages/viewpage.action?pageId=15892789'+';'+\
#                             'http://wiki.corp.tudou.com:8080/confluence/pages/viewpage.action?pageId=28705068')
#     def post(self):
#         '''
#         User login
#         '''
#         loginname = self.get_str_argument('loginname')
#         passwd = self.get_str_argument('passwd', strip=False)
#         remember = self.get_str_argument('remember', scope=['0', '1'])
#         enc = self.get_str_argument('enc', default='0', scope=['0', '1'])
#         code_id = self.get_str_argument('codeid', '')
#         vcode = self.get_str_argument('vcode', '')
#         if enc == '1':
#             pc = self.get_int_argument('pc', default=0)
#             try:
#                 passwd = decode_password(passwd, pc)
#             except Exception, e:
#                 LOG.error(traceback.format_exc())
#                 self.write({'code': '994', 'msg': u'密码错误', 'result': {}})
#                 return

#         response, data = yield PassportUserApi.login(loginname, passwd, remember, code_id,
#                                                      vcode, ip=self.get_ip())
#         res = {}
#         if data.get('code') == 0:
#             data = data.get('data', {})
#             cookies = response.headers['set-cookie']
#             uid = data.get('uid', '')

#             pass_status = yield PassportUserApi.is_password_set(uid, self.get_ip())
#             data.update({'is_passwd_set': pass_status.get('code', 0)})

#             uinfo = {}
#             raw = yield UisUserApi.find_user(uid)
#             if raw.get('code', -1) == 0:
#                 uinfo = raw.get('data', {})
#                 uinfo['desc'] = parse_html(uinfo.get('desc', ''))
#             data.update({'username': uinfo.get('username'),
#                          'nickname': uinfo.get('nickname'),
#                          'userpic': uinfo.get('userpic'),
#                          'vip_member': uinfo.get('isMember'),
#                          'isVuser': uinfo.get('verifyType') in (1, 2),
#                          'userDesc': uinfo.get('desc', ''),
#                          'isLiveUser': -1,
#                         })

#             self.yktk_auth_login(uid, data.get('data', {}).get('yktk'), uinfo.get("uidCode", ""))

#             if cookies:
#                 self.set_cookies_from_back(cookies)

#             live_uinfo = yield CMSApi.query_user(uid)
#             if live_uinfo['data']['token'] is None and \
#                     live_uinfo['data']['user'] is None:
#                 yield CMSApi.insert_user(uid)
#                 live_uinfo = yield CMSApi.query_user(uid)

#             data['isLiveUser'] = live_uinfo['data']['user']['status']
#             data['liveToken'] = live_uinfo['data']['token']

#             res['code'] = 0
#             res['msg'] = u'成功'
#             res['data'] = data
#         else:
#             res = {'code': -1, 'msg': u'失败', 'result': data}

#         self.write(res)

# @handler_define
# class UserStatusHandler(ApiHandler):

#     @auth_required
#     @coroutine
#     @api_define('user live status', '/gpspic/user/status',
#                 params=[
#                 ],
#                 filters=[], description=u'获取用户信息(0：审核中，1：正常)',
#                 api_type=API_TYPE_COLLECT)
#     def get(self):
#         '''
#         get user live status
#         '''
#         res = yield CMSApi.query_user(self.current_user_id)
#         self.write(res)

# @handler_define
# class UserApplyHandler(ApiHandler):

#     @auth_required
#     @coroutine
#     @api_define('user login', '/gpspic/user/apply',
#                 params=[
#                     Param('name', True, str, None, 'JayChow', '姓名'),
#                     Param('phone', True, str, None, '13012345678', '手机'),
#                     Param('email', True, int, None, 'test@tudou.com', '邮箱'),
#                     Param('reason', True, str, None, '个人直播', '申请用途'),
#                 ],
#                 filters=[], description=u'申请成为直播用户',
#                 api_type=API_TYPE_COLLECT, offline=True)
#     def post(self):
#         '''
#         User apply
#         '''
#         name = self.get_str_argument('name')
#         phone = self.get_str_argument('phone')
#         email = self.get_str_argument('email')
#         reason = self.get_str_argument('reason')
 
#         res = yield CMSApi.insert_user(self.current_user_id,
#                                        name, phone, email, reason)
#         self.write(res)

# @handler_define
# class LiveShowListHandler(ApiHandler):

#     @auth_required
#     @coroutine
#     @api_define('live show list', '/gpspic/user/liveshow/list',
#                 params=[
#                     Param('pn', True, int, 1, '1', '页号'),
#                     Param('pz', True, int, 10, '10', '每页数量'),
#                 ],
#                 filters=[], description=u'获取直播用户的直播列表(直播状态liveStatus 0:未开始,1:进行中,2:结束)',
#                 api_type=API_TYPE_COLLECT)
#     def get(self):
#         '''
#         get live show list
#         '''
#         page_no = self.get_int_argument('pn', 1)
#         page_size = self.get_int_argument('pz', 10)
#         hds = self.get_str_argument('hds', '2')
#         live_uinfo = yield CMSApi.query_user(self.current_user_id)
#         if 'user' in live_uinfo.get('data', {}) and \
#                     live_uinfo['data']['user'] is not None:
#             res = yield CMSApi.query_liveshow(live_uinfo['data']['user']['id'],
#                                               page_no, page_size)
#             items = res.get('data', {}).get('items', [])
#             total = res.get('data', {}).get('records', 0)
#             for i in range(len(items)):
#                 show = items[i]
#                 show['liveName'] = '%sTS%s' % (show['id'], show['startDate']/1000)
#                 show['endDate'] = show['dueDate']
#                 show['liveStatus'] = show['status']
#                 if show['status'] == 1:
#                     try:
#                         data = json.loads(show['data'])
#                     except Exception as e:
#                         LOG.error(e)
#                     else:
#                         show['upload_url'] = data['upload_url']
#                         show['playDispUrl'] = data.get(hds)[0].get('play_disp_url','') + '&' + urlencode({'expire':show['startDate']/1000})
#                 else:
#                     show['upload_url'] = ''
#                 del show['status']
#                 del show['data']
#                 del show['owner']
#                 del show['ownerId']
#                 del show['testable']
#                 del show['createDate']
#                 del show['lastUpdate']
#                 del show['dueDate']
#             self.write({'code': 0, 'data': items, 'total': total})
#         else:
#             self.write({'code': 0, 'data': []})

# @handler_define
# class CreateLiveShowHandler(ApiHandler):

#     @auth_required
#     @coroutine
#     @api_define('create live show', '/gpspic/liveshow/create',
#                 params=[
#                     Param('title', True, str, None, '测试直播', '直播标题'),
#                     Param('token', True, str, None, '', '申请认证返回的token'),
#                     Param('userName', True, str, None, '', '登陆用户名'),
#                     Param('testable', False, str, None, '0', '直播用途{1:测试直播}'),
#                     Param('hds', False, str, None, '2', '输出直播流的清晰度'
#                                                         '1：标清 256p 约256kbps; 2：高清, 480p 约550kbps; '
#                                                         '3: 超清 720p 约1200kbps; 4：1080p 约2500kbps'),
#                     Param('bitrate', False, int, None, 500, '采集端编码后上传流的码率，等于hds中清晰度最高的码率，不必精确'),
#                 ],
#                 filters=[], description=u'开始直播(直播状态liveStatus 0:未开始,1:进行中,2:结束)',
#                 api_type=API_TYPE_COLLECT)
#     def get(self):
#         '''
#         create live show
#         '''
#         title = self.get_str_argument('title')
#         token = self.get_str_argument('token')
#         device = self.get_str_argument('_os_')
#         #proto = settings.live_proto.get(device)
#         testable = self.get_str_argument('testable', default='0')
#         uname = self.get_str_argument('userName')
#         hds = self.get_str_argument('hds', '2')
#         bitrate = self.get_int_argument('bitrate', 500)
#         #LOG.error("token=[%s]", token)
#         now = int(time.time())
#         endTime = now + 14 * 86400

#         mode = 1
#         proto = 'rtmp'
#         vhost = 'zb.youku.com'
#         app = 'live2'
#         limit = -1
#         desc = 'CREATE_STREAM'
#         salt = settings.livestream_salt

#         #直播名称，用于构造直播流id；字母或数字，每次调用必须保证liveName不同
#         livename = '%s_%s' % (str(now), random.randint(10000, 99999))

#         text = '&'.join([uname, livename, str(now), str(endTime), str(mode), proto, hds,
#                          str(bitrate), '0', vhost, app, str(limit), salt])
#         text = text.encode('utf-8')

#         LOG.debug('[LIVE CREATE] text => %s', text)
#         try:
#             m = hashlib.md5()
#             m.update(text)
#             key = m.hexdigest()
#         except Exception as e:
#             LOG.error(e)
#             self.write({'code': -1, 'msg': u'生成key失败'})
#             return

#         params = {
#             'user_name': uname.encode('utf-8'),
#             'user_ip': self.get_ip(),
#             'live_name': livename,
#             'mode': mode,
#             'proto': proto,
#             'hds': hds,
#             'bitrate': bitrate,
#             'vhost': vhost,
#             'app': app,
#             'limit': limit,
#             'live_desc': desc,
#             'key': key,
#             'start_time':now,
#             'end_time':endTime,
#             'need_format':'0',
#         }
#         LOG.debug('[LIVE CREATE] params => %s', params)
#         stream_info = yield LiveStreamApi.create_live(params)
#         code = int(stream_info.get('code', -1))

#         if code == 200:
#             # 创建流成功，在DB中创建liveshow记录
#             task = yield CMSApi.create_liveshow(title, token, testable, now)
#             if task.get('code', -1) != 0:
#                 self.write({'code': -1, 'msg': u'创建直播任务失败'})
#                 return
#             showid = task['data']['id']
#             stream_info['stream_name'] = livename
#             stream_str = json.dumps(stream_info)
#             yield CMSApi.update_liveshow(showid, token, **{'data': stream_str, 'status': 1})
#             res = yield CMSApi.create_livestream(showid, token, hds, stream_str)
#             play_disp_url = stream_info.get(hds)[0].get('play_disp_url','')
#             data = {
#                 'liveStatus': 1,
#                 'showId': showid,
#                 'title': title,
#                 'liveName': livename,
#                 'startTime': now * 1000,
#                 'uploadUrl': stream_info.get('upload_url', ''),
#                 'playDispUrl': play_disp_url + '&' + urlencode({'expire':now}),
#             }
#             self.write({'code': 0, 'msg': u'成功', 'result': data})
#         elif code == 503:
#             self.write({'code': -1, 'msg': u'直播名称已使用', 'result': stream_info})
#         else:
#             self.write({'code': -1, 'msg': u'创建流失败', 'result': stream_info})

# @handler_define
# class CreateLiveStreamHandler(ApiHandler):

#     @auth_required
#     @coroutine
#     @api_define('create live stream', '/gpspic/livestream/create',
#                 params=[
#                     Param('showId', True, str, None, '', '直播ID'),
#                     Param('token', True, str, None, '', '用户申请认证返回的token'),
#                     Param('userName', True, str, None, '', '登陆用户名'),
#                     Param('startTime', False, int, None, '', '预设直播开始时间，精确到秒'),
#                     Param('endTime', False, int, None, '', '预设直播终止时间，精确到秒'),
#                     Param('hds', False, str, None, '2', '输出直播流的清晰度，逗号分隔 '
#                                                         '1：标清 256p 约256kbps; 2：高清, 480p 约550kbps; '
#                                                         '3: 超清 720p 约1200kbps; 4：1080p 约2500kbps'),
#                     Param('bitrate', False, int, None, 500, '采集端编码后上传流的码率，等于hds中清晰度最高的码率，不必精确'),
#                 ],
#                 filters=[], description=u'创建一个直播视角(视角状态0:正常，-1:删除)',
#                 api_type=API_TYPE_COLLECT, offline=True)
#     def get(self):
#         '''
#         create live stream
#         '''
#         showid = self.get_str_argument('showId')
#         token = self.get_str_argument('token')
#         uname = self.get_str_argument('userName')
#         stime = self.get_int_argument('startTime', 0)
#         etime = self.get_int_argument('endTime', 0)
#         hds = self.get_str_argument('hds', '2')
#         bitrate = self.get_int_argument('bitrate', 500)
#         #直播模式，1:普通, 2:全景, 3:3D, 11：普通商业, 12：全景商业, 13：3D商业
#         mode = 1
#         #采集端上传流协议, rtmp或者flvoverhttp
#         proto = 'rtmp'
#         #以下两种情况中的任一情况，都需要将need_format设置为1: 
#         #（1）   采集端上传流编码格式不是h.264+aac
#         #（2）   采集端上传流码率> bitrate,需要服务器端压码
#         #建议：采集端上传流尽量满足编码为h.264+aac，码率约等于bitrate，
#         #以避免服务器端进行转码。如果将need_format=1，会导致直播流的延迟增加
#         need_format = 0
#         #业务名
#         vhost = 'zb.youku.com'
#         #直播应用名
#         app = 'live2'
#         #允许观看直播的最大用户数，超过limit的用户会被拒绝服务，-1表示不限制；
#         limit = -1
#         #直播描述
#         desc = 'CREATE STREAM'

#         # 创建流校验key
#         key = 'X5dXjrD^$LQWkVlu'

#         now = int(time.time())
#         if stime == 0:
#             stime = now - 10
#         if etime == 0:
#             etime = stime + 7200
#         if stime >= etime:
#             self.write({'code': '999', 'msg': u'失败', 'result': {'desc': u'预设开始时间大于结束时间'}})
#             return
#         if stime >= now:
#             self.write({'code': '999', 'msg': u'失败', 'result': {'desc': u'预设开始时间大于当前时间'}})
#             return

#         #直播名称，用于构造直播流id；字母或数字，每次调用必须保证liveName不同
#         livename = '%sTS%s' % (showid, str(now))

#         text = '&'.join([uname, livename, str(stime), str(etime), str(mode), proto,
#                          hds, str(bitrate), str(need_format), vhost, app, str(limit), key])
#         LOG.debug('[LIVE CREATE] text => %s', text)
#         try:
#             m = hashlib.md5()
#             m.update(text)
#             key = m.hexdigest()
#         except Exception as e:
#             LOG.error(e)
#             self.write({'code': '999', 'msg': u'失败', 'result': {'desc': u'生成key失败'}})
#             return

#         params = {
#             'user_name': uname,
#             'user_ip': self.get_ip(),
#             'live_name': livename,
#             'start_time': stime,
#             'end_time': etime,
#             'mode': mode,
#             'proto': proto,
#             'hds': hds,
#             'bitrate': bitrate,
#             'need_format': need_format,
#             'vhost': vhost,
#             'app': app,
#             'limit': limit,
#             'live_desc': desc,
#             'key': key,
#         }
#         LOG.debug('[LIVE CREATE] params => %s', params)
#         res = yield LiveStreamApi.create_live(params)
#         code = int(res.get('code', -1))
#         if code == 200:
#             res2 = yield CMSApi.create_livestream(showid, token, hds, livename)
#             data = res2.get('data', {})
#             data['bitrate'] = bitrate
#             data['upload_url'] = res.get('upload_url', '')
#             self.write({'code': '000', 'msg': u'成功', 'result': data})
#         elif code == 503:
#             self.write({'code': '988', 'msg': u'直播名称已使用', 'result': res})
#         else:
#             self.write({'code': '999', 'msg': u'失败', 'result': res})

# @handler_define
# class DestroyLiveStreamHandler(ApiHandler):

#     @auth_required
#     @coroutine
#     @api_define('live stream destroy', '/gpspic/livestream/destroy',
#                 params=[
#                     Param('showId', True, str, None, '', '直播ID'),
#                     Param('liveName', True, str, None, '', '直播名称'),
#                     Param('token', True, str, None, '', '申请认证返回的token'),
#                     Param('pause', True, str, None, '', '暂停'),
#                 ],
#                 filters=[], description=u'停止当前直播(直播状态liveStatus 0:未开始,1:进行中,2:结束)',
#                 api_type=API_TYPE_COLLECT, source_wiki='')
#     def post(self):
#         '''
#         '''
#         showid = self.get_str_argument('showId')
#         livename = self.get_str_argument('liveName')
#         token = self.get_str_argument('token')
#         pause = self.get_str_argument('pause')
#         status =  1 if pause == '1' else 2
        
#         now = int(time.time())
#         app = 'live2'
#         vhost = 'zb.youku.com'

#         params = {
#             'vhost': vhost,
#             'app': app,
#             'live_name': livename,
#         }
#         LOG.debug('[LIVE CANCEL] params => %s', params)

#         #cancell destroy_live 2016/7/14 
#         # res = yield LiveStreamApi.destroy_live(params)
#         # if int(res.get('code', -1)) == 200:
#         #     end_time = datetime.datetime.fromtimestamp(now)
#         #     req = {
#         #         'dueDate': end_time.strftime("%Y-%m-%d %H:%M:%S"),
#         #         'status': 2,
#         #     }
#         #     res2 = yield CMSApi.update_liveshow(showid, token, **req)
#         #     del res['code']
#         #     res['liveStatus'] = res2.get('data', {}).get('status', 0)
#         #     res['endTime'] = res2.get('data', {}).get('dueDate', 0)
#         #     self.write({'code': 0, 'msg': u'成功', 'result': res})
#         # else:
#         #     self.write({'code': -1, 'msg': u'失败', 'result': res})
#         res = {}
#         end_time = datetime.datetime.fromtimestamp(now)
#         req = {
#             'dueDate': end_time.strftime("%Y-%m-%d %H:%M:%S"),
#             'status': status,
#         }
#         res2 = yield CMSApi.update_liveshow(showid, token, **req)
#         res['liveStatus'] = res2.get('data', {}).get('status', 0)
#         res['endTime'] = res2.get('data', {}).get('dueDate', 0)
#         res['desc'] = 'stop encode success'
#         self.write({'code': 0, 'msg': u'成功', 'result': res})

