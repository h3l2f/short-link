from flask import Flask,render_template,request,redirect
import hashlib
import json
import subprocess
app = Flask(__name__,template_folder='templates')

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



@app.route("/")
def index():
    p = request.args.get('p')
    pwd = request.args.get("pass")
    with open("link.json","r") as f:
        d = json.load(f)
    if p == None:
        return f"<meta name='viewport' content='width=device-width'>Not found<br>Using {request.url_root}?p=(SCode)&pass=(password if necessary)"
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
const p = getParameterByName('p');
var pass = document.getElementById('checkpass').value;
if (pass == "") {alert("Please enter the correct password!")} else {
window.location = '/?p='+p+'&pass='+pass;
}
}
</script>
"""

@app.route('/all-link')
def run_script():
    result = subprocess.run(['python', 'get.py'], capture_output=True, text=True)
    output = result.stdout
    return f"<meta name='viewport' content='width=device-width'>{output}"

@app.route("/generate")
def gen():
    return render_template("generate.html")

@app.route('/gencode', methods=['POST'])
def gencode():
    link = request.form['link']
    rscode = request.form['rscode']
    p = request.form["spasswd"]
    scode = command(link,rscode,p)
    with open("link.json",'r') as f:
        d = json.load(f)
    pwd = d["link"][scode]["pass"]
    return f"<meta name='viewport' content='width=device-width'>Please Wait<br><script>localStorage.setItem('sc', '{scode}');localStorage.setItem('p','{pwd}');window.location = '/scode' </script>"

@app.route('/scode')
def getscode():
    return '<meta name="viewport" content="width=device-width"><span id="scode">Null</span> <script>s = document.getElementById("scode");var scode =localStorage.getItem("sc");if (scode == "Scode is not available,try again with another Scode!") {s.textContent = scode} else {s.textContent = "Your Scode is: "+scode+" and password is " + localStorage.getItem("p")} </script>'

if __name__ == '__main__':
    app.run(host="127.0.0.1",port="5000",debug=True)
