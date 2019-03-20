from flask import Flask, render_template, request,url_for,redirect,session,flash
from werkzeug.utils import secure_filename
import dbconnection as db
import os
import pageinsight
import insta as ins
import csv
import embedreports as em
app = Flask(__name__, static_url_path='/static')
app.secret_key = '0192824ksjfss'
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route("/")
@app.route("/index")
def index():
    if session.get('image') is None and session.get('username') is None:
        return render_template('index.html',image = '',username = '')
    else:    
        return render_template('index.html',image = session['image'],username = session['username'])

@app.route("/signin")
def signin():
    return render_template('examples/sign-in.html')

@app.route("/sign-inre")
def signin_edirect():
    return redirect(url_for('signin'))

@app.route("/signup")
def signup():
    return render_template('examples/sign-up.html')

@app.route("/sign-upre")
def signup_edirect():
    return redirect(url_for('signup'))


@app.route("/mainpage")
def mainpage():
    return ''

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "POST":
        con = db.con()
        cursor = con.cursor()
        tsql = "INSERT INTO Users (name, email, password, type) VALUES (?,?,?,?);"
        name = request.form["fname"]
        email = request.form["email"]
        password = request.form["password"]
        utype = "user"
        image = "static/images/nopict.png"
        with cursor.execute(tsql,name,email,password,utype,image):
            return redirect(url_for('signin'))

@app.route("/login",methods=["GET","POST"])
def login():
    error = ''
    try:
        if request.method == "POST":
            con = db.con()
            cursor = con.cursor()
            email = request.form["email"]
            session['username'] = email
            password = request.form["password"]
            tsql = "SELECT email, password, image FROM Users where email=? and password=?;"
            with cursor.execute(tsql,email,password):
                row = cursor.fetchone()
                session['image'] = row[2]
                if row is not None:
                    return render_template('index.html',image = session['image'],username = session['username'])
                else:
                    error = 'Invalid credentials' 
                    return render_template("examples/sign-in.html",error = error)
    except:
            return render_template("examples/sign-in.html", error = error) 
@app.route('/logout')
def logout():
   session.pop('username', None)
   session.pop('image', None)
   return render_template('index.html')   

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload',methods=["GET","POST"])
def upload_file():
    if request.method == 'POST':
       if 'files' not in request.files:
            flash('No file part')
            return render_template('index.html',image = session['image'],username= session['username'])
       f = request.files['files']
       if f.filename == '':
            flash('No file selected')
            return render_template('index.html',image = session['image'],username= session['username'])
       if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            con = db.con()
            cursor = con.cursor()
            tsql = "UPDATE Users SET image = ? WHERE email = ?"
            with cursor.execute(tsql,'static/images/'+f.filename,session['username']):
                session['image'] = 'static/images/'+f.filename
                return render_template('index.html',image = session['image'],username= session['username'])
    return render_template('index.html',image = session['image'],username= session['username'])

@app.route('/facebook')
def get_facebook():
    if session.get('username') is None:
        return render_template('index.html',image = '',username = '')
    else:
        return render_template('forms/facebook.html',image = session['image'],username= session['username'], token = '')
    

@app.route('/instagram')
def get_insta():
    if session.get('username') is None:
        return render_template('index.html',image = '',username = '')
    else:
        return render_template('forms/instagram.html',image = session['image'],username= session['username'],token = '')
    
@app.route('/twitter')
def get_twit():
    if session.get('username') is None:
        return render_template('index.html',image = '',username = '')
    else:
        return render_template('forms/twitter.html',image = session['image'],username= session['username'],token = '')

@app.route('/generate',methods=["GET","POST"])
def get_token():
    if request.method == "POST":
        token = pageinsight.get_fb_token(request.form["stoken"])
        return render_template('forms/facebook.html',image = session['image'],username= session['username'],token = token)

@app.route('/fbscrap')
def get_fbdata():
    token = request.args.get("stoken1")
    res = pageinsight.get_fb_data(token)
    return render_template('forms/facebook.html',image = session['image'],username= session['username'],token = res)

@app.route('/instareport')
def get_instareport():
    group_id = '4f445ef7-7251-4c99-8b3c-d8a42e08788b'
    report_id = 'f7b13239-27b9-4feb-ab6c-1248091364a4'
    accesstoken = em.get_access_token()
    embedtoken = em.get_embed_token(accesstoken,group_id,report_id)
    embed_url = 'https://app.powerbi.com/reportEmbed?reportId=' + report_id + '&groupId=' + group_id
    return render_template('forms/reportstemplate.html',image = session['image'],username= session['username'],token = '',embedtoken = embedtoken,id = report_id,embedurl = embed_url)

