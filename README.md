# do-ddns

Simple script that updates DNS records via Digital Ocean's HTTP API

## Installation

### Dependencies

* `requests`

### Instructions

1. Clone the project
2. Move files to a sensible location
3. Set your details and token in the file
4. `chmod +x updater.py`
5. Install `systemd` service and timer to `/etc/systemd/system`
6. Start timer and service

    ```
    sudo systemctl enable --now do-ddns-updater.timer
    ```

7. Confirm the timer is installed correctly: `systemctl list-timers`

## License

MIT

## Credits

Matias Silva, 2021