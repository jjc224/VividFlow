
execfile("routes/algorithm/algorithm.py")
execfile("routes/module/module.py")
execfile("routes/resource/resource.py")
execfile("routes/public.py")
execfile("routes/user/user.py")


# /module/node/?
@app.route('/node/<node_id>/output')
def output_node():
    pass
    #return app.jinja_env.get_template('node_output.html').render(...)
