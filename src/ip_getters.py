import urllib3


def get_ip_ifconfig_me() -> str:
    """
    Returns the external IP address of this machine by sending an HTTP request to
    https://ifconfig.me.

    Returns
    -------
    str
        IPv4 address as a string.
    """

    http = urllib3.PoolManager()
    r = http.request('GET', 'https://ifconfig.me/')
    ip = r.data.decode('utf-8')
    return ip
