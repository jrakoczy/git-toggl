import yaml

SETTINGS_PATH = 'settings.yaml' 

def save_settings(git_dir, handle, api_key, pid):
    data = {
        'directory' : git_dir,
        'handle' : handle,
        'key' : api_key,
        'pid' : pid 
     }

    with open(SETTINGS_PATH, 'w+') as sfile:
        sfile.write(yaml.dump(data, default_flow_style=True))
        
def load_settings():
    data = {}

    with open(SETTINGS_PATH, 'r') as sfile:
        data = yaml.load(sfile)

    return data
        
