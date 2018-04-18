# User

# Session functions.
def user_is_logged_in():
    return session.has_key('user')

def user_is_disabled():
    return user_is_logged_in() and session['user']['disabled']

@app.route('/user/login', methods=['POST'])
def login_user():
    print request.form["username"]
    user_id = dbconn.db.login_user(request.form["username"], request.form["password"])
    user_json = dbconn.db.get_user(user_id)
    if user_json is None:
        print "No users found"
        return redirect("/?failed=true", code=302)
    user_object = Constants.SerialObjectTypes.build_object_from_json(user_json)


    if not user_is_logged_in():
        session.update(user_object.build_session_dict())
        if user_is_disabled():
            # Delete session
            session.pop('user', True)
            print "User is disabled"
            return redirect("/?failed=true", code=302)
        #user successfully logged in
        return redirect("/", code=302)
    else:
        return redirect("/?failed=true", code=302)

@app.route('/user/logout')
def logout_user():
    if not user_is_logged_in():
        return 'User is not logged in.'

    dbconn.db.logout_user(session['user']['id'])
    # Delete session
    session.pop('user', True)

    return redirect("/", code=302)

@app.route('/user/create', methods=['POST'])
def create_user():
    username = request.form["username"]
    password = request.form["password"]
    result = dbconn.db.create_user(username, password)
    if result is None:
        return "failed to create new account"
    else:
        return "success"

# TODO: 'enable' route?
@app.route('/user/disable')
@app.route('/user/<user_id>/disable')
def disable_user(user_id = None):
    result = None
    if user_id is None:
        if not user_is_logged_in():
            return 'User is not logged in.'

        result = dbconn.db.disable_user(session['user']['id'])
        session['user']['disabled'] = True
    else:
        result = dbconn.db.disable_user(user_id)
    if result is None:
        return "failed to disable account"
    else:
        return "success"

@app.route('/user/enable')
@app.route('/user/<user_id>/enable')
def enable_user(user_id = None):
    if user_id is None:
        if not user_is_logged_in():
            return 'User is not logged in.'
        dbconn.db.enable_user(session['user']['id'])
        session['user']['disabled'] = False
    else:
        dbconn.db.enable_user(user_id)
    return 'success'
    #return app.jinja_env.get_template('user/enable.html').render(USER_ID=user_id)    # TODO: enable.html does not exist.

@app.route('/user/modify')
#@app.route('/user/<user_id>/modify')
def modify_user(user_id = None):
    # Check a user is logged in
    if not user_is_logged_in():
        return redirect("/", code=302)
    return app.jinja_env.get_template('user/modify.html').render(USER_ID=session['user']['id'])

@app.route('/user/reset_password', methods=['POST'])
#@app.route('/user/<user_id>/reset_password', methods=['POST'])
def reset_password():
    if not user_is_logged_in():
        return redirect("/", code=302)
    result = dbconn.db.update_password(session['user']['id'], request.form["password"])
    if result is None:
        return "Failed to reset password"
    else:
        return "success"

@app.route('/user/<user_id>/json', methods=['GET', 'POST'])
def user_json_request(user_id):
    if request.method == 'GET':
        retrieved_user = dbconn.db.get_user(user_id)
        if retrieved_user is None:
            return "{}"
        return json.dumps(retrieved_user)
    elif request.method == 'POST':
        dbconn.db.insert_user_str(request.form['user']);
        return "thank you!"
    else:
        print "unsupported request"
        return "Unsupported request"
