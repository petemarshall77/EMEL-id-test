#!/usr/bin/python

from flask import Flask, render_template, flash, url_for, request, session, g, redirect

from flask_oauth import OAuth

# Setup
app = Flask(__name__)
app.secret_key = "hush dont tell anyone"

# OAuth setup
oauth = OAuth()
emelid = oauth.remote_app('emel_id',
                           base_url = 'http://0.0.0.0:3000',
#                           request_token_url = 'http://0.0.0.0:3000/oauth/token',
                           request_token_url = None,
                           access_token_url = 'http://0.0.0.0:3000/oauth/token',
                           authorize_url = 'http://0.0.0.0:3000/oauth/authorize',
                           consumer_key = 'cfa59195dbbb31094beda066891bf5112be0f15e161834c4a8f4b2237a5bfae4',
                           consumer_secret = '3d6060f08d972225e0db9977073317355a530e7e323eabce980afa4a04d1b2be')


# Home page
@app.route("/")
def show_index_page():
    return render_template('index.html')

# Login
@app.route("/login")
def do_login():
    return emelid.authorize(callback = url_for('oauth_authenticated',
                                                next = request.args.get('next') or request.referrer or None))
                                                

@emelid.tokengetter
def get_emel_id_token(token=None):
    return session.get('emel_id_token')

@app.route('/oauth_authenticated')
@emelid.authorized_handler
def oauth_authenticated(resp):
    print "Got to Here!!!"
    print resp
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash('You did not sign in')
        return redirect(next_url)

    session['emel_id_token'] = (resp['oauth_token'], resp['oauth_token_secret'])
    flash('You are signed in')
    return redirect(next_url)
                             

# Logout
@app.route("/logout")
def do_logout():
    session.pop('emel_id_token', None)
    flash('You were logged out')
    return redirect(url_for('index'))
                    
if __name__ == "__main__":
    app.run()
