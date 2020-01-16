import re


GROUP_NAME_PATTERN = re.compile(r'\?P<(?P<group_name>\w+)>')


def extract(pattern, source):
    '''
    Extract matched string specified by @pattern from @source 
    The @pattern must contains a named group.
    '''
    matched = re.search(pattern, source)
    if matched is None:
        return None

    g_name = GROUP_NAME_PATTERN.search(pattern)
    if g_name is None:
        raise Exception(f'Regex r\'{pattern}\' must contains named group')

    group_name = g_name.group('group_name')
    return matched.group(group_name)


def multi_match(pattern, source):
    '''
    Extract matched string specified by @pattern from @source 
    There are more than one match.
    '''
    return re.findall(pattern, source)
