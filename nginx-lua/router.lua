-- 根据 user-agent 做转发规则

local agent = ngx.var.http_user_agent
if string.match(agent, "itunesstored/%d%.%d.+iOS/9%.%d.+") or string.match(agent, ".+OS%s9_.+Version/9%.%d.+") then
    local res = ngx.location.capture("/xz/ZNConnectIOS9.plist")
    if res.status == 200 then
        ngx.print(res.body)
    end
else
    -- IOS before 9
    local res = ngx.location.capture("/xz/ZNConnect.plist")
    if res.status == 200 then
        ngx.print(res.body)
    end
end
