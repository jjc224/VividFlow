import os

g_settings = Constants.Settings['modules']
g_vividflow_lib_dir = os.path.join('static', g_settings['path_rel_vividflow_lib_dir'])

def get_module_template_code():
    template_file = os.path.join(g_vividflow_lib_dir, g_settings['vividflow_lib_template_source'])
    with open(template_file, 'r') as file:
        return file.read()

@app.route('/module/list/json')
def list_modules_as_json():
    modules_from_db = dbconn.db.get_all_modules_json(session['user']['id'])
    module_strings = []
    for obj in modules_from_db:
        module_strings.append(obj["jsonstr"])
    return json.dumps(module_strings)

@app.route('/module/create')
def create_module():
    result = dbconn.db.create_module(session['user']['id'])
    newUrl = url_for('edit_module', module_id=result);
    #newUrl = url_for('list_modules')
    return app.jinja_env.get_template("redirect.html").render(NEW_URL=newUrl)

@app.route('/module/<module_id>/delete')
def delete_module(module_id):
    #result = dbconn.db.create_algorithm()
    #newUrl = url_for('view_algorithm', algorithm_id=result);
    #return app.jinja_env.get_template("redirect.html").render(NEW_URL=newUrl)
    if dbconn.db.delete_module(module_id) > 0:
        return "Success!"
    return "Failed!"

@app.route('/module/list')
def list_modules():
    return app.jinja_env.get_template('user/modulelist.html').render(MODULE_DICT=dbconn.db.get_all_modules(session['user']['id']))

@app.route('/module/<module_id>/edit')
def edit_module(module_id):
    vividflow_lib_abs_path = os.path.join(os.sep, g_vividflow_lib_dir, g_settings['vividflow_lib_header'])
    #os.path.join(os.sep, 'static', g_settings['path_rel_vividflow_lib_dir'], g_settings['vividflow_lib_header'])
    return app.jinja_env.get_template("user/module_designer.html").render(MODULE_ID=module_id, VIVIDFLOW_LIB_PATH=vividflow_lib_abs_path)

@app.route('/module/<module_id>/json', methods=['GET', 'POST'])
def module_json_request(module_id):
    if request.method == 'GET':
        retrieved_module = dbconn.db.get_module(module_id)
        if retrieved_module is None:
            return "{}"
        return json.dumps(retrieved_module)
    elif request.method == 'POST':
        dbconn.db.insert_module_str(request.form["module"]);
        return "thank you!"
    else:
        print "unsupported request"
        return "Unsupported request"

@app.route('/module/<module_id>/code', methods=['GET', 'POST'])
def module_code_request(module_id):
    module_json = dbconn.db.get_module(module_id)
    if module_json is None:
        return "Module version does not exist."

    reconstructed_module = Constants.SerialObjectTypes.build_object_from_json(module_json)
    if reconstructed_module is None:
        return "{}"

    if request.method == 'GET':
        module_code = reconstructed_module.get_code()
        if module_code is None:
            return get_module_template_code()    # return "No code."
        return module_code
    elif request.method == 'POST':
        module_code = json.loads(request.form['module_code'])
        reconstructed_module.upload_code(module_code)
        print request.form
        return "thank you!"
    else:
        print "unsupported request"
        return "Unsupported request"
