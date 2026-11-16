import json
S="/private/tmp/claude-501/a5-evidence"
SRC="/Users/bear/Documents/CoWork/bear-textbooks/books/walker-claude/evidence/course-assignment-series/shaders"
def enc(x):
    x=min(max(x,0.0),1.0)
    return 12.92*x if x<=0.0031308 else 1.055*x**(1/2.4)-0.055
def dec(y): return y/12.92 if y<=0.04045 else ((y+0.055)/1.055)**2.4
def b(x): return int(round(enc(x)*255+1e-12))
out={}
# hint predictions
out["hint_prediction"]={str(v):{"x":v/255,"encode_x":enc(v/255),"times255":enc(v/255)*255,"rgb8":round(enc(v/255)*255)} for v in (64,128,192)}
# signal
quiet=[0.40,0.16,0.09]; active=[0.12,0.72,0.52]
def signal_as_written(a, stripe):
    f=0.65 if stripe=="dark" else 1.0
    return [ (q*f)*(1-a)+ac*a for q,ac in zip(quiet,active)]
def signal_linear(a, stripe):
    f=0.65 if stripe=="dark" else 1.0
    return [ (dec(q)*f)*(1-a)+dec(ac)*a for q,ac in zip(quiet,active)]
def clamp8(v): return max(0,min(255,int(round(v*255))))
pred=json.load(open(SRC+"/controlled-predictions.json"))["rows"]
ex=json.load(open(SRC+"/material-native-results.json"))["rows"]
fp=json.load(open(S+"/out/fp/signal_values_forward_plus.json"))["rows"]
cp=json.load(open(S+"/out/compat/signal_values_compatibility.json"))["rows"]
table=[]
for i,a in enumerate([0.0,0.5,1.0,2.0]):
    for j,stripe in enumerate(["dark","light"]):
        p=[r for r in pred if r["activation"]==a and r["stripe"]==stripe][0]["predicted_display_rgb8_compatibility"]
        exm=[r for r in ex if r.get("case")=="signal" and r["set_value"]==a][0]["samples"][j]["rgb8"]
        f=fp[i]["samples"][j]["rgb8"]; c=cp[i]["samples"][j]["rgb8"]
        asw=[clamp8(v) for v in signal_as_written(a,stripe)]
        lin=[int(round(enc(v)*255)) for v in signal_linear(a,stripe)]
        row={"activation":a,"stripe":stripe,"uv_x":[0.15625,0.21875][j],
             "example_prediction":p,"as_written_recomputed":asw,"linear_model_recomputed":lin,
             "example_recorded_compat":exm,"rerun_compat":c,"rerun_forward_plus":f,
             "diff_compat_minus_prediction":[x-y for x,y in zip(c,p)],
             "diff_forward_plus_minus_prediction":[x-y for x,y in zip(f,p)],
             "diff_rerun_compat_minus_example_recorded":[x-y for x,y in zip(c,exm)],
             "diff_forward_plus_minus_linear_model":[x-y for x,y in zip(f,lin)]}
        table.append(row)
out["signal"]=table
json.dump(out,open(S+"/analysis/analysis.json","w"),indent=1)
for r in table:
    print(f'a={r["activation"]:<3} {r["stripe"]:<5} pred={r["example_prediction"]} aswritten={r["as_written_recomputed"]} | compat={r["rerun_compat"]} (ex {r["example_recorded_compat"]}) d={r["diff_compat_minus_prediction"]} | fp={r["rerun_forward_plus"]} d={r["diff_forward_plus_minus_prediction"]} | linmodel={r["linear_model_recomputed"]} fp-lin={r["diff_forward_plus_minus_linear_model"]}')
print(out["hint_prediction"])
