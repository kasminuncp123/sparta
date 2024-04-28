from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime

# Connect MongoDb
client = MongoClient('mongodb://kasmin123:kasmin123@ac-xcdbald-shard-00-00.zacdl7x.mongodb.net:27017,ac-xcdbald-shard-00-01.zacdl7x.mongodb.net:27017,ac-xcdbald-shard-00-02.zacdl7x.mongodb.net:27017/?ssl=true&replicaSet=atlas-wjm5br-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0')

db = client.dbdiary

app=Flask(__name__)
 
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({},{'_id':False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]
    
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    file=request.files["file_give"]
    extension = file.filename.split('.')[-1]
    filename =  f'static/file-{mytime}.{extension}'
    

    profile=request.files["profil_give"]
    extension = profile.filename.split('.')[-1]
    profilname =  f'static/pro-{mytime}.{extension}'
    

    # Validasi
    if  not title_receive or not content_receive :
        return jsonify({'error': 'Harap lengkapi data!'})
    
    file.save(filename)

    profile.save(profilname)

    doc = {
        'file': filename,
        'profil':profilname,
        'title':title_receive,
        'content':content_receive
    }
    db.diary.insert_one(doc)
    return jsonify({'msg':'Upload complete!'})
 
if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug= True)