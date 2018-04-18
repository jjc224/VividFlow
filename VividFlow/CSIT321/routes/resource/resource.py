import Constants
import os
from werkzeug.utils import secure_filename

@app.route('/resource/list')
def resource_list():
    resources = dbconn.db.get_resource_list(session['user']['id'])
    return json.dumps(resources)

@app.route('/resource/manager')
def resource_manager():
    return app.jinja_env.get_template('user/resource_manager.html').render()


@app.route('/resource/add', methods=['POST'])
def resource_add():
    # Insert db record and get record id
    id = dbconn.db.insert_resource(request.form, session['user']['id'])
    # check if the post request has the file part
    if 'file' not in request.files:
        print('No file part')
    else:
        file = request.files['file']
        if file.filename == '':
            print('No selected file')
        else:
            # Figure out filename
            filename = secure_filename(file.filename)
            print "File Found: " + file.filename
            # Figure out file path
            folder_path = str(os.path.join(Constants.Settings["resources"]["path_abs"], str(id)))
            print folder_path
            # Try to delete any existing files
            try:
                dir_files = os.listdir(folder_path)
                for item in dir_files:
                    os.remove(os.path.join(folder_path, item))
            except:
                print "No folder to delete"
            # Try to create directory for file
            try:
                os.mkdir(folder_path)
            except:
                print "Could no make dir"
                pass
            # Save file to hdd
            file.save(os.path.join(folder_path, filename))
    return "success"
