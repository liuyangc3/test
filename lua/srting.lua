function string.startwiths(String, Start)
    return string.sub(String, 1, string.len(Start)) == Start
end


s = "hello world"
print(string.startwiths(s, "h"))

true
