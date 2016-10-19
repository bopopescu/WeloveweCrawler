# local.api.paihuo.tudou.com

upstream paihuo {
   server 127.0.0.1:8080 ;
}

# init lua
#lua_code_cache on;

server {
    listen 80;
    listen 443 ssl;
    server_name 10.5.28.67;
    index index.html index.htm index.jsp;
    charset utf-8;

    # enable SSL
    ssl_certificate /home/ffyao/workspace/paihuo_api/paihuo_api/test.crt;
    ssl_certificate_key /home/ffyao/workspace/paihuo_api/paihuo_api/test.key;

    #log_subrequest on;

    #set $x_remote_addr $http_x_real_ip;
    set $x_remote_addr $http_client_ip;
    if ($x_remote_addr = "") {
        set $x_remote_addr $remote_addr;
    }

    #log_format main '$x_remote_addr "$time_iso8601" $request_method "$uri" "$args" "$request_body" $status $body_bytes_sent $request_time "$http_user_agent"';
    #access_log /opt/logs/nginx/access/log main;

    location ~ /doc {
        # 只允许内网访问
        allow 60.247.104.99; # 办公室的公网IP
        allow 10.10.0.0/16;
        allow 10.5.0.0/16;
        allow 10.10.116.0/24;
        allow 10.155.6.0/24;
        allow 10.155.7.0/24;
        allow 10.155.8.0/24;
        allow 10.155.59.0/24;
        allow 10.155.56.0/24;
        allow 10.155.57.0/24;
        allow 10.155.58.0/24;
        #deny all;

        proxy_pass http://paihuo;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~* /cover_update$ {

        # 验证客户端访问权限
        #access_by_lua_file conf/lua/check_pid.lua;

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

    location = /v1/statis/vv {
        #rewrite  cn.bing.com redirect;
        proxy_pass http://paihuo/openapi/statis/vv;
    }

    location / {

        # 验证客户端访问权限
        #access_by_lua_file conf/lua/check_pid.lua;

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
