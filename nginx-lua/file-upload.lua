package.path='/usr/local/openresty/lualib/resty/?.lua'

local upload = require "upload"

local CHUNK = 4096

local file
local filename
local fileExtensionName


-- fuctions
function getFilename(res)
    local filename = ngx.re.match(res,'(.+)filename="(.+)"(.*)')
    if filename then
        return filename[2]
    end
end

function getFileExtensionName(str)
    return str:match(".+%.(%w+)$")
end

-- ip 限制
if ngx.var.remote_addr ~= "61.49.246.150" then
    ngx.exit(ngx.HTTP_FORBIDDEN)
end

-- url query arg
local foo = ngx.var.arg_foo
if not version then
    ngx.say('can not get arg foo')
    return
end

local form, err = upload:new(CHUNK)
if not form then
    ngx.log(ngx.ERR, "failed to new upload: ", err)
    ngx.exit(500)
end

form:set_timeout(0)

while true do
    local typ, res, err = form:read()

    if not typ then
        ngx.say("failed to read form: ", err)
        return
    end

    if typ == "header" then
        if res[1] ~= "Content-Type" then
            filename = getFilename(res[2])
            if not filename then
                ngx.say("failed to get file name")
                return
            end
            fileExtensionName = getFileExtensionName(filename)
            if not fileExtensionName then
                ngx.say("failed to get file extension name")
                return
            end
            file = io.open(filename, "w+")
            if not file then
               ngx.say("failed to open file ", filename)
               return
            end
        end

    elseif typ == "body" then
        file:write(res)

    elseif typ == "part_end" then
        if file then  
            file:close()  
            file = nil  
            ngx.say("file upload success")  
        end


    elseif typ == "eof" then
        break
    end
end
