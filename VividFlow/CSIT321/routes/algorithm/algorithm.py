# Algorithm
@app.route('/algorithm/list')
def algorithm_list(options = ''):
    return app.jinja_env.get_template('user/algorithmlist.html').render(ALGORITHM_DICT=dbconn.db.get_all_algorithms(session['user']['id']))

@app.route('/algorithm/create')
def create_algorithm():
    result = dbconn.db.create_algorithm(session['user']['id'])
    newUrl = url_for('view_algorithm', algorithm_id=result);
    return app.jinja_env.get_template("redirect.html").render(NEW_URL=newUrl)

@app.route('/algorithm/<algorithm_id>/delete')
def delete_algorithm(algorithm_id):
    #result = dbconn.db.create_algorithm()
    #newUrl = url_for('view_algorithm', algorithm_id=result);
    #return app.jinja_env.get_template("redirect.html").render(NEW_URL=newUrl)
    if dbconn.db.delete_algorithm(algorithm_id) > 0:
        return "Success!"
    return "Failed!"

@app.route('/algorithm/<algorithm_id>/json', methods=['GET', 'POST'])
def algorithm_json_request(algorithm_id):
    if request.method == 'GET':
        retrieved_algorithm = dbconn.db.get_algorithm(algorithm_id)
        if retrieved_algorithm is None:
            return "{}"
        algo = Constants.SerialObjectTypes.build_object_from_json(retrieved_algorithm)
        algo.upgrade_modules()
        algo.relink_algorithm()
        return algo.serialize_json();
        #return json.dumps(retrieved_algorithm)
    elif request.method == 'POST':
        dbconn.db.insert_algo_str(request.form["algo"]);
        #print request.form
        return "thank you!"
    else:
        print "unsupported request"
        return "Unsupported request"

@app.route('/algorithm/<algorithm_id>/view')
def view_algorithm(algorithm_id):
    # algorithm_exists = dbconn.db.check_algorithm_exists(algorithm_id)
    # if algorithm_exists:
    return app.jinja_env.get_template("user/algorithm_designer.html").render(ALGORITHM_ID=algorithm_id)
    # else:
    # return app.jinja_env.get_template('user/algorithmlist.html').render(ALGORITHM_DICT=dbconn.db.get_all_algorithms())


@app.route('/algorithm/<algorithm_id>/history')
def view_algorithm_history(algorithm_id):
    jobs = dbconn.db.get_scheduled_tasks_for_algorithm(algorithm_id)
    jobs_objects = []
    for item in jobs:
        newobj = json.loads(item["jsonstr"])
        newobj = Constants.SerialObjectTypes.build_object_from_json(newobj)
        jobs_objects.append(newobj)
    return app.jinja_env.get_template("user/algorithm_run_log.html").render(ALGORITHM_ID=algorithm_id, HISTORY_DICT=jobs_objects)

@app.route('/algorithm/<algorithm_id>/schedule_run', methods=['GET'])
def schedule_algorithm_run(algorithm_id):
    if request.method == 'GET':
        algo_json = dbconn.db.get_algorithm(algorithm_id)
        if algo_json is None:
            return "Algorithm does not exist"
        taskid = dbconn.db.create_scheduled_task()
        json_obj = dbconn.db.get_scheduled_task(taskid)
        task = Constants.SerialObjectTypes.build_object_from_json(json_obj)
        task.mark_task_scheduled()
        task.set_algorithm_id(algo_json["_AlgorithmID"])
        dbconn.db.insert_schedtask_str(task.serialize_json())
        return "JobID: " + str(task._ScheduledTaskID) + " scheduled"
    else:
        print "unsupported request"
        return "Unsupported request"
