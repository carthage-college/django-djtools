import django
django.setup()
uname='smitchell'
import urllib2, json, sys
root = "https://www.carthage.edu"
earl = "{}/live/json/profiles/search/{}/".format(root,uname)
response =  urllib2.urlopen(earl)
data = json.loads(response.read())

if len(data) > 0:
    email = "{}@carthage.edu".format(uname)
    for p in data:
        if p.get("profiles_37") == email \
        or p.get("profiles_45") == email \
        or p.get("profiles_149") == email \
        or p.get("profiles_80") == email:
            earl = "{}/live/profiles/{}@JSON".format(root,p["id"])
            response =  urllib2.urlopen(earl)
            p = json.loads(response.read())
            if p.get("parent"):
                earl = "{}/live/profiles/{}@JSON".format(
                    root,p["parent"]
                )
                response =  urllib2.urlopen(earl)
                p = json.loads(response.read())
            if p.get("thumb"):
                listz = p["thumb"].split('/')
                listz[8] = '145'
                listz[0] = 'https:'
                new_listz = listz[0:9]
                new_listz.append(listz[-1])
                p["thumbnail"] = '/'.join(new_listz)
            prof = p

print prof

