import re


class ConfigParsingError(Exception):
    pass


def check_and_replace_ip(config_file: str, new_ip: str) -> bool:
    """
    Replaces the IP address in the OpenVPN configuration file at `config_file` with the value in
    `new_ip`, if they don't match. The file is overwritten without backup.

    Raises
    ------
    ConfigParsingError:
        If the IP address cannot be replaced.

    Parameters
    ----------
    config_file : str
        Path to the OpenVPN configuration file
    new_ip : str
        The IP address to put in said file.

    Returns
    -------
    bool:
        True if the file was updated; False if `new_ip` matches the IP address in the file.
    """

    with open(config_file, 'r') as f:
        config = f.read()

    match = re.search(r'remote \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', config, re.MULTILINE)
    if match is None:
        raise ConfigParsingError('Cannot find a line containing "remote <IPv4 address>".')
    remote_line = match[0]
    ip_address = remote_line.split(' ')[1]
    if ip_address == new_ip:
        return False
    else:
        new_config = config.replace(remote_line, f'remote {new_ip}')
        with open(config_file, 'w') as f:
            f.write(new_config)
        return True
