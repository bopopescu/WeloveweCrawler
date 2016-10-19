upstream gpspic {
   server 127.0.0.1:20000 fail_timeout=0;
   server 127.0.0.1:20001 fail_timeout=0;
   server 127.0.0.1:20002 fail_timeout=0;
   server 127.0.0.1:20003 fail_timeout=0;
   server 127.0.0.1:20004 fail_timeout=0;
   server 127.0.0.1:20005 fail_timeout=0;
   server 127.0.0.1:20006 fail_timeout=0;
   server 127.0.0.1:20007 fail_timeout=0;
}

# init lua
#lua_code_cache on;

server {
    listen 8080;
    server_name gpspic.zb.tudou.com;
    index index.html index.htm index.jsp;
    charset utf-8;

    #set $x_remote_addr $http_x_real_ip;
    set $x_remote_addr $http_client_ip;
    if ($x_remote_addr = "") {
        set $x_remote_addr $remote_addr;
    }

    log_format main '$x_remote_addr "$time_iso8601" $request_method "$uri" "$args" "$request_body" $status $body_bytes_sent $request_time "$http_user_agent"';
    access_log /opt/logs/nginx/access/log main;

    location = /favicon.ico {
        try_files /favicon.ico =204;
        access_log off;
    }
 
    #################################################
    #                   Robots Module                #
    #################################################
    location ~ /robots.txt {
        default_type text/plain;
        alias /opt/app/python/payment_proxy/conf/nginx/robots.txt;
    }

    #################################################
    #                   Proxy Module                #
    #################################################

    location / {

        # 验证客户端访问权限
        #access_by_lua_file conf/lua/check_pid.lua;

        proxy_pass          http://gpspic;

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
