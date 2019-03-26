import copy
import yaml
import sys

GLB_CONFIG_DEFAULT = {
    'verbose': True,
    'debug': True
}

JOB_CONFIG_DEFAULT = {
    'name': 'default',
    'delta': 31,
    'granularity': 'daily',
    'refresh': 43200,
    'metric': 'UnblendedCost',
    'credentials': {},
    'metric_labels': {}
}

CONFIG_TEMPLATE = {
    'global': GLB_CONFIG_DEFAULT,
    'jobs': []
}


def _handle_global_section(glb):
    block = copy.deepcopy(GLB_CONFIG_DEFAULT)
    # deleting unnecessary config items
    for key in glb.keys():
        if key not in GLB_CONFIG_DEFAULT.keys():
            print('DEBUG: removing key {} from \
                configuration in global section').format(key)
            glb.pop(key)
    block.update(glb)
    return block


def _handle_job_section(job):
    block = copy.deepcopy(JOB_CONFIG_DEFAULT)
    for key in JOB_CONFIG_DEFAULT.keys():
        try:
            block[key] = job[key]
        except KeyError:
            pass
    return block


def load_config(filepath):
    data = {}
    try:
        with open(filepath, 'r') as fl:
            raw = fl.read()
            config = yaml.load(raw)
            data['global'] = _handle_global_section(config['global'])
            data['jobs'] = [_handle_job_section(j) for j in config['jobs']]
            return data
    except Exception as e:
        print('an error occured')
        print(e)
        sys.exit(2)
