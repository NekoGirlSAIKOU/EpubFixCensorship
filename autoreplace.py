from typing import List, Tuple, Dict

from lxml import etree

try:
    import regex as re
except ImportError:
    import re


class AutoReplace:
    def __init__(self, *, rules: List[dict] = [], replace_histories:Dict[str,str] = {}):
        self.rules = rules
        self.replace_histories = replace_histories

    def replace_text(self, text) -> List[Tuple[str, str]]:
        r = [('origin', text)]

        new_text = self.replace_histories.get(text)
        if new_text is not None:
            r.append(('history',new_text))

        for replace_rule in self.rules:
            replace_rule['name'] = replace_rule.get('name', replace_rule.get('replaceSummary', ''))
            replace_rule['pattern'] = replace_rule.get('pattern', replace_rule.get('regex'))
            replace_rule['replacement'] = replace_rule.get('replacement', '')
            replace_rule['isEnabled'] = replace_rule.get('isEnabled', replace_rule.get('enable', True))
            if replace_rule['name'] == '' or replace_rule['name'] is None:
                replace_rule['name'] = f'{replace_rule["pattern"]} to {replace_rule["replacement"]}'

            if replace_rule['isEnabled'] is False:
                continue

            if replace_rule.get('isRegex', False):
                try:
                    r = re.findall(replace_rule['pattern'], text)
                    new_text = re.sub(replace_rule['pattern'], replace_rule['replacement'], text, count=0, flags=0)
                    if new_text != text:
                        r.append((replace_rule['name'], new_text))
                except Exception as e:
                    replace_rule['isEnabled'] = False
                    continue
            else:
                new_text = text.replace(replace_rule['pattern'], replace_rule['replacement'])
                if new_text != text:
                    r.append((replace_rule['name'], new_text))
        return r
