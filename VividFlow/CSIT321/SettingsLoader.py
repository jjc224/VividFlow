import os
import json

class SettingsLoader:
    SettingsFilename = "config.json"

    @staticmethod
    def load_settings():
        config_file = open("config.json")
        if config_file is None:
            print "Unable to open config file when connecting to database"
            return
        Settings = json.load(config_file)
        config_file.close()
        SettingsLoader.add_runtime_settings(Settings)
        SettingsLoader.normalize_paths(Settings)
        return Settings

    @staticmethod
    def normalize_paths(indict):
        for key,value in indict.items():
            if isinstance(value, dict):
                SettingsLoader.normalize_paths(value)
            else:
                if str(key).startswith("path_"):
                    indict[key] = os.path.normpath(value)

    @staticmethod
    def add_runtime_settings(Settings):
        base_dir = ""
        static_dir = ""
        # path settings
        if "system" not in Settings:
            Settings["system"] = {}
        if "jobs" not in Settings:
            Settings["jobs"] = {}
        if "resources" not in Settings:
            Settings["resources"] = {}

        Settings["system"]["path_abs_root"] = os.path.dirname(os.path.realpath(__file__))
        base_dir = Settings["system"]["path_abs_root"]
        print "Base directory: " + base_dir

        Settings["system"]["path_abs_static"] = os.path.join(base_dir, "static")
        static_dir = Settings["system"]["path_abs_static"]
        print "Static directory: " + static_dir

        # job settings
        Settings["jobs"]["path_abs_working"] = os.path.join(base_dir, Settings["jobs"]["path_rel_working"])
        Settings["jobs"]["path_abs_output"] = os.path.join(static_dir, Settings["jobs"]["path_rel_output"])

        # module settings
        Settings["modules"]["path_abs_code"] = os.path.join(base_dir, Settings["modules"]["path_rel_code"])
        Settings["modules"]["path_abs_executables"] = os.path.join(base_dir, Settings["modules"]["path_rel_executables"])
        Settings["modules"]["path_abs_vividflow_lib_dir"] = os.path.join(static_dir, Settings["modules"]["path_rel_vividflow_lib_dir"])

        # resources settings
        Settings["resources"]["path_abs"] = os.path.join(static_dir, Settings["resources"]["path_rel"])

    @staticmethod
    def print_settings_dict(indict):
        for key,value in indict.items():
            if isinstance(value, dict):
                print "==================="
                print key
                print "==================="
                SettingsLoader.print_settings_dict(value)
            else:
                print key + ": " + str(value)

    @staticmethod
    def print_settings():
        SettingsLoader.print_settings_dict(Settings)

    @staticmethod
    def save_settings(filename, Settings):
        try:
            config_file = open(filename,"w")
            if config_file is None:
                print "Unable to open config file when connecting to database"
                return
            json.dump(Settings, config_file)
            config_file.close()
        except IOError:
            pass
