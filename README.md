Symbiosis Realtime DNS
======================

By deafult Symbiosis updates DNS every hour.

For a small server with no many changes this is a long time.

This deamon is designed to trigger updates as soon as files are changed.

Usage
-----
1. Put dns-watcher.py in /usr/local/bin/dns-watcher
2. Put init-script in /etc/init.d/dns-watcher
3. Make /usr/local/bin/dns-watcher + /etc/init.d/dns-watcher executable
4. Configure the service to start automatically (update-rc.d dns-watcher
   defaults)
5. Put monit-script in /etc/symbiosis/monit.d/dns-watcher
6. Start dns-watcher (service dns-watcher start)
7. Watch /var/log/dns-watcher.log
8. Edit a dns config file /src/example.com/config/dns/example.com.txt and it
   picked up in real time.

Note: monit will keep restarting dns-watcher for us.
