# Hooks client for Raspberry Pi

|Branch|Travis|
|------|:------:|
|master|[![Build Status](https://img.shields.io/travis/jenyayel/hooks-client-rpi/master.svg)](https://travis-ci.org/jenyayel/hooks-client-rpi)|
|dev   |[![Build Status](https://img.shields.io/travis/jenyayel/hooks-client-rpi/dev.svg)](https://travis-ci.org/jenyayel/hooks-client-rpi)|

## Application Configurations

The only prerequisite is to have environment variables which defines the endpoint of API and a security token.

Those can be defined either simply in `/etc/environment`:
```bash
HOOKSCLIENTRPI_ENDPOINT="[endpoint URI]"
HOOKSCLIENTRPI_TOKEN="[authorization token]"
```

## Running as shell application

Since GPIO requires elevations, environment variables needs to be added for sudo
```bash
sudo visudo
```
then add:
```bash
Defaults	env_keep +="HOOKSCLIENTRPI_ENDPOINT"
Defaults	env_keep +="HOOKSCLIENTRPI_TOKEN"
```

Deploy the `/` folder into Raspberry Pi and start client from terminal:
```bash
sudo python hooks_listener
```

## Running as daemon service

>The client daemonized using [Stephen's](http://blog.scphillips.com/posts/2013/07/getting-a-python-script-to-run-in-the-background-as-a-service-on-boot/) fairly painless trick.

Assuming that the project cloned into `/home/pi/hooks-client-rpi` (this can me changed in `hooksclientrpi.sh`), copy init script to `/etc/init.d`:

```bash
sudo cp hooksclientrpi.sh /etc/init.d
```

Make sure that both `hooksclientrpi.sh` and `service.py` are executable:

```bash
sudo chmod 755 /etc/init.d/hooksclientrpi.sh
chmod 755 service.py
```

At this stage you can start and stop service:
```bash
sudo /etc/init.d/hooksclientrpi.sh start
sudo /etc/init.d/hooksclientrpi.sh status
sudo /etc/init.d/hooksclientrpi.sh stop
```

See log file at `/tmp/hooks-client-rpi.log` for info or errors.

Now, add it to boot sequence:
```bash
sudo update-rc.d hooksclientrpi.sh defaults
```
