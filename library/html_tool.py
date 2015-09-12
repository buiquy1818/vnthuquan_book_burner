__author__ = 'quybvs'

def decode_param_to_dict(params_string):
    if isinstance(params_string, str) or isinstance(params_string, unicode):
        params_list_of_str = params_string.split('&')
        params_list = {}
        for param_str in params_list_of_str:
            param_name, param_value = param_str.split('=')
            params_list[param_name] = param_value
        return params_list
    else:
        return None
