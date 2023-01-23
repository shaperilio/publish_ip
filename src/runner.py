import shutil
import time

from ip_getters import get_ip_ifconfig_me
from ovpn import check_and_replace_ip
from dropbox import get_dropbox_path_business
from output import log, seconds2pretty

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('source_ovpn_file', nargs=1, default=[],
                        help='Location of OpenVPN configuration file in which to '
                        'record the IP address. Note that this file is overwritten '
                        'with the updated IP address!')
    parser.add_argument('dest_ovpn_file', nargs=1, default=[],
                        help='Location within your Dropbox business folder into which the '
                        'updated file should be copied.')
    parser.add_argument('-i', '--interval_minutes', default='10', action='store',
                        help='Number of minutes to wait between IP address checks.')
    args = parser.parse_args()
    config_file = args.source_ovpn_file[0]
    dropbox_loc = args.dest_ovpn_file[0]
    interval_sec = float(args.interval_minutes) * 60
    while True:
        try:
            my_ip = get_ip_ifconfig_me()
            if check_and_replace_ip(config_file, my_ip):
                dropbox = get_dropbox_path_business()
                pub_path = f'{dropbox}/{dropbox_loc}'
                shutil.copyfile(config_file, pub_path)
                log(f'IP address updated to {my_ip}; file saved at {pub_path}.')
            else:
                log(f'IP address is still {my_ip}; no update necessary.')

        except Exception as e:
            log(f'Exception encountered:\n\n{e}\n\nRetrying in 1 minute.')
            time.sleep(60)
            continue
        log(f'Waiting {seconds2pretty(interval_sec)} until next check.')
        time.sleep(interval_sec)
