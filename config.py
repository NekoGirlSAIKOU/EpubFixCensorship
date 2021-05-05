import os

PROGRAM_PATH = os.path.split(os.path.realpath(__file__))[0]

def init_config(config:dict):
    config['element_tags'] = config.get('element_tags',['p','div'])
    config['element_strings'] = config.get('element_strings',['*'])
    config['check_element_by_rules'] = config.get('check_element_by_rules',False)

    config['language'] = config.get('language', 'zh-CN')