import sys
import pymysql.cursors
import json
import Constants
import Module
import ScheduledTask
import Algorithm
import User
from werkzeug.utils import secure_filename

class DBConnect:
    conn = None
    def __init__(self):
        self.connect_to_database()

    def _actually_connect_to_database(self):
        if self.conn is not None:
            try:
                self.conn.close()
            except:
                pass
        self.conn = pymysql.connect(host=Constants.Settings["db"]["hostname"],
                                    user=Constants.Settings["db"]["username"],
                                    password=Constants.Settings["db"]["password"],
                                    db=Constants.Settings["db"]["dbname"],
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor,
                                    autocommit=True)

    def connect_to_database(self):
        if self.conn is None or self.conn.open is False:
            self._actually_connect_to_database()
        else:
            try:
                with self.conn.cursor() as cursor:
                    # Read a single record
                    sql = "SELECT now()"
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    cursor.close()
            except:
                self._actually_connect_to_database()

    def close_connection(self):
        self.conn.close()

    def __del__(self):
        self.close_connection()

    def delete_algorithm(self, algoid):
        # Update algorithm
        print "Delete"
        rowsaffected = 0
        with self.conn.cursor() as cursor:
            sql = "DELETE FROM algorithm WHERE id=%s"
            cursor.execute(sql, (algoid))
            rowsaffected = cursor.rowcount
            cursor.close()
        return rowsaffected

    def delete_module(self, modid):
        # Update algorithm
        print "Delete"
        rowsaffected = 0
        with self.conn.cursor() as cursor:
            sql = "UPDATE module SET moduleversionstate=%s WHERE moduleid=%s"
            cursor.execute(sql, ("Retired", modid))
            rowsaffected = cursor.rowcount
            cursor.close()
        return rowsaffected

    def create_algorithm(self, userid):
        print "UserID = " + str(userid)
        #blank_object = """{"ObjectType":"Algorithm","_ObjectID":"0.855728915432","_AlgorithmName":"Test Algorithm","_Links":[{"ObjectType":"Link","_ObjectID":"0.528267114008","_In_Node_Id":"0.509584754457","_In_Socket_Id":"0.711196963317","_Out_Node_Id":"0.0219765860289","_Out_Socket_Id":"0.723020435549"},{"ObjectType":"Link","_ObjectID":"0.650707573661","_In_Node_Id":"0.509584754457","_In_Socket_Id":"0.612248955965","_Out_Node_Id":"0.465383768327","_Out_Socket_Id":"0.195663637935"},{"ObjectType":"Link","_ObjectID":"0.843939951377","_In_Node_Id":"0.0219765860289","_In_Socket_Id":"0.552629630653","_Out_Node_Id":"0.0549616363085","_Out_Socket_Id":"0.365033258614"},{"ObjectType":"Link","_ObjectID":"0.768619115474","_In_Node_Id":"0.195308552177","_In_Socket_Id":"0.570632894723","_Out_Node_Id":"0.0219765860289","_Out_Socket_Id":"0.723020435549"}],"_Nodes":[{"ObjectType":"StringTestNode","_ObjectID":"0.509584754457","_PosX":535,"_PosY":236,"_InputSockets":[{"ObjectType":"NodeIOSocket","_ObjectID":"0.711196963317","_ArgumentNumber":1,"_Name":"Output","_DataType":"String","_OwnerNodeId":"0.509584754457","_Required":false},{"ObjectType":"NodeIOSocket","_ObjectID":"0.612248955965","_ArgumentNumber":2,"_Name":"Output","_DataType":"String","_OwnerNodeId":"0.509584754457","_Required":false}],"_OutputSockets":[{"ObjectType":"NodeIOSocket","_ObjectID":"0.114729205702","_ArgumentNumber":1,"_Name":"Output","_DataType":"String","_OwnerNodeId":"0.509584754457","_Required":false}],"_ModuleId":null,"_Node_Name":"Node1"},{"ObjectType":"StringTestNode","_ObjectID":"0.0219765860289","_PosX":269,"_PosY":66,"_InputSockets":[{"ObjectType":"NodeIOSocket","_ObjectID":"0.552629630653","_ArgumentNumber":1,"_Name":"Output","_DataType":"String","_OwnerNodeId":"0.0219765860289","_Required":false}],"_OutputSockets":[{"ObjectType":"NodeIOSocket","_ObjectID":"0.723020435549","_ArgumentNumber":1,"_Name":"Output","_DataType":"String","_OwnerNodeId":"0.0219765860289","_Required":false}],"_ModuleId":null,"_Node_Name":"Node2"},{"ObjectType":"StringTestNode","_ObjectID":"0.465383768327","_PosX":270,"_PosY":237,"_InputSockets":[],"_OutputSockets":[{"ObjectType":"NodeIOSocket","_ObjectID":"0.195663637935","_ArgumentNumber":1,"_Name":"Output","_DataType":"String","_OwnerNodeId":"0.465383768327","_Required":false}],"_ModuleId":null,"_Node_Name":"Node3"},{"ObjectType":"StringTestNode","_ObjectID":"0.0549616363085","_PosX":24,"_PosY":66,"_InputSockets":[],"_OutputSockets":[{"ObjectType":"NodeIOSocket","_ObjectID":"0.365033258614","_ArgumentNumber":1,"_Name":"Output","_DataType":"String","_OwnerNodeId":"0.0549616363085","_Required":false}],"_ModuleId":null,"_Node_Name":"Node4"},{"ObjectType":"StringTestNode","_ObjectID":"0.195308552177","_PosX":535,"_PosY":66,"_InputSockets":[{"ObjectType":"NodeIOSocket","_ObjectID":"0.570632894723","_ArgumentNumber":1,"_Name":"Output","_DataType":"String","_OwnerNodeId":"0.195308552177","_Required":false}],"_OutputSockets":[{"ObjectType":"NodeIOSocket","_ObjectID":"0.509081553008","_ArgumentNumber":1,"_Name":"Output","_DataType":"String","_OwnerNodeId":"0.195308552177","_Required":false}],"_ModuleId":null,"_Node_Name":"Node5"},{"ObjectType":"ValueNode","_ObjectID":"0.0963301177146","_PosX":28,"_PosY":238,"_InputSockets":[{"ObjectType":"NodeIOSocket","_ObjectID":"0.470905082632","_ArgumentNumber":1,"_Name":"Output","_DataType":"Integer","_OwnerNodeId":"0.0963301177146","_Required":false}],"_OutputSockets":[],"_DataType":"Integer","_Value":23}],"_UserID":""" + str(userid) + """}"""
        blank_object = Algorithm.Algorithm()
        blank_object.set_algorithm_userid(userid)
        blank_object = blank_object.serialize_json()
        blank_object = json.loads(blank_object)

        rowid = self.insert_algo_dict(blank_object)
        if rowid is not None:
            blank_object["_AlgorithmID"] = str(rowid)
            self.insert_algo_dict(blank_object)
            return rowid
        return None

    def create_module(self, userid):
        blank_object = Module.ModuleNode()
        blank_object.set_module_userid(userid)
        blank_object = blank_object.serialize_json()
        blank_object = json.loads(blank_object)
        rowid = self.insert_module_dict(blank_object)
        if rowid is not None:
            blank_object["_ModuleVersionId"] = str(rowid)
            blank_object["_ModuleId"] = str(rowid)
            self.insert_module_dict(blank_object)
            return rowid
        return None

    def create_scheduled_task(self):
        blank_object = ScheduledTask.ScheduledTask().serialize_json()
        blank_object = json.loads(blank_object)
        rowid = self.insert_schedtask_dict(blank_object)
        if rowid is not None:
            blank_object["_ScheduledTaskID"] = str(rowid)
            self.insert_schedtask_dict(blank_object)
            return rowid
        return None

    def create_user(self, username, password):
        user_json = User.User(username=username, password=password).serialize_json()
        user_json = json.loads(user_json)
        rowid = self.insert_user_dict(user_json)
        if rowid is not None:
            user_json['_UserID'] = rowid    # NOTE: why do the other functions written use str(rowid)?
            self.insert_user_dict(user_json)
            return rowid
        return None

    def insert_schedtask_dict(self, task):
        self.connect_to_database()
        # Initialise variables for sql insert
        taskid = None
        algorithmid = None
        taskstatus = None

        # Extract data from dict
        if "_ScheduledTaskID" in task:
            taskid = task["_ScheduledTaskID"]
        if "_AlgorithmID" in task:
            algorithmid = task["_AlgorithmID"]
        if "_TaskStatus" in task:
            taskstatus = task["_TaskStatus"]

        # Show task values
        print "TaskID: ", taskid
        print "AlgoID: ", algorithmid
        print "TaskStatus: ", taskstatus
        print

        # Show Keys
        for k in task.keys():
            print k

        lastrowid = None

        # Check if insert or update required based on id
        if (taskid is None or taskid == ""):
            # Insert task
            print "Insert"
            with self.conn.cursor() as cursor:
                sql = "INSERT INTO scheduled_tasks (algorithmid, taskstatus, jsonstr) VALUES (%s, %s, %s)"
                cursor.execute(sql, (algorithmid, taskstatus, json.dumps(task)))
                lastrowid = cursor.lastrowid
                cursor.close()
        else:
            # Update task
            print "Update"
            with self.conn.cursor() as cursor:
                sql = "UPDATE scheduled_tasks SET algorithmid=%s, taskstatus=%s, jsonstr=%s WHERE scheduledtaskid=%s"
                cursor.execute(sql, (algorithmid, taskstatus, json.dumps(task), taskid))
                lastrowid = cursor.lastrowid
                cursor.close()
        self.conn.commit()
        return lastrowid

    def insert_schedtask_str(self, str):
        # Cast string to dictonary
        task = json.loads(str)
        # Use insert algo function
        self.insert_schedtask_dict(task)

    def retire_all_module_versions(self, module_id):
        self.connect_to_database()
        if module_id is None or module_id == "":
            return
        with self.conn.cursor() as cursor:
            sql = "UPDATE module SET moduleversionstate = \"" + Constants.ModuleStates.Retired + "\" WHERE moduleid=%s"
            cursor.execute(sql, (module_id))
            result = cursor.fetchall()
            return result

    def insert_module_dict(self, mod):
        self.connect_to_database()
        # Initialise variables for sql insert

        name = None
        modversionid = None
        userid = None
        version = None
        moduleid = None
        moduleversionstate = None

        # Extract data from dict
        if "_Name" in mod:
            name = mod["_Name"]
        if "_ModuleVersionId" in mod:
            modversionid = mod["_ModuleVersionId"]
        if "_UserID" in mod:
            userid = mod["_UserID"]
        if "_ModuleVersion" in mod:
            version = mod["_ModuleVersion"]
        if "_ModuleId" in mod:
            moduleid = mod["_ModuleId"]
        if "_ModuleVersionState" in mod:
            moduleversionstate = mod["_ModuleVersionState"]

        # Show mod values
        print "name:", name
        print "modversionid:", modversionid
        print "userid:", userid
        print "version:", version
        print "moduleid", moduleid
        print "moduleversionstate:", moduleversionstate
        print

        lastrowid = None

        self.retire_all_module_versions(moduleid)

        # Check if insert or update required based on id
        if modversionid is None or modversionid == "":
            if version is None:
                version = 1
            print "Insert"
            with self.conn.cursor() as cursor:
                sql = "INSERT INTO module (name, version, userid, moduleid, moduleversionstate, jsonstr) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (name, version, userid, moduleid, moduleversionstate, json.dumps(mod)))
                lastrowid = cursor.lastrowid
                cursor.close()
            if mod["_ModuleVersionId"] is None:
                mod["_ModuleVersionId"] = lastrowid
                self.insert_module_dict(mod)
        else:
            # Update algorithm
            print "Update"
            with self.conn.cursor() as cursor:
                sql = "UPDATE module SET name=%s, version=%s, userid=%s, moduleid=%s, moduleversionstate=%s, jsonstr=%s WHERE modversionid=%s"
                cursor.execute(sql, (name, version, userid, moduleid, moduleversionstate, json.dumps(mod), modversionid))
                lastrowid = cursor.lastrowid
                cursor.close()
        self.conn.commit()
        return lastrowid

    def insert_module_str(self, str):
        # Cast string to dictonary
        module = json.loads(str)
        # Use insert algo function
        self.insert_module_dict(module)

    def get_module_by_record_moduleversionid(self, modversionid):
        self.connect_to_database()
        with self.conn.cursor() as cursor:
            # Read a single record
            sql = "SELECT jsonstr from module where modversionid=%s"
            cursor.execute(sql, (modversionid))
            result = cursor.fetchone()
            if result is None:
                cursor.close()
                return None
            result = json.loads(result["jsonstr"])
            cursor.close()
            return result

    def get_module_by_object_id(self, moduleid, version):
        self.connect_to_database()
        with self.conn.cursor() as cursor:
            # Read a single record
            sql = "SELECT jsonstr from module where moduleid=%s and version=%s"
            cursor.execute(sql, (moduleid, version))
            result = cursor.fetchone()
            if result is None:
                cursor.close()
                return None
            result = json.loads(result["jsonstr"])
            cursor.close()
            return result

    def get_latest_module_version(self, moduleid):
        self.connect_to_database()
        with self.conn.cursor() as cursor:
            # Read a single record
            sql = "SELECT jsonstr FROM module WHERE moduleid=%s AND version=(select max(version) from module where moduleid=%s)"
            cursor.execute(sql, (moduleid, moduleid))
            result = cursor.fetchone()
            if result is None:
                cursor.close()
                return None
            result = json.loads(result["jsonstr"])
            cursor.close()
            return result

    def insert_algo_dict(self, algo):
        self.connect_to_database()
        # Initialise variables for sql insert
        name = None
        algoid = None
        userid = None
        version = None

        # Extract data from dict
        if "_AlgorithmName" in algo:
            name = algo["_AlgorithmName"]
        if "_AlgorithmID" in algo:
            algoid = algo["_AlgorithmID"]
        if "_UserID" in algo:
            userid = algo["_UserID"]
        if "_Version" in algo:
            version = algo["_Version"]

        # Show algo values
        print "Name: ", name
        print "AlgoID: ", algoid
        print "UserID: ", userid
        print "Version: ", version
        print

        # Show Keys
        for k in algo.keys():
            print k

        lastrowid = None

        # Check if insert or update required based on id
        if (algoid is None or algoid == ""):
            # Insert algorithm
            if (version is None):
                version = 1
            print "Insert"
            with self.conn.cursor() as cursor:
                sql = "INSERT INTO algorithm (name, version, userid, jsonstr) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (name, version, userid, json.dumps(algo)))
                lastrowid = cursor.lastrowid
                cursor.close()
        else:
            # Update algorithm
            print "Update"
            with self.conn.cursor() as cursor:
                sql = "UPDATE algorithm SET name=%s, version=%s, userid=%s, jsonstr=%s WHERE id=%s"
                cursor.execute(sql, (name, version, userid, json.dumps(algo), algoid))
                lastrowid = cursor.lastrowid
                cursor.close()
        self.conn.commit()
        return lastrowid

    def insert_algo_str(self, str):
        # Cast string to dictonary
        algo = json.loads(str)
        # Use insert algo function
        self.insert_algo_dict(algo)

    def get_all_algorithms(self, userid):
        self.connect_to_database()
        with self.conn.cursor() as cursor:
            # Read a single record
            sql = "SELECT id, name, version, userid from algorithm where userid=%s"
            cursor.execute(sql, (userid))
            result = cursor.fetchall()
            for row in result:
                print row["id"], " : ", row["name"], " : Ver ", row["version"]
            cursor.close()
            return result

    def get_algorithm(self, id):
        return self.get_jsonstr('algorithm', 'id', id)

    def get_scheduled_task(self, id):
        return self.get_jsonstr('scheduled_tasks', 'scheduledtaskid', id)

    def get_all_modules(self, userid):
        self.connect_to_database()
        # Read a single record
        with self.conn.cursor() as cursor:
            sql = "SELECT modversionid, moduleversionstate, name, version, userid, moduleid FROM module m WHERE userid=%s AND modversionid = (SELECT MAX(modversionid) FROM module WHERE moduleid = m.moduleid) AND (moduleversionstate = 'Published' OR moduleversionstate = 'InDevelopment')"    # NOTE: only exludes jconstr column.
            cursor.execute(sql, (userid))
            result = cursor.fetchall()
            for row in result:
                print row["modversionid"], " : ", row["name"], " : Ver ", row["version"]
            return result

    def get_all_modules_json(self, userid):
        self.connect_to_database()
        with self.conn.cursor() as cursor:
            sql = "SELECT * FROM module m WHERE userid=%s AND modversionid = (SELECT MAX(modversionid) FROM module WHERE moduleid = m.moduleid) AND (moduleversionstate = 'Published' OR moduleversionstate = 'InDevelopment')"
            cursor.execute(sql, (userid))
            result = cursor.fetchall()
            return result

    def get_module(self, id):
        self.connect_to_database()
        with self.conn.cursor() as cursor:
            # Read a single record
            sql = "SELECT jsonstr from module where moduleid = %s order by version desc limit 1"
            cursor.execute(sql, (str(id)))
            result = cursor.fetchone()
            if result is None:
                return None
            if result["jsonstr"] is None:
                print >> sys.stderr, "Unexpected error: jsonstr column for module is NULL."
                return None
            result = json.loads(result["jsonstr"])
            return result

    def update_scheduled_task(self, task):
        self.connect_to_database()
        with self.conn.cursor() as cursor:
            sql = "UPDATE scheduled_tasks SET taskstatus=%s, jsonstr=%s WHERE scheduledtaskid=%s"
            cursor.execute(sql, (task._TaskStatus, task.serialize_json(), task._ScheduledTaskID))
            lastrowid = cursor.lastrowid
            cursor.close()
            self.conn.commit()

    # A more general function to retrieve 'jsonstr' column for some table and id column, as it's used a lot.
    def get_jsonstr(self, table, id_column, id):
        self.connect_to_database()
        with self.conn.cursor() as cursor:
            # Read a single record
            sql = "SELECT jsonstr from " + table + " where " + id_column + " = %s order by " + id_column + " desc limit 1"
            cursor.execute(sql, (str(id)))
            result = cursor.fetchone()
            if result is None:
                return None
            if result["jsonstr"] is None:
                print >> sys.stderr, "Unexpected error: jsonstr column for module is NULL."
                return None
            result = json.loads(result["jsonstr"])
            return result

    def get_one_scheduled_task_with_status(self, status):
        self.connect_to_database()
        with self.conn.cursor() as cursor:
            sql = "SELECT jsonstr from scheduled_tasks where taskstatus='" + status + "' order by scheduledtaskid limit 1"
            cursor.execute(sql)
            result = cursor.fetchone()
            if result is None:
                return None
            if result["jsonstr"] is None:
                print >> sys.stderr, "Unexpected error: jsonstr column for module is NULL."
                return None
            result = json.loads(result["jsonstr"])
            return result

    def get_scheduled_tasks_for_algorithm(self, algorithm_id):
        self.connect_to_database()
        with self.conn.cursor() as cursor:
            sql = "SELECT jsonstr from scheduled_tasks where algorithmid='" + algorithm_id + "'"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result

    def count_scheduled_tasks_with_status(self, status):
        self.connect_to_database()
        with self.conn.cursor() as cursor:
            sql = "SELECT count(scheduledtaskid) as count from scheduled_tasks where taskstatus='" + status + "'"
            cursor.execute(sql)
            result = cursor.fetchone()
            if result is None:
                return None
            if result["count"] is None:
                print >> sys.stderr, "Unexpected error: jsonstr column for module is NULL."
                return None
            result = result["count"]
            return result

    def get_resource_list(self, user_id = None):
        self.connect_to_database()
        with self.conn.cursor() as cursor:
            sql = "SELECT * FROM resource WHERE NOT deleted AND user_id=%s"
            cursor.execute(sql, (user_id))
            result = cursor.fetchall()
            return result

    def get_resource_by_id(self, res_id, user_id = None):
        self.connect_to_database()
        with self.conn.cursor() as cursor:
            sql = "SELECT * FROM resource WHERE NOT deleted and id = " + str(res_id)
            cursor.execute(sql)
            result = cursor.fetchone()
            return result

    def insert_resource(self, resource, userid):
        self.connect_to_database()

        # Initialise variables for sql insert
        row_id = None
        filename= None
        resource_name = None
        file_type = None
        user_id = userid
        deleted = 0

        # Extract data from dict
        if "id" in resource:
            row_id = resource["id"]
        if "filename" in resource:
            filename = secure_filename(resource["filename"])
        if "resource_name" in resource:
            resource_name = resource["resource_name"]
        if "file_type" in resource:
            file_type = resource["file_type"]
        if "deleted" in resource:
            deleted = resource["deleted"]

        # Show mod values
        print "id:", row_id
        print "filename:", filename
        print "resource_name:", resource_name
        print "file_type:", file_type
        print "user_id:", user_id
        print "deleted:", deleted
        print

        # for return
        lastrowid = None
        # Check if insert or update required based on id
        if row_id is None or row_id == "":
            print "Insert"
            with self.conn.cursor() as cursor:
                sql = "INSERT INTO resource (filename, resource_name, file_type, user_id, deleted) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (filename, resource_name, file_type, user_id, deleted))
                lastrowid = cursor.lastrowid
                cursor.close()
        else:
            print "Update"
            with self.conn.cursor() as cursor:
                sql = "UPDATE resource SET filename=%s, resource_name=%s, file_type=%s, user_id=%s, deleted=%s WHERE id=%s"
                #sql = "UPDATE resource SET resource_name=%s WHERE id=%s"
                cursor.execute(sql, (filename, resource_name, file_type, user_id, deleted, row_id))
                lastrowid = row_id
                cursor.close()
        self.conn.commit()
        return lastrowid

    def insert_user(self, user):
        self.connect_to_database()
        lastrowid = None
        with self.conn.cursor() as cursor:
            sql = "INSERT INTO user (username, password, logged_in, disabled, jsonstr) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (user._UserName, user._UserPassword, int(user._LoggedIn), int(user._Disabled), user.serialize_json()))
            lastrowid = cursor.lastrowid
            cursor.close()
            self.conn.commit()
        return lastrowid

    def get_user(self, id):
        return self.get_jsonstr('user', 'id', id)

    # NOTE: json update works, but need to update jsonstr for most queries.
    # Looking for a better way to do it.
    def update_password(self, user_id, password):
        user_json = self.get_user(user_id)

        if user_json is None:
            return None

        user_json['_UserPassword'] = User.User.get_hash(password)

        self.connect_to_database()
        lastrowid = None
        with self.conn.cursor() as cursor:
            sql = "UPDATE user SET password=%s, jsonstr=%s WHERE id=%s"
            cursor.execute(sql, (user_json['_UserPassword'], json.dumps(user_json), user_id))
            lastrowid = cursor.lastrowid
            cursor.close()
            self.conn.commit()
        return lastrowid

    def disable_user(self, user_id):
        return self.update_user_access(user_id, True)

    def enable_user(self, user_id):
        return self.update_user_access(user_id, False)

    def update_username(self, user_id, username):
        user_json = self.get_user(user_id)

        if user_json is None:
            return None

        user_json['_UserName'] = username

        self.connect_to_database()
        lastrowid = None
        with self.conn.cursor() as cursor:
            sql = "UPDATE user SET username=%s, jsonstr=%s WHERE id=%s"
            cursor.execute(sql, (username, json.dumps(user_json), user_id))
            lastrowid = cursor.lastrowid
            cursor.close()
            self.conn.commit()
        return lastrowid

    def update_user_access(self, user_id, disabled):
        user_json = self.get_user(user_id)

        if user_json is None:
            return None

        user_json['_Disabled'] = disabled

        self.connect_to_database()
        lastrowid = None
        with self.conn.cursor() as cursor:
            sql = "UPDATE user SET disabled=%s, jsonstr=%s WHERE id=%s"
            cursor.execute(sql, (disabled, json.dumps(user_json), user_id))
            lastrowid = cursor.lastrowid
            cursor.close()
            self.conn.commit()
        return lastrowid

    def modify_user(self, user_id, username, password, disabled):
        # NOTE: Better to use one query, will review. Individual functions are needed for other routes.
        self.update_username(user_id, username)
        self.update_password(user_id, password)
        self.update_user_access(user_id, disabled)

    def get_user_login_status(self, user_id = None):
        with self.conn.cursor() as cursor:
            # Read a single record
            sql = "SELECT logged_in FROM user WHERE user_id=%s"
            cursor.execute(sql, (username))
            result = cursor.fetchone()
            if result is None:
                cursor.close()
                return None
            cursor.close()
            return result['logged_in']

    def update_user_login_status(self, user_id, logged_in):
        user_json = self.get_user(user_id)

        if user_json is None:
            return None

        user_json['_LoggedIn'] = logged_in

        self.connect_to_database()
        lastrowid = None
        with self.conn.cursor() as cursor:
            sql = "UPDATE user SET logged_in=%s, jsonstr=%s WHERE id=%s"
            cursor.execute(sql, (logged_in, json.dumps(user_json), user_id))
            lastrowid = cursor.lastrowid
            cursor.close()
            self.conn.commit()
        return lastrowid

    # TODO: implement session expirary functionality.
    def logout_user(self, user_id):
        return self.update_user_login_status(user_id, False)

    # TODO: implement session creation functionality.
    # TODO: what if multiple rowws have the same username and password?
    def login_user(self, username, password):
        self.connect_to_database()
        with self.conn.cursor() as cursor:
            # Read a single record
            sql = "SELECT id FROM user WHERE username=%s"
            cursor.execute(sql, (username))
            result = cursor.fetchone()
            if result is None:
                cursor.close()
                return None
            user_id = result['id']
            cursor.close()

        user_json = self.get_user(user_id)

        if user_json is None:
            return None

        user_object = Constants.SerialObjectTypes.build_object_from_json(user_json)

        if user_object.check_password(password):
            if not self.update_user_login_status(user_id, True):
                print >> sys.stderr, 'Unable to update logged_in = True in database.'
        else:
                print >> sys.stderr, 'Unable to login user (id = %i).' % user_id
                return None

        return user_id

    def insert_user_dict(self, user):
        self.connect_to_database()

        # Show dict.
        for k, v in user.items():
            print (k, v)

        lastrowid = None

        try:
            # Check if insert or update required based on id
            if (user['_UserID'] is None or user['_UserID'] == ""):
                # Insert task
                print "Insert"
                with self.conn.cursor() as cursor:
                    sql = "INSERT INTO user (id, username, password, logged_in, disabled, jsonstr) VALUES (%s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (user['_UserID'], user['_UserName'], user['_UserPassword'], user['_LoggedIn'], user['_Disabled'], json.dumps(user)))
                    lastrowid = cursor.lastrowid
                    cursor.close()
            else:
                # Update task
                print "Update"
                with self.conn.cursor() as cursor:
                    sql = "UPDATE user SET username=%s, password=%s, logged_in=%s, disabled=%s, jsonstr=%s WHERE id=%s"
                    cursor.execute(sql, (user['_UserName'], user['_UserPassword'], user['_LoggedIn'], user['_Disabled'], json.dumps(user), user['_UserID']))
                    lastrowid = cursor.lastrowid
                    cursor.close()
            self.conn.commit()
            return lastrowid
        except:
            return None

    def insert_user_str(self, str):
        user = json.loads(str)
        self.insert_user_dict(user)

