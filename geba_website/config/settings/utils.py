import os

def get_env_variable(var_name):
    try:
        # return os.environ[var_name]
        return os.environ.get(var_name)
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        print(error_msg)
        raise KeyError(error_msg)
    except:
        print('there was an error finding environment variable!')