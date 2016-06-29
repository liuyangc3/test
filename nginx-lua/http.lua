local http = require("resty.http")
local client = http:new()
client:set_timeout(200) -- 200ms
local url = "http://www.google.com"
local response, err = client:request_uri(
    url, {method = "GET"})
if not response then
    ngx.say("no response: ", err)
    return
end
ngx.say(response.body)
