import sys, re, html, subprocess
url=sys.argv[1]
raw=subprocess.run(['curl','-sL',url],capture_output=True).stdout.decode('utf-8','replace')
m=re.search(r"<article[^>]*>(.*?)</article>", raw, re.S) or re.search(r'<main.*?>(.*?)</main>', raw, re.S)
body=m.group(1) if m else raw
body=re.sub(r'<(script|style).*?</\1>','',body,flags=re.S)
body=re.sub(r'<br\s*/?>|</p>|</li>|</dt>|</dd>|</h\d>|</tr>','\n',body)
t=html.unescape(re.sub(r'<[^>]+>','',body))
t=re.sub(r'\n\s*\n+','\n',t)
print(t)
