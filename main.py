from flask import Flask,render_template,request,redirect
import json
import subprocess
app = Flask(__name__,template_folder='templates')

@app.route("/")
def index():
    p = request.args.get('p')
    with open("link.json","r") as f:
        d = json.load(f)
    if p == None:
        return f"<meta name='viewport' content='width=device-width'>Not found<br>Using {request.url_root}?p=(SCode)"
    else:
        try:
            n = d["link"][p]
        except KeyError:
            return "<meta name='viewport' content='width=device-width'>SCode Not Found"
        else:
            return redirect(d["link"][p],code=302)
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
    if rscode == "":
        add = subprocess.run(['python','slink.py','-l',f'{link}'], capture_output=True, text=True)
        scode = add.stdout.strip()
        scode = f'"{scode}"'
        return f"<meta name='viewport' content='width=device-width'>Please Wait<br><script>localStorage.setItem('sc', {scode});window.location = '/scode' </script>"
    else:
        add = subprocess.run(['python','slink.py','-l',f'{link}','-rsc',f'{rscode}'], capture_output=True,text=True)
        scode = add.stdout.strip()
        scode = f'"{scode}"'
        return f"<meta name='viewport' content='width=device-width'>Please Wait<br><script>localStorage.setItem('sc', {scode});window.location = '/scode' </script>"

@app.route('/scode')
def getscode():
    return '<meta name="viewport" content="width=device-width"><span id="scode">Null</span> <script>s = document.getElementById("scode");var scode =localStorage.getItem("sc");if (scode == "Scode is not available,try again with another Scode!") {s.textContent = scode} else {s.textContent = "Your Scode is: "+scode} </script>'

if __name__ == '__main__':
    app.run(host="127.0.0.1",port="5000",debug=True)
