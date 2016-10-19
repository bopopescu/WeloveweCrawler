#coding=utf-8
import time

def get_sub_point_str(**kwargs):
    '''
    构造订阅信息的发送参数
    '''
    params = [
        kwargs.get('LogVersion', 1),#日志版本
        kwargs.get('ID', ''),#日志ID
        kwargs.get('userID', ''),#订阅者ID
        kwargs.get('targetUserID', ''),#被订阅用户ID
        kwargs.get('showID', ''),#被订阅节目ID
        kwargs.get('subTime', int(time.time())),#操作时间戳(毫秒),服务器时间戳
        kwargs.get('subType', ''),#操作类型,1=订阅、2=取消订阅
        kwargs.get('favType', ''),#订阅类型,3=节目、6=自频道
        kwargs.get('cookieID', ''),#web端传入cookieID，app端传入GUID  self.get_argument('guid', '')
        kwargs.get('useragent', ),#web／app端传入各自类型的UA self.client.user_agent
        kwargs.get('IP', ''),#操作时的IP ip2long(self.get_ip())
        kwargs.get('deviceID', ''),#1=PC web、2=PC app、3=移动web、4=iPhone app、
                                   #5=iPad app、6=Android phone app、7=Android pad app、
                                   #8=iOS 拍客、9=Android 拍客、10=windowsphone app、11=TV app
        kwargs.get('sourceID', ''),#产品定义各平台收藏用户的操作入口ID
        kwargs.get('url', ''),#操作时的页面信息
        kwargs.get('videoID', ''),#视频id，如果页面为播放页则传入当前播放页的videoID
        kwargs.get('ext', ''),#预留扩展信息
    ]

    return '\t'.join([str(x) for x in params])

def get_comment_log_content(**kwargs):
    '''
    构造评论信息的发送参数
    '''
    params = [
        'tcomment',
        kwargs.get('version', 1),#日志版本号
        kwargs.get('comment_id', ''),#评论ID
        kwargs.get('video_id', ''),#视频ID
        kwargs.get('channel_id', ''),#视频一级分类
        kwargs.get('user_id', ''),#用户ID
        kwargs.get('target_user_id', ''),#第三方用户ID（非虚拟ID）
        kwargs.get('sub_time', int(time.time())),#操作时间戳(毫秒),服务器时间戳
        kwargs.get('sub_type', ''),#操作类型,1=评论、2=回复评论、3=支持评论、4=反对评论
        kwargs.get('reply_cid', ''),#回复／支持／反对的目标ID
        kwargs.get('org_cid', ''),#回复／支持／反对的始祖ID
        kwargs.get('order_id', ''),#该评论在该视频评论列表中的位置
        kwargs.get('is_original', ''),#是否为始祖评论 0=否，1=是
        kwargs.get('status', ''),#评论状态 0=可见，2=先审后发，3=删除，4=屏蔽
        kwargs.get('old_status', ''),#旧的评论状态	0=可见，2=先审后发，3=删除，4=屏蔽
        kwargs.get('content', ''),#评论内容 base64编码
        kwargs.get('cookie_id', ''),#web端传入cookieID，app端传入GUID  self.get_argument('guid', '')
        kwargs.get('ua', ),#web／app端传入各自类型的UA self.client.user_agent
        kwargs.get('ip', ''),#操作时的IP ip2long(self.get_ip())
        kwargs.get('outside', ''),#站内外区分0=站内、1=sina、2=renren、3=tencent、4=qzone
        kwargs.get('device_id', ''),#1=PC web、2=PC app、3=移动web、4=iPhone app、
                                    #5=iPad app、6=Android phone app、7=Android pad app、
                                    #8=iOS 拍客、9=Android 拍客、10=windows phone app、11=TV app
        kwargs.get('source_id', ''),#产品定义各平台收藏用户的操作入口ID
        kwargs.get('url', ''),#操作时的页面信息
        kwargs.get('ext', ''),#预留扩展信息
    ]

    return '\2'.join([str(x) for x in params])

def get_dig_bury_log_content(**kwargs):
    '''
    构造挖埋信息的发送参数
    '''
    params = [
        'wamai',
        kwargs.get('version', 1),#日志版本号
        kwargs.get('id', ''),#日志ID
        kwargs.get('user_id', ''),#用户ID，未登录为0
        kwargs.get('video_id', ''),#视频ID
        kwargs.get('channel_id', ''),#视频一级分类
        kwargs.get('sub_time', int(time.time())),#操作时间戳(毫秒),服务器时间戳
        kwargs.get('sub_type', ''),#操作类型,1=挖、2=埋
        kwargs.get('cookie_id', ''),#web端传入cookieID，app端传入GUID  self.get_argument('guid', '')
        kwargs.get('ua', ''),#web／app端传入各自类型的UA self.client.user_agent
        kwargs.get('ip', ''),#操作时的IP ip2long(self.get_ip())
        kwargs.get('device_id', ''),#1=PC web、2=PC app、3=移动web、4=iPhone app、
                                    #5=iPad app、6=Android phone app、7=Android pad app、
                                    #8=iOS 拍客、9=Android 拍客、10=windows phone app、11=TV app
        kwargs.get('source_id', ''),#产品定义各平台收藏用户的操作入口ID
        kwargs.get('url', ''),#操作时的页面信息
        kwargs.get('ext', ''),#预留扩展信息
    ]

    return '\2'.join([str(x) for x in params])

def get_favor_point_str(**kwargs):
    '''
    构造搜藏信息的发送参数
    '''
    params = [
        kwargs.get('LogVersion', 1),#日志版本
        kwargs.get('ID', ''),#日志ID
        kwargs.get('userID', ''),#2：收藏者ID
        kwargs.get('videoID', ''),#被收藏视频ID
        kwargs.get('playlistID', ''),#被收藏专辑ID
        kwargs.get('showID', ''),#被收藏节目ID（预留）
        kwargs.get('channelId', ''),#视频一级分类
        kwargs.get('playlistChannelId', ''),#专辑一级分类
        kwargs.get('showChannelId', ''),#节目剧集一级分类（预留）
        kwargs.get('subTime', int(time.time())),#操作时间戳(毫秒),服务器时间戳
        kwargs.get('subType', ''),#操作类型,1=收藏、2=取消收藏
        kwargs.get('favType', ''),#收藏类型,1=视频、2=专辑（豆单）
        kwargs.get('cookieID', ''),#web端传入cookieID，app端传入GUID
        kwargs.get('useragent', ''),#web／app端传入各自类型的UA
        kwargs.get('IP', ''),#操作时的IP
        kwargs.get('deviceID', ''),#1=PC web、2=PC app、3=移动web、4=iPhone app、
                                   #5=iPad app、6=Android phone app、7=Android pad app、
                                   #8=iOS 拍客、9=Android 拍客、10=windowsphone app、11=TV app
        kwargs.get('sourceID', ''),#产品定义各平台收藏用户的操作入口ID
        kwargs.get('url', ''),#操作时的页面信息
        kwargs.get('ext', ''),#预留扩展信息
    ]

    return '\t'.join([str(x) for x in params])

