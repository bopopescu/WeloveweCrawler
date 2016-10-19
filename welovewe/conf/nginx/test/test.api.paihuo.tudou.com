# test.api.paihuo.tudou.com

upstream paihuo {
   server 127.0.0.1:20000 ;
   #check interval=3000 rise=2 fall=3 timeout=1000 type=http;
   #check_keepalive_requests 100;
   #check_http_send "HEAD /lvs/lvs_head HTTP/1.1\r\nConnection: keep-alive\r\n\r\n";
   #check_http_expect_alive http_2xx http_3xx;
   #keepalive 50;
}

# init lua
lua_code_cache on;

server {
    listen 8008;
    server_name test.api.paihuo.tudou.com;
    index index.html index.htm index.jsp;
    charset utf-8;

    log_subrequest on;

    #set $x_remote_addr $http_x_real_ip;
    set $x_remote_addr $http_client_ip;
    if ($x_remote_addr = "") {
        set $x_remote_addr $remote_addr;
    }

    log_format main '$x_remote_addr "$time_iso8601" $request_method "$uri" "$args" "$request_body" $status $body_bytes_sent $request_time "$http_user_agent"';
    access_log /opt/logs/nginx/access/log _main;

    location ~ /doc {
        # 只允许内网访问
        allow 60.247.104.99; # 办公室的公网IP
        allow 10.10.0.0/16;
        allow 10.5.0.0/16;
        allow 10.5.16.0/22;
        allow 10.10.116.0/24;
        allow 10.155.6.0/24;
        allow 10.155.7.0/24;
        allow 10.155.8.0/24;
        allow 10.155.59.0/24;
        allow 10.155.56.0/24;
        allow 10.155.57.0/24;
        allow 10.155.58.0/24;
        deny all;

        proxy_pass http://paihuo;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~* (/cache_update|/cms/video_list|/cms/vsg_info|/user/permissions)$ {
        # 只允许内网访问
        allow 10.5.0.0/16;
        allow 10.10.0.0/16;
        allow 10.25.0.0/16;
        allow 10.108.0.0/16;
        allow 10.100.0.0/16;
        allow 10.155.0.0/16;
        deny all;

        proxy_pass http://paihuo;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    # H5分享页面使用的接口不进行参数签名的检查
    location ~* /h5/video_list$|/video/goods$|/v2/web/* {

        # 设置H5接口允许跨域
        add_header 'Access-Control-Allow-Origin' '*';
        add_header 'Access-Control-Allow-Credentials' 'true';
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
        add_header 'Access-Control-Allow-Headers' 'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type';

        proxy_pass          http://paihuo;

        proxy_connect_timeout 3;
        proxy_send_timeout 3;
        proxy_read_timeout 3;

        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    # m3u8描述信息接口不进行参数签名的检查
    location ~* /m3u8_info$ {

        proxy_pass          http://paihuo;

        proxy_connect_timeout 3;
        proxy_send_timeout 3;
        proxy_read_timeout 3;

        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~* /cover_update$ {

        # 验证客户端访问权限
        access_by_lua_file conf/lua2/check_pid.lua;

        proxy_pass          http://paihuo;

        # 提高图片上传接口超时时间
        proxy_connect_timeout 6;
        proxy_send_timeout 6;
        proxy_read_timeout 6;

        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location / {

        # 验证客户端访问权限
        access_by_lua_file conf/lua2/check_pid.lua;

        proxy_pass          http://paihuo;

        proxy_connect_timeout 3;
        proxy_send_timeout 3;
        proxy_read_timeout 3;

        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }
}
