from app import app
from flask import render_template, redirect, url_for

@app.route('/')
def home():
    return redirect(url_for('ig.posts'))
    names = ['Shoha', "Dylan", "Christopher", "Alex", "Blair"]

    
    return render_template('index.html', my_list=names)



@app.route('/about')
def iCanNameThisAnything():
    return render_template('about.html')




@app.route('/api/v2/pokemon/')
def signMeUp():
    
    return {'hi' : "there"}

