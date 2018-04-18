@app.route('/')
def hello_world():
    if user_is_logged_in():
        return app.jinja_env.get_template("user/landing_page.html").render()
    else:
        return app.jinja_env.get_template("public/home.html").render()

@app.route('/testtemplate/')
def test_template(options=""):
    return app.jinja_env.get_template("testtemplate.html").render(IPADDRESS=request.remote_addr)
