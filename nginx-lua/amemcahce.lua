
local cjson = require "cjson"

-- init memcached
local memcached = require "resty.memcached"
local memc, err = memcached:new()
if not memc then
    ngx.say("failed to instantiate memc: ", err)
    return
end
memc:set_timeout(1000) -- 1 sec

local ok, err = memc:connect("192.168.0.1", 11211)
if not ok then
    ngx.say("failed to connect: ", err)
    return
end

local res, flags, err = memc:get("key")
if err then
    ngx.say("failed to get: ", err)
end

ngx.say(res)
