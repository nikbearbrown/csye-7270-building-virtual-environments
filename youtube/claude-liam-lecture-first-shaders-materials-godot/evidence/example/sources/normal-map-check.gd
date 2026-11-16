extends RefCounted
static func curl_ratio(img: Image, directx: bool = false, stride: int = 2) -> float:
 var s := -1.0 if directx else 1.0
 var curl_sq := 0.0
 var terms_sq := 0.0
 for v in range(1, img.get_height()-1, stride):
  for u in range(1, img.get_width()-1, stride):
   var t1 := (du(img,u,v+1)-du(img,u,v-1))*0.5
   var t2 := (dv(img,u+1,v,s)-dv(img,u-1,v,s))*0.5
   curl_sq += (t1-t2)*(t1-t2)
   terms_sq += t1*t1+t2*t2
 return curl_sq/maxf(terms_sq,1e-12)
static func normal(img:Image,u:int,v:int)->Vector3:
 var c:=img.get_pixel(u,v)
 return Vector3(c.r,c.g,c.b)*2.0-Vector3.ONE
static func du(img:Image,u:int,v:int)->float:
 var n:=normal(img,u,v)
 return -n.x/maxf(n.z,0.05)
static func dv(img:Image,u:int,v:int,s:float)->float:
 var n:=normal(img,u,v)
 return s*n.y/maxf(n.z,0.05)
