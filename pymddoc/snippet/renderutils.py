import typing

def split_map_join(func: typing.Callable[[str],str], text: str, line_end: str = '\n') -> str:
    '''Split string by line, apply func, and join back together.'''
    return line_end.join([func(l) for l in text.split(line_end)])


def split_filter_join(func: typing.Callable[[str],bool], text: str, line_end: str = '\n') -> str:
    '''Split string by line, apply func, and join back together.'''
    return line_end.join([l for l in text.split(line_end) if func(l)])


def map_line(func: typing.Callable[[str],typing.Any], text: str, line_end: str = '\n') -> typing.List[typing.Any]:
    '''Split string by line and apply func, returning a list.'''
    return [func(l) for l in text.split(line_end)]


