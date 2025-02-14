import yaml
_conf = {} # global config dict

# key 为点分符分割的字符串， 
def get(key:str):
    return _get_conf_item(key, _conf) 

def _get_conf_item(key, conf):
    if "." not in key:
        return conf.get(key, None)
    else:
        key_list = key.split(".")
        return _get_conf_item(key_list[1:], conf[key_list[0]])

def merge_rb_config(conf):
    global _conf
    _conf.update(conf)