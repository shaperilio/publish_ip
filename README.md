# publish_ip
Python script to publish your external IP somewhere, e.g. Dropbox.

As-is, it will alter an OpenVPN config file and copy it into a folder in a Dropbox business account.

## Instructions
 - Create a Python 3.8+ virtual environment (or don't).
 - Install requirements.
 - Execute [./src/runner.py](src/runner.py), e.g.
  ```
 python3 ./src/runner.py my_open_vpn_config.ovpn my_dropbox_subfolder/my_open_vpn_config.ovpn
 ````
   By default, it will check if your IP has changed every 10 minutes. Use `--interval_minutes` to
   change that.