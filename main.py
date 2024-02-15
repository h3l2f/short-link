from flask import Flask,render_template,request,redirect
import hashlib
import json
import subprocess
app = Flask(__name__,template_folder='templates')

nmchr="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

def command(p,rscode,spasswd):
    cm = ["python","slink.py","-l",f"{p}"]
    if rscode == "":
        pass
    else:
        cm.append("-rsc")
        cm.append(rscode)
    if spasswd == "":
        pass
    else:
        cm.append("-p")
        cm.append(spasswd)
    add = subprocess.run(cm, capture_output=True,text=True)
    scode = add.stdout.strip()
    print(cm)
    return scode

@app.errorhandler(404)
def not_found(e):
    p = request.path
    p = p.replace("/","")
    pwd = request.args.get("pass")
    with open("link.json","r") as f:
        d = json.load(f)
    if p == "":
        return f"<meta name='viewport' content='width=device-width'>Not found<br>Use {request.url_root}(SCode)<br>Or use can go to <a href='/manage/generate'>Generate page</a> to get a slink for yourself."
    else:
        try:
            n = d["link"][p]
        except KeyError:
            return "<meta name='viewport' content='width=device-width'>SCode Not Found"
        else:
            if d["link"][p]["pass"] == "":
                return redirect(d["link"][p]["url"],code=302)
            else:
                if pwd == d['link'][p]["pass"]:
                    return redirect(d["link"][p]["url"],code=302)
                else:
                    return """
<!DOCTYPE html>
<html>
<head>
<meta name='viewport' content='width=device-width'>
<title>Scode is protected by password</title>
</head>
<body>
<style>
.hh {
    line-height: 0.1;
    text-align: center;
}
body {
line-height: 0.01
}
</style>
<h2 class='hh'>Scode is protected by password</h2><br><h4 class='hh'>Please enter the correct password to continue</h4><br>
<input type='password' id='checkpass' placeholder='Enter the correct password'>
<input type='checkbox' id='pw' onclick='shpw()'>Show Password
<br><button onclick='check()'>Check</button>
<script>
function getParameterByName(name) {
      const urlParams = new URLSearchParams(window.location.search);
      return urlParams.get(name);
    }

function shpw() {
    var x = document.getElementById('checkpass');
    if (x.type === 'password') {
      x.type = 'text';
    } else {
      x.type = 'password';
    }
  };

function check() {
const p = window.location.pathname;
var pass = document.getElementById('checkpass').value;
if (pass == "") {alert("Please enter the correct password!")} else {
window.location = p+'?pass='+pass;
}
}
</script>
"""

@app.route('/manage/all-link')
def run_script():
    result = subprocess.run(['python', 'get.py'], capture_output=True, text=True)
    output = result.stdout
    return f"<meta name='viewport' content='width=device-width'>{output}"

@app.route("/manage/generate")
def gen():
    return render_template("generate.html")

@app.route('/manage/gencode', methods=['POST'])
def gencode():
    link = request.form['link']
    rscode = request.form['rscode']
    p = request.form["spasswd"]
    if any(chr not in nmchr for chr in rscode):
        scode = "Incl spt"
        pwd = ""
        return f"<meta name='viewport' content='width=device-width'>Please Wait<br><script>localStorage.setItem('sc', '{scode}');localStorage.setItem('p','{pwd}');window.location = '/manage/scode' </script>"
    else:
        scode = command(link,rscode,p)
        with open("link.json",'r') as f:
            d = json.load(f)
        if scode == "Scode is not available,try again with another Scode!":
            pwd = ""
        else:
            pwd = d["link"][scode]["pass"]
        return f"<meta name='viewport' content='width=device-width'>Please Wait<br><script>localStorage.setItem('sc', '{scode}');localStorage.setItem('p','{pwd}');window.location = '/manage/scode' </script>"

@app.route('/manage/scode')
def getscode():
    return '''
<meta name="viewport" content="width=device-width">
<span id="scode">Null</span> <span id="passwd"></span>
<script>
s = document.getElementById("scode");
var scode =localStorage.getItem("sc");
var pass = localStorage.getItem("p");
if (scode == "Scode is not available,try again with another Scode!") {
    s.textContent = scode
} else {if (scode == "Incl spt") {s.textContent="Sorry,Scode cannot include spectial character!"} else {
    var s1 = document.createElement("b");
    s1.textContent= scode;
    s.textContent = "Your Scode is: ";
    s1.setAttribute("style","color : red;");
    s.appendChild(s1);
}};
if (pass=="") {} else {
    var show_pass = document.getElementById("passwd");
    show_pass.textContent = "and your password is: ";
    s2 = document.createElement("b");
    s2.textContent = pass;
    s2.setAttribute("style","color : blue;");
    show_pass.appendChild(s2);
};
</script>'''

if __name__ == '__main__':
    app.run(host="127.0.0.1",port="5000",debug=True)
