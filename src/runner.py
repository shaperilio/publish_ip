import time

from ip_getters import get_ip_ifconfig_me
from ovpn import check_and_replace_ip
from publishers import publish
from output import log, seconds2pretty, get_traceback_str

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('source_ovpn_file', nargs=1, default=[],
                        help='Location of OpenVPN configuration file in which to '
                        'record the IP address. Note that this file is overwritten '
                        'with the updated IP address!')
    parser.add_argument('dest_ovpn_file', nargs=1, default=[],
                        help='Location to which the altered profile will be published. Currently '
                        'two endpoints are supported. If this arugment starts with "dropbox::", '
                        'the file is copied to a subdirectory of your Dropbox business folder. '
                        'Otherwise, the path is assumed to be local.')
    parser.add_argument('-i', '--interval_minutes', default='10', action='store',
                        help='Number of minutes to wait between IP address checks.')
    args = parser.parse_args()
    config_file = args.source_ovpn_file[0]
    publish_loc = args.dest_ovpn_file[0]
    interval_sec = float(args.interval_minutes) * 60
    while True:
        try:
            my_ip = get_ip_ifconfig_me()
            if check_and_replace_ip(config_file, my_ip):
                config_changed = True
                log(f'IP address updated to {my_ip}.')
            else:
                config_changed = False
                log(f'IP address is still {my_ip}; no update necessary.')
            publish(config_file, publish_loc, config_changed)
        except Exception as e:
            log(f'`{e.__class__.__name__}` encountered:\n\n'
                f'{e}\n\nTraceback:\n{get_traceback_str()}\n\n'
                'Retrying in 1 minute.')
            time.sleep(60)
            continue
        log(f'Waiting {seconds2pretty(interval_sec)} until next check.')
        time.sleep(interval_sec)
