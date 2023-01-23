from typing import Optional
import math
from datetime import datetime
import sys
from traceback import StackSummary, extract_tb
from types import TracebackType


def log(msg: str):
    """
    Simple print statement with timestamp.
    """
    ts = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f')[:-3]
    ts = f'[{ts}]'
    tab = ' '*(len(ts)+1)
    for n, line in enumerate(msg.split('\n')):
        if n == 0:
            print(f'{ts}: {line}')
        else:
            print(f'{tab} {line}')


def get_traceback_str(traceback: Optional[TracebackType] = None) -> str:
    if traceback is None:
        _, _, traceback = sys.exc_info()
    tb_parts = [item.strip() for item in StackSummary.from_list(extract_tb(traceback)).format()]
    return '\n'.join(tb_parts)


def seconds2pretty(seconds: float, show_ms: bool = True, short: bool = False) -> str:
    """
    Convert seconds to a "pretty" string, i.e. labeled with "hours", "minutes",
    etc. (with proper singular and plural!).

    Parameters
    ----------
    seconds: float
        Number of seconds to make the string for.

    show_ms: bool = True
        False to never show milliseconds. If True, milliseconds are shown for
        times lower than 1 minute; deciseconds shown for up to 1 hour, and
        seconds shown beyond that.

    short: bool = False
        True to show short descriptors, e.g. "s" instead of "seconds".


    Returns
    -------
    str

    Examples
    --------
    >>> seconds2pretty(1.2345)
    '1.235 seconds'
    >>> seconds2pretty(60 + 12.345)
    '1 minute, 12.3 seconds'
    >>> seconds2pretty(60*60 + 60*40 + 1.2345)
    '1 hour, 40 minutes, 1 second'
    >>> seconds2pretty(1.2345, show_ms=False)
    '1 second'

    The maximum clock resolution is days
    >>> seconds2pretty(60*60*123 + 60*40 + 1.2345)
    '5 days, 3 hours, 40 minutes, 1 second'

    >>> seconds2pretty(60*60*123 + 60*40 + 1.2345, short=True)
    '5 d, 3 h, 40 m, 1 s'

    'nan' is returned for `nan`.
    >>> seconds2pretty(float('nan'))
    'nan'

    No funny times! rounding is taken care of.
    >>> seconds2pretty(59.999 + 60 * 59)  # nearly an hour
    '1 hour, 0 minutes, 0.0 seconds'
    """
    if math.isnan(seconds):
        return 'nan'

    if short:
        s = 's'
        m = 'm'
        h = 'h'
        d = 'd'
    else:
        s = 'second'
        m = 'minute'
        h = 'hour'
        d = 'day'

    def plural(val):
        if short:
            return ''
        return '' if val == 1 else 's'

    r = seconds
    #             days ---------------|
    #            hours ----------|    |
    #            minutes ----|   |    |
    days = int(math.floor(r / 60 / 60 / 24))
    r -= days * 24 * 60 * 60
    hours = int(math.floor(r / 60 / 60))
    r -= hours * 60 * 60
    minutes = int(math.floor(r / 60))
    r -= minutes * 60
    seconds = r

    if show_ms:
        prec = 1000
        if minutes > 0:
            prec = 10  # show only 10ths of a second if time is greater than 1 minute.
        if hours > 0:
            prec = 1  # don't show any fraction of a second if over an hour.
    else:
        prec = 1

    # Round and carry the 1.
    seconds = math.floor(seconds * prec + 0.5) / prec

    if seconds >= 60:
        minutes += 1
        seconds -= 60
    if minutes >= 60:
        hours += 1
        minutes -= 60
    if hours >= 24:
        days += 1
        hours -= 24

    result = ''
    if days > 0:
        result += f'{days:d} ' + d + plural(days)
    if result != '' or hours > 0:
        if result != '':
            result += ', '
        result += f'{hours:d} ' + h + plural(hours)
    if result != '' or minutes > 0:
        if result != '':
            result += ', '
        result += f'{minutes:d} ' + m + plural(minutes)
    if seconds > 0:
        if result != '':
            result += ', '
        sec_txt = '{:.{ndec}f}'.format(seconds, ndec=len(str(prec)) - 1)
        result += f'{sec_txt} ' + s + plural(seconds)

    return result