@app.route('/createinsta')
def create_instareport():
    group_id = '4f445ef7-7251-4c99-8b3c-d8a42e08788b'
    dataset_id = 'b50b2585-7a3b-47ee-b278-52853c4c7cd3'
    accesstoken = em.get_access_token()
    print(accesstoken)
    embedtoken = em.get_datasetkey(accesstoken,group_id,dataset_id)
    print(embedtoken)
    return render_template('forms/reportstemplate.html',image = session['image'],username= session['username'],token = '',embedtoken = embedtoken, id = dataset_id,embedurl = 'https://embedded.powerbi.com/reportEmbed'+group_id)

@app.route('/instascrap')
def get_instadata():
    link = request.args.get("instalink")
    k = ins.InstagramScraper()
    results = k.profile_page_recent_posts(link)
    #profile=k.profile_page_metrics(link)
    Imagecolumns = ['Typename','Accessibility_Caption','Comments_disabled_status','dimension_height','dimension_width','url','Likes_count','Media_preview_likes_count','edge_media_to_caption','Media_preview_comments_count','Gating_info','id','is_video','location','media_preview','owner_id','owner_name','shortcode','timestamp']
    Videocolumns = ['Typename','Comments_disabled_status','dimension_height','dimension_width','url','Likes_count','Media_preview_likes_count','Media_preview_caption','Media_preview_comments_count','Gating_info','id','is_video','location','media_preview','owner_id','owner_name','shortcode','timestamp']
    headersimage = ['__typename','accessibility_caption','comments_disabled','dimensions','display_url','edge_liked_by','edge_media_preview_like','edge_media_to_caption','edge_media_to_comment','gating_info','id','is_video','location','media_preview','owner','shortcode','taken_at_timestamp']
    headersvideo = ['__typename','comments_disabled','dimensions','display_url','edge_liked_by','edge_media_preview_like','edge_media_to_caption','edge_media_to_comment','gating_info','id','is_video','location','media_preview','owner','shortcode','taken_at_timestamp']
    dimsub = {'height','width'}
    likedsub = {'count'}
    ownersub = {'id','username'}
    imagedata = []
    videodata = []
    for i in range(12):
         imagearr = []
         videoarr = []
         if results[i]['__typename'] == 'GraphImage':
            for h in headersimage:
                if h == 'dimensions':
                    for d in dimsub:
                        imagearr.append(results[i][h][d])
                elif h == 'edge_liked_by':
                    for l in likedsub:
                        imagearr.append(results[i][h][l])
                elif h == 'edge_media_preview_like':
                    for l in likedsub:
                        imagearr.append(results[i][h][l])
                elif h == 'edge_media_to_caption':
                    if not results[i][h]['edges']:
                        imagearr.append(None)
                    else:
                        imagearr.append(results[i][h]['edges'][0])
                    
                elif h == 'edge_media_to_comment':
                    for l in likedsub:
                        imagearr.append(results[i][h][l])
                elif h == 'owner':
                    for o in ownersub:
                        imagearr.append(results[i][h][o])
                else:
                    imagearr.append(results[i][h])
            imagedata.append(imagearr)
         elif results[i]['__typename'] == 'GraphVideo':
                for h in headersvideo:
                    if h == 'dimensions':
                        for d in dimsub:
                            videoarr.append(results[i][h][d])
                    elif h == 'edge_liked_by':
                        for l in likedsub:
                            videoarr.append(results[i][h][l])
                    elif h == 'edge_media_preview_like':
                        for l in likedsub:
                            videoarr.append(results[i][h][l])
                    elif h == 'edge_media_to_caption':
                        if not results[i][h]['edges']:
                            videoarr.append(None)
                        else:
                            videoarr.append(results[i][h]['edges'][0])
                    
                    elif h == 'edge_media_to_comment':
                        for l in likedsub:
                            videoarr.append(results[i][h][l])
                    elif h == 'owner':
                        for o in ownersub:
                            videoarr.append(results[i][h][o])
                    else:
                        videoarr.append(results[i][h])
                videodata.append(videoarr)   
    writefile('RecentImagePost.csv',Imagecolumns,imagedata)
    writefile('RecentVideoPost.csv',Videocolumns,videodata)
    return render_template('forms/instagram.html',image = session['image'],username= session['username'],token = '')

def writefile(filename,header,data):
    append_write = 'w'
    myFile = open(filename, append_write, newline='', encoding="utf-8")
    with myFile:
        writer = csv.writer(myFile)
        writer.writerow(header)
        writer.writerows(data)
    myFile.close()
        

if __name__ == '__main__':
    app.run(debug=True)