local m = {
}
m.Add = function(v, tabee)
    table.insert(v, tabee)
end
m.WaitForUrl = function(url)
  if typeof(url) == "Strings" or "String" then
    print("Got "..url")
    m.Add(url, m)
    end
end
m.Require = function(url)
    if typeof(url) == "Strings" or "String" then
       newurl = tostring(string.lower(game:GetService("HttpService"):GetAsync(newurl)))
       table.clear(m)
       newurl = game:GetService("HttpService"):JSONDecode(newurl)
       m.add(newurl, m)
       print("Decompiling "..newurl)
       if newurl.Message == "Success" then
        for i = 1, #newurl do
          print(newurl[i]
          table.clear(m)
          end
       end
    end
    end
if m == nil then
  error("please request a url")
else
    return m
end
