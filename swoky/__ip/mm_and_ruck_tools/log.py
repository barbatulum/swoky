import inspect
import logging


logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)
# create file handler that logs debug and higher level messages
fh = logging.FileHandler('spam.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warning('warn message')
logger.error('error message')
logger.critical('critical message')

_LOG_LEVELS = {
    'debug': 10,
    'info': 20,
    'warning': 30,
    'error': 40,
    'critical': 50
}
_MSG_PARAMS = {
    'heading': {
        'debug': 'h3',
        'info': 'h3',
        'warning': 'h2',
        'error': 'h1',
        'critical': 'h1'
    },
    'color': {
        'debug': 'green',
        'info': 'green',
        'warning': 'yellow',
        'error': 'red',
        'critical': 'red'
    }
}

from six import string_types

from maya import cmds


def log(
        msg, logger, level='info',
        default_heading='h3', default_color='green',
        override_message=None, color=None, heading=None
):
    if isinstance(level, (int, float)):
        level = _LOG_LEVELS.get(level, 'info')
    # In view message
    in_view_msg = override_message
    if not override_message:
        in_view_msg = '<{heading}><font color="{color}">{msg}</{heading}>'.format(
            heading=heading or _MSG_PARAMS.get('heading', {}).get(level, default_heading),
            color=color or _MSG_PARAMS.get('color', {}).get(level, default_color),
            msg=msg,
        )

    cmds.inViewMessage(in_view_msg)

    try:
        frame = inspect.getouterframes(inspect.currentframe())[1]
    except IndexError:
        frame = None

    log_call = getattr(logger, level)
    log_msg = msg
    if frame:
        msg = 'ruck_tools', frame.function

    log_call()
    print('Function name: ', frame.function)
    print('File name:', __name__)
    caller = inspect.currentframe().f_back
    if caller:
        print('Caller:', caller.f_globals['__name__'])


def test():
    log()