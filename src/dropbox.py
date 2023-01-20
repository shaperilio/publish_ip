import os
import json
from typing import Optional


def _get_dropbox_config_location() -> Optional[str]:
    """
    Returns the path to the JSON file from which the Dropbox folder location can
    be established. If the JSON file is not found, returns None.
    """
    # Windows
    json_path = 'Dropbox\\info.json'
    path = f"{os.getenv('LOCALAPPDATA')}\\{json_path}"
    if os.path.exists(path):
        return path
    # linux
    path = os.path.expanduser('~/.dropbox/info.json')
    if os.path.exists(path):
        return path
    return None


def get_dropbox_path_business() -> str:
    """
    Returns the path to the business Dropbox account running on the machine.
    Specifically speaking, it opens Dropbox's "info.json" file and returns the
    contents of "root_path" under the "business" key.

    Raises
    ------
    RuntimeError
        If the Dropbox path can't be established.

    Returns
    -------
    str:
        The absolute path to the Dropbox folder
    """
    # See info here:
    # https://help.dropbox.com/installs-integrations/desktop/locate-dropbox-folder

    def read_json(path):
        if not os.path.exists(path):
            return None
        with open(path, 'r') as f:
            dropbox = json.loads(f.read())
        if 'business' in dropbox.keys() and 'root_path' in dropbox['business'].keys():
            return dropbox['business']['root_path']
        return None

    json_path = _get_dropbox_config_location()
    if json_path is None:
        raise RuntimeError('Dropbox is not installed.')

    result = read_json(json_path)
    if result is None:
        raise RuntimeError('Cannot establish Dropbox folder path.')

    return result
