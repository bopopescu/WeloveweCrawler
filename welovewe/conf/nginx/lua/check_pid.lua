local pid = nil
local sig = nil
local timestamp = nil
local enc = nil

local req_method = ngx.var.request_method
local expire_time = 60 * 30

--md5("This is tudou api test pid secret")
local old_secret = "6b72db72a6639e1d5a2488ed485192f6"

--更换秘钥
--md5("php is the best programming language")
local secret = "52bd746c8391b56ca766d6d3757a5abf"

-- Get auth params
if req_method == "GET" then
    pid = ngx.var.arg_pid
    sig = ngx.var.arg__s_
    timestamp = ngx.var.arg__t_
    enc = ngx.var.arg__e_
elseif  req_method == "POST" or req_method == "PUT" or  req_method == "DELETE" then
    ngx.req.read_body()
    local post_args = ngx.req.get_post_args()
    pid = post_args.pid
    sig = post_args._s_
    timestamp = post_args._t_
    enc = post_args._e_
    if not pid then
        pid = ngx.var.arg_pid
    end
    if not sig then
        sig=ngx.var.arg__s_
    end
    if not timestamp then
        timestamp = ngx.var.arg__t_
    end
    if not enc then
        enc = ngx.var.arg__e_
    end
else
    ngx.exit(ngx.HTTP_FORBIDDEN)
end

-- Pid check
if not pid or not timestamp or not sig then
    ngx.exit(ngx.HTTP_FORBIDDEN)
end

-- hack for test & debug
if timestamp == "0" and sig == "x" then
    return
end

-- Deal expired request
if ngx.now() - timestamp < -expire_time or ngx.now() - timestamp >= expire_time then
    ngx.status = ngx.HTTP_GONE
    local _now = ngx.now()
    ngx.header.server_time = _now
    ngx.say(_now)
    ngx.exit(ngx.HTTP_OK)
end

-- Generate server sig
local token_string = req_method .. ":" .. ngx.var.uri .. ":" .. timestamp .. ":"  .. secret
local token = ""

local old_token_string = req_method .. ":" .. ngx.var.uri .. ":" .. timestamp .. ":"  .. old_secret
local old_token = ""

if enc == "sha1" then
    token = ngx.sha1_bin(token_string)
    old_token = ngx.sha1_bin(old_token_string)
else
    token = ngx.md5(token_string)
    old_token = ngx.md5(old_token_string)
end

--ngx.log(ngx.ERR, "------------" .. token_string .. "---------------" .. token )

-- Compare sever genned sig(var token) with request sig(request param sig)
if token ~= sig and old_token ~= sig then
    ngx.exit(ngx.HTTP_FORBIDDEN)
else
    return
end

