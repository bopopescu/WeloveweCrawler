#encoding=utf-8

def update_tornado_settings(settings):
    settings.update({
        'debug': False,
        'cookie_secret': 'd4a256d61d2b934a2c4abc5267fbfbf8',
    })

def update_global_settings(settings):
    settings.update({
        # general settings
        'DEBUG': False,
        'SYNCHRONOUS': False,
        'GLOBAL_TIMEOUT': 2,
        'AES_KEY': '094b2a34e812a4282f25c7ca1987789f',
        'AES_PADDING': ' ',
        'KEY_SETTINGS': {
            "paihuo_key": "83bed8eb5943bb57", #拍货项目独立的key
            "iphone_key": "224998dc8b40887e",
            "ipad_key": "8ee649cc5592472f",
            "aphone_key": "ef7d8b3fff3e3be7",
            "apad_key": "c72b5ee6e024f39c",
            "wphone_key": "0728254aef5d83b3",
        },
        'connect_timeout': 1.2,
        'request_timeout': 2.8,
        'dm_uid_secret': '348eceac0c6d4a9da5e1793119672fb7',
        # constant settings
        'channel_ids': {88: u'玩货', 89: u'拍货'},
        # cookie config
        "expires": None,
        'expires_days': 30,
        'server_domain': '.gpspic.zb.tudou.com',
        # host config
        'tudou_auth_host': 'login.jj.tudou.com',
        'tudou_uis_host': 'www.tudou.com',
        'livestream_host': 'm.live.tudou.com',
        'livestream_salt': 'X5dXjrD^$LQWkVlu',
        'livecollect_cms_host': 'sharedapi.gpspic.zb.jj.tudou.com',
        'live_proto':{'iPhone':'rtmp','Android':'flvoverhttp'},
        'play_private_token':'zbtest#321',
        'client_private_token':'8ICiSXC*VUNGhFy*cTPc',
    })

