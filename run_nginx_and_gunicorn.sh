#! /usr/bin/bash

# as sudo!

nginx -c '/home/oleg/1_Технопарк/web/AskMax/nginx.conf'

(cd '/home/oleg/1_Технопарк/web/AskMax/' && gunicorn --workers=8 --bind=127.0.0.1:8000 AskMax.wsgi)

# https://www.digitalocean.com/community/tutorials/how-to-use-systemctl-to-manage-systemd-services-and-units
# http://docs.gunicorn.org/en/stable/deploy.html
# http://www2.kangran.su/%7Ennz/pub/s4a/s4a_latest.pdf
# https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/system_administrators_guide/sect-managing_services_with_systemd-unit_files
