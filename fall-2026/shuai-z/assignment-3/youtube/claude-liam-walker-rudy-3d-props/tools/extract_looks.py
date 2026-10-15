import json,base64,sys,os
p=sys.argv[1]; out=sys.argv[2]
uses={}
n=0
for line in open(p):
    d=json.loads(line)
    ts=d.get("timestamp","")
    m=d.get("message",{})
    c=m.get("content")
    if not isinstance(c,list): continue
    for x in c:
        if x.get("type")=="tool_use":
            uses[x["id"]]=(x["name"],json.dumps(x["input"])[:160])
        if x.get("type")=="tool_result":
            cc=x.get("content")
            if not isinstance(cc,list): continue
            for y in cc:
                if y.get("type")=="image":
                    n+=1
                    data=base64.b64decode(y["source"]["data"])
                    ext=y["source"].get("media_type","image/png").split("/")[-1]
                    fn=f"{out}/look-{n:03d}.{ext}"
                    open(fn,"wb").write(data)
                    print(fn, ts, uses.get(x["tool_use_id"],("?",""))[0], uses.get(x["tool_use_id"],("?",""))[1])
