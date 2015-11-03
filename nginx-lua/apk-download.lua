-- 自动获取智农通非灰度的版本号
-- 先从memcached取
-- 如果失败调用chat.nxin.com的接口

local appName = "zhinongtong"
local cjson = require "cjson"

-- init memcached

local memcached = require "resty.memcached"
local memc, err = memcached:new()
if not memc then
    ngx.say("failed to instantiate memc: ", err)
    return
end
memc:set_timeout(1000) -- 1 sec
local ok, err = memc:connect("172.16.200.98", 11211)
if not ok then
    ngx.say("failed to connect: ", err)
    return
end   

-- get version from memcached

-- oatongWebcacheVeraionNum_10 andriod
-- oatongWebcacheVeraionNum_00 ios
local res, flags, err = memc:get("oatongWebcacheVeraionNum_10")
if not res then

    -- get version from chat.nxin.com
    
    local http = require("resty.http")
    local httpc = http:new()
    httpc:set_timeout(200) -- 200ms
    local url = "http://chat.nxin.com/api/user/getVersionNum.action?phoneType=0&isTest=0"
    -- phoneType 0:android 1:ios 
    -- isTest 0:正式版本 1:灰度版本
    local response, err = httpc:request_uri(url, {method = "GET"})
    if not response then
        ngx.say("failed to call chat api ", err)
        return
    end
    res = response.body
end

version = cjson.decode(res)["versionNum"]            
local apk = "/xz/".. appName .. version .. ".apk"
ngx.redirect(apk)