db = DBConnect()

# test insert and update
# db.insert_algo_str('{"_Nodes": [{"_Node_Name": "Node1", "_NodeId": null, "_InputSockets": [{"_DataType": "String", "_Name": "Output", "_Required": false, "_DBObjectID": null, "_ArgumentNumber": 1, "_OwnerNodeId": null, "ObjectType": "NodeIOSocket"}, {"_DataType": "String", "_Name": "Output", "_Required": false, "_DBObjectID": null, "_ArgumentNumber": 2, "_OwnerNodeId": null, "ObjectType": "NodeIOSocket"}], "_OutputSockets": [{"_DataType": "String", "_Name": "Output", "_Required": false, "_DBObjectID": null, "_ArgumentNumber": 1, "_OwnerNodeId": null, "ObjectType": "NodeIOSocket"}], "_DBObjectID": null, "_ModuleId": null, "_PosX": 0, "_PosY": 0, "ObjectType": "StringTestNode"}, {"_Node_Name": "Node2", "_NodeId": null, "_InputSockets": [{"_DataType": "String", "_Name": "Output", "_Required": false, "_DBObjectID": null, "_ArgumentNumber": 1, "_OwnerNodeId": null, "ObjectType": "NodeIOSocket"}], "_OutputSockets": [{"_DataType": "String", "_Name": "Output", "_Required": false, "_DBObjectID": null, "_ArgumentNumber": 1, "_OwnerNodeId": null, "ObjectType": "NodeIOSocket"}], "_DBObjectID": null, "_ModuleId": null, "_PosX": 0, "_PosY": 0, "ObjectType": "StringTestNode"}, {"_Node_Name": "Node3", "_NodeId": null, "_InputSockets": [], "_OutputSockets": [{"_DataType": "String", "_Name": "Output", "_Required": false, "_DBObjectID": null, "_ArgumentNumber": 1, "_OwnerNodeId": null, "ObjectType": "NodeIOSocket"}], "_DBObjectID": null, "_ModuleId": null, "_PosX": 0, "_PosY": 0, "ObjectType": "StringTestNode"}, {"_Node_Name": "Node4", "_NodeId": null, "_InputSockets": [], "_OutputSockets": [{"_DataType": "String", "_Name": "Output", "_Required": false, "_DBObjectID": null, "_ArgumentNumber": 1, "_OwnerNodeId": null, "ObjectType": "NodeIOSocket"}], "_DBObjectID": null, "_ModuleId": null, "_PosX": 0, "_PosY": 0, "ObjectType": "StringTestNode"}, {"_Node_Name": "Node5", "_NodeId": null, "_InputSockets": [{"_DataType": "String", "_Name": "Output", "_Required": false, "_DBObjectID": null, "_ArgumentNumber": 1, "_OwnerNodeId": null, "ObjectType": "NodeIOSocket"}], "_OutputSockets": [{"_DataType": "String", "_Name": "Output", "_Required": false, "_DBObjectID": null, "_ArgumentNumber": 1, "_OwnerNodeId": null, "ObjectType": "NodeIOSocket"}], "_DBObjectID": null, "_ModuleId": null, "_PosX": 0, "_PosY": 0, "ObjectType": "StringTestNode"}, {"_Value": 23, "_NodeId": null, "_InputSockets": [{"_DataType": "Integer", "_Name": "Output", "_Required": false, "_DBObjectID": null, "_ArgumentNumber": 0, "_OwnerNodeId": null, "ObjectType": "NodeIOSocket"}], "_DataType": "Integer", "_OutputSockets": [], "_DBObjectID": null, "_PosX": 0, "_PosY": 0, "ObjectType": "ValueNode"}], "_Links": [{"_Out_Node_Id": null, "_In_Socket_Num": 1, "_In_Node_Id": null, "_DBObjectID": null, "_Out_Socket_Num": 1, "ObjectType": "Link"}, {"_Out_Node_Id": null, "_In_Socket_Num": 2, "_In_Node_Id": null, "_DBObjectID": null, "_Out_Socket_Num": 1, "ObjectType": "Link"}, {"_Out_Node_Id": null, "_In_Socket_Num": 1, "_In_Node_Id": null, "_DBObjectID": null, "_Out_Socket_Num": 1, "ObjectType": "Link"}, {"_Out_Node_Id": null, "_In_Socket_Num": 1, "_In_Node_Id": null, "_DBObjectID": null, "_Out_Socket_Num": 1, "ObjectType": "Link"}], "_DBObjectID": null, "_AlgorithmName": "UntitledAlgorithm", "ObjectType": "Algorithm"}')
# db.insert_algo_str('{"_AlgorithmID":"1","_Version":"2","_Nodes": [{"_Node_Name": "Node1", "_NodeId": null, "_InputSockets": [{"_DataType": "String", "_Name": "Output", "_Required": false, "_DBObjectID": null, "_ArgumentNumber": 1, "_OwnerNodeId": null, "ObjectType": "NodeIOSocket"}, {"_DataType": "String", "_Name": "Output", "_Required": false, "_DBObjectID": null, "_ArgumentNumber": 2, "_OwnerNodeId": null, "ObjectType": "NodeIOSocket"}], "_OutputSockets": [{"_DataType": "String", "_Name": "Output", "_Required": false, "_DBObjectID": null, "_ArgumentNumber": 1, "_OwnerNodeId": null, "ObjectType": "NodeIOSocket"}], "_DBObjectID": null, "_ModuleId": null, "_PosX": 0, "_PosY": 0, "ObjectType": "StringTestNode"}, {"_Node_Name": "Node2", "_NodeId": null, "_InputSockets": [{"_DataType": "String", "_Name": "Output", "_Required": false, "_DBObjectID": null, "_ArgumentNumber": 1, "_OwnerNodeId": null, "ObjectType": "NodeIOSocket"}], "_OutputSockets": [{"_DataType": "String", "_Name": "Output", "_Required": false, "_DBObjectID": null, "_ArgumentNumber": 1, "_OwnerNodeId": null, "ObjectType": "NodeIOSocket"}], "_DBObjectID": null, "_ModuleId": null, "_PosX": 0, "_PosY": 0, "ObjectType": "StringTestNode"}, {"_Node_Name": "Node3", "_NodeId": null, "_InputSockets": [], "_OutputSockets": [{"_DataType": "String", "_Name": "Output", "_Required": false, "_DBObjectID": null, "_ArgumentNumber": 1, "_OwnerNodeId": null, "ObjectType": "NodeIOSocket"}], "_DBObjectID": null, "_ModuleId": null, "_PosX": 0, "_PosY": 0, "ObjectType": "StringTestNode"}, {"_Node_Name": "Node4", "_NodeId": null, "_InputSockets": [], "_OutputSockets": [{"_DataType": "String", "_Name": "Output", "_Required": false, "_DBObjectID": null, "_ArgumentNumber": 1, "_OwnerNodeId": null, "ObjectType": "NodeIOSocket"}], "_DBObjectID": null, "_ModuleId": null, "_PosX": 0, "_PosY": 0, "ObjectType": "StringTestNode"}, {"_Node_Name": "Node5", "_NodeId": null, "_InputSockets": [{"_DataType": "String", "_Name": "Output", "_Required": false, "_DBObjectID": null, "_ArgumentNumber": 1, "_OwnerNodeId": null, "ObjectType": "NodeIOSocket"}], "_OutputSockets": [{"_DataType": "String", "_Name": "Output", "_Required": false, "_DBObjectID": null, "_ArgumentNumber": 1, "_OwnerNodeId": null, "ObjectType": "NodeIOSocket"}], "_DBObjectID": null, "_ModuleId": null, "_PosX": 0, "_PosY": 0, "ObjectType": "StringTestNode"}, {"_Value": 23, "_NodeId": null, "_InputSockets": [{"_DataType": "Integer", "_Name": "Output", "_Required": false, "_DBObjectID": null, "_ArgumentNumber": 0, "_OwnerNodeId": null, "ObjectType": "NodeIOSocket"}], "_DataType": "Integer", "_OutputSockets": [], "_DBObjectID": null, "_PosX": 0, "_PosY": 0, "ObjectType": "ValueNode"}], "_Links": [{"_Out_Node_Id": null, "_In_Socket_Num": 1, "_In_Node_Id": null, "_DBObjectID": null, "_Out_Socket_Num": 1, "ObjectType": "Link"}, {"_Out_Node_Id": null, "_In_Socket_Num": 2, "_In_Node_Id": null, "_DBObjectID": null, "_Out_Socket_Num": 1, "ObjectType": "Link"}, {"_Out_Node_Id": null, "_In_Socket_Num": 1, "_In_Node_Id": null, "_DBObjectID": null, "_Out_Socket_Num": 1, "ObjectType": "Link"}, {"_Out_Node_Id": null, "_In_Socket_Num": 1, "_In_Node_Id": null, "_DBObjectID": null, "_Out_Socket_Num": 1, "ObjectType": "Link"}], "_DBObjectID": null, "_AlgorithmName": "UntitledAlgorithm", "ObjectType": "Algorithm"}')

# Get all algos
# db.get_all_algorithms()

# Test return data
# algo = db.get_algorithm("1")
# print algo["_AlgorithmName"]


# create table algorithm(
# id int auto_increment primary key,
# name varchar(255),
# version int,
# userid int,
# jsonstr mediumtext
# );
