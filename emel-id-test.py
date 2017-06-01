#!/usr/bin/python

from flask import Flask, render_template, flash, url_for, request, session, g, redirect
import os

# Setup
app = Flask(__name__)
app.secret_key = "hush dont tell anyone"

# Home page
@app.route("/")
def show_index_page():
    return render_template('index.html')

# Login
@app.route("/login")
def do_login():
    server_url = 'http://emel-id.org:3000/authorize'
    callback_url = 'http://0.0.0.0:5000/authenticated'
    server_key = os.getenv('SPP_APP_KEY')
    login_uri = "%s?key=%s&callback_url=%s" % (server_url, server_key, callback_url)
    return redirect(login_uri)

@app.route('/authenticated')
def authenticated():
    flash('You are signed in. Welcome!')
    session['emel_id_logged_in'] = True
    return redirect(url_for('show_index_page'))
                             
# Logout
@app.route("/logout")
def do_logout():
    session.pop('emel_id_logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_index_page'))
                    
if __name__ == "__main__":
    app.run()
