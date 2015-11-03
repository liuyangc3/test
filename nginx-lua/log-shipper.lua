-- JSON log foramt
-- push to redis

-- use in log_by_lua

lua_package_path "/usr/local/openresty/lualib/?.lua;;";
local redis = require "resty.redis"
local red = redis:new()
red:set_timeout(0)
local ok, err = red:connect("172.16.200.98", 6379)
        
function handler(premature, key, logs)
  if err then
      ngx.log(ngx.WARN, err)
      return
  end
  
  local res, err = red:lpush(key, logs)
  if not res then
      ngx.log(ngx.WARN, err)
      return
        end
end

# log_by_lua

cjson = require "cjson"
local tbl = {
    "time": string.gsub(ngx.var.time_iso8601, "(.-)T([%d:]+)%+.*", "%1 %2"), -- 去掉 T 字母
    
    -- log ip
    "client": ngx.var.remote_addr,
    "server": ngx.var.server_addr,
    "x_forwarded_for": ngx.var.http_x_forwarded_for,
    
    -- http req
    "domain": ngx.var.host,
    "method": ngx.var.request_method,
    "uri": ngx.var.uri,
    
    -- http resp
    "status": ngx.var.status,
    "bytes": ngx.var.body_bytes_sent,
    
    -- proxy backend
    "upstream_addr": ngx.var.upstream_addr,
    "upstream_status": ngx.var.upstream_status,
    "upstream_response_time": ngx.var.upstream_response_time
}

-- ngx lua can not use cosocket in log_by_lua
-- use ngx.timer instead of directly push to redis
ngx.timer.at(0, handler, ngx.var.host, cjson.encode(tbl))
