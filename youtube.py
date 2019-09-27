import urllib.request
import urllib.parse
import re
import webbrowser as wb

query_string = urllib.parse.urlencode({"search_query" : input()})
html_cont = urllib.request.urlopen("http://www.youtube.com/results?"+query_string)
search_res = re.findall(r'href=\"\/watch\?v=(.{11})', html_cont.read().decode())
print("http://www.youtube.com/watch?v=" + search_res[0])
wb.open_new("http://www.youtube.com/watch?v={}".format(search_res[0]))
