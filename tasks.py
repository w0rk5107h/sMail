import os
import sys
from text import *
from helper import *
from color import *


# init log
def init_log():
    log_init()

# clear screen
def clear_screen():
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')

# print welcome text_hellu everynyn :)(bahahhh)
def print_welcome_text():
    print(f'{Color.fg.darkgrey}{WELCOME_TEXT}{Color.reset}')

# check os
def check_os():
    INSTALLATION_PROGRESS = get_installation_progress()
    if check_os.__name__ not in INSTALLATION_PROGRESS:

        print(f'{Color.fg.blue}[.] CHECKING [OS]{Color.reset}')
        if os.name != 'posix':
            print(f'{Color.fg.red}[-] This installer is not compatible with windows, it only works with debian 12{Color.reset}')
            sys.exit()
        
        try:
            with open('/etc/os-release') as file:
                data = file.read()
                if 'Debian GNU/Linux 12 (bookworm)' not in data:
                    print(f'{Color.bg.red}[-] This installer only works with debian 12 (bookworm){Color.reset}')
                    sys.exit()
        except Exception as e:
            print(f'{Color.fg.red}[-] Some error occured while checking linux version: {Color.reset}')
            print(f'{Color.bg.red}{str(e)}{Color.reset}')
            sys.exit()

        print(f'{Color.fg.green}[+] [OS] OK{Color.reset}')
        
        set_installation_progress(check_os.__name__)

# check user
def check_user():
    print(f'{Color.fg.blue}[.] CHECKING [USER]{Color.reset}')
    if os.getuid():
        print(f'{Color.bg.red}[-] Run this with sudo or as root{Color.reset}')
        sys.exit()
    print(f'{Color.fg.green}[+] [USER] OK{Color.reset}')

# collect variables
def collect_variables():
    INSTALLATION_PROGRESS = get_installation_progress()
    if collect_variables.__name__ not in INSTALLATION_PROGRESS:

        print(f'{Color.fg.blue}[.] COLLECTING [VARIABLES]{Color.reset}')
        print(f'{Color.fg.cyan}[>] {Color.reset}{Color.bg.cyan}SERVICE_NAME{Color.reset}')
        SERVICE_NAME = input(f'{Color.fg.cyan}{SERVICE_NAME_INPUT_MESSAGE}{Color.reset}')
        print(f'{Color.fg.cyan}[>] {Color.reset}{Color.bg.cyan}SERVER_FQDN{Color.reset}')
        SERVER_FQDN = input(f'{Color.fg.cyan}{SERVER_FQDN_INPUT_MESSAGE}{Color.reset}')
        print(f'{Color.fg.cyan}[>] {Color.reset}{Color.bg.cyan}MAIL_DN{Color.reset}')
        MAIL_DN = input(f'{Color.fg.cyan}{MAIL_DN_INPUT_MESSAGE}{Color.reset}')
        print(f'{Color.fg.cyan}[>] {Color.reset}{Color.bg.cyan}DKIM_SELECTOR{Color.reset}')
        DKIM_SELECTOR = input(f'{Color.fg.cyan}{DKIM_SELECTOR_INPUT_MESSAGE}{Color.reset}')
        print(f'{Color.fg.cyan}[>] {Color.reset}{Color.bg.cyan}SERVICE_LOGO{Color.reset}')
        input(f'{Color.fg.cyan}{SERVICE_LOGO_INPUT_MESSAGE}{Color.reset}')
        
        set_config({
            'SERVICE_NAME': SERVICE_NAME,
            'SERVER_FQDN': SERVER_FQDN,
            'MAIL_DN': MAIL_DN,
            'DKIM_SELECTOR': DKIM_SELECTOR
        })
        print(f'{Color.fg.green}[+] [VARIABLES] COLLECTED{Color.reset}')

        set_installation_progress(collect_variables.__name__)

# install packages
def install_packages():
    INSTALLATION_PROGRESS = get_installation_progress()
    if install_packages.__name__ not in INSTALLATION_PROGRESS:

        print(f'{Color.fg.blue}[.] INSTALLING [PACKAGES]{Color.reset}')
        CONFIG = get_config()
        commands = [
            ['apt -y install debconf-utils', '[-] Error while installing `debconf-utils`:'],
            ['echo "postfix postfix/main_mailer_type select Internet Site" | debconf-set-selections', '[-] Error while setting debconf selection for postfix:'],
            [f'echo "postfix postfix/mailname string {CONFIG["SERVER_FQDN"]}" | debconf-set-selections', '[-] Error while setting debconf selection for postfix:'],
            ['echo "roundcube-core roundcube/dbconfig-install boolean false" | debconf-set-selections', '[-] Error while setting debconf selection for roundcube:'],
            ['apt install -y mariadb-server postfix postfix-mysql apache2 php rspamd redis-server swaks mutt certbot dovecot-mysql dovecot-pop3d dovecot-imapd dovecot-managesieved dovecot-lmtpd ca-certificates rsyslog python3-certbot-apache roundcube roundcube-plugins roundcube-plugins-extra roundcube-mysql dnsutils', '[-] Error while installing reqired packages:']
        ]
        for command in commands:
            _ = run_command(command[0], command[1])
        print(f'{Color.fg.green}[+] [PACKAGES] INSTALLED{Color.reset}')
        
        set_installation_progress(install_packages.__name__)

# setup http site
def setup_http_site():
    INSTALLATION_PROGRESS = get_installation_progress()
    if setup_http_site.__name__ not in INSTALLATION_PROGRESS:

        print(f'{Color.fg.blue}[.] SETTING UP [HTTP SITE]{Color.reset}')
        CONFIG = get_config()
        create_new_file(
            f'/etc/apache2/sites-available/{CONFIG["SERVER_FQDN"]}-http.conf',
            APACHE_HTTP_VHOST_FILE_CONTENT.replace('##SERVER_FQDN##', CONFIG['SERVER_FQDN'])
        )

        commands = [
            [f'mkdir /var/www/{CONFIG["SERVER_FQDN"]}', f'[-] Error while creating directory `/var/www/{CONFIG["SERVER_FQDN"]}`:'],
            [f'chown www-data:www-data /var/www/{CONFIG["SERVER_FQDN"]}', f'[-] Error while change owner of `/var/www/{CONFIG["SERVER_FQDN"]}`:'],
            ['service apache2 start', '[-] Error while starting apache2 service:'],
            ['a2enmod rewrite', '[-] Error while enabling apache2 rewrite mod:'],
            [f'a2ensite {CONFIG["SERVER_FQDN"]}-http', f'[-] Error while enabling apache2 site `{CONFIG["SERVER_FQDN"]}-http`:'],
            ['service apache2 restart', '[-] Error while restarting apche2 service:']
        ]
        for command in commands:
            _ = run_command(command[0], command[1])
        print(f'{Color.fg.green}[+] [HTTP SITE] SETUP DONE{Color.reset}')

        set_installation_progress(setup_http_site.__name__)

# get ssl cert
def get_ssl_cert():
    INSTALLATION_PROGRESS = get_installation_progress()
    if get_ssl_cert.__name__ not in INSTALLATION_PROGRESS:

        print(f'{Color.fg.blue}[.] REQUESTING [SSL CERTIFICATE]{Color.reset}')
        CONFIG = get_config()
        command = [
            f'certbot --apache --non-interactive --apache-le-vhost-ext "s.conf" --agree-tos --register-unsafely-without-email --no-redirect --domains {CONFIG["SERVER_FQDN"]}',
            f'[-] Error while getting ssl certificate for `{CONFIG["SERVER_FQDN"]}`'
        ]
        _ = run_command(command[0], command[1])
        append_to_file(
            '/etc/letsencrypt/cli.ini',
            'post-hook = systemctl restart postfix dovecot apache2'
        )
        print(f'{Color.fg.green}[+] [SSL CERTIFICATE] REQUESTED{Color.reset}')

        set_installation_progress(get_ssl_cert.__name__)

# setup https site
def setup_https_site():
    INSTALLATION_PROGRESS = get_installation_progress()
    if setup_https_site.__name__ not in INSTALLATION_PROGRESS:

        print(f'{Color.fg.blue}[.] SETTING UP [HTTPS SITE]{Color.reset}')
        CONFIG = get_config()
        create_new_file(
            f'/etc/apache2/sites-available/{CONFIG["SERVER_FQDN"]}-https.conf',
            APACHE_HTTPS_VHOST_FILE_CONTENT.replace('##SERVER_FQDN##', CONFIG['SERVER_FQDN'])
        )

        commands = [
            ['mkdir /var/www/html/autoconfig-mail', '[-] Error while creating the `autoconfig-mail`:'],
            ['a2enmod ssl', '[-] Error while enabling apache2 ssl mod:'],
            ['a2enmod proxy_http', '[-] Error while enabling apache2 proxy_http mod:'],
            [f'a2ensite {CONFIG["SERVER_FQDN"]}-https', f'[-] Error while enabling apache2 site `{CONFIG["SERVER_FQDN"]}-https`:'],
            ['service apache2 restart', '[-] Error while restarting apche2 service:']
        ]
        
        for command in commands:
            _ = run_command(command[0], command[1])

        create_new_file(
            '/var/www/html/autoconfig-mail/config-v1.1.xml',
            AUTOCONFIG_FILE_CONTENTS.replace('###SERVER_FQDN###', CONFIG['SERVER_FQDN']).replace('###SERVICE_NAME###', CONFIG['SERVICE_NAME']).replace('###MAIL_DN###', CONFIG['MAIL_DN'])
        )
        print(f'{Color.fg.green}[+] [HTTPS SITE] SETUP DONE{Color.reset}')

        set_installation_progress(setup_https_site.__name__)

# setup mysql database
def setup_mysql_database():
    INSTALLATION_PROGRESS = get_installation_progress()
    if setup_mysql_database.__name__ not in INSTALLATION_PROGRESS:

        print(f'{Color.fg.blue}[.] SETTING UP [SQL]{Color.reset}')
        MYSQL_mailserverdbadmin_PASSWORD = generate_random_password(30)
        MYSQL_mailserverdbuser_PASSWORD = generate_random_password(30)
        MYSQL_roundcubedbuser_PASSWORD = generate_random_password(30)
        MAIL_admin_PASSWORD = generate_random_password(30)
        MAIL_admin_PASSWORD_HASHED = hash_password(MAIL_admin_PASSWORD)
        CONFIG = get_config()
        set_config({
            'MYSQL_MAIL_DB': 'mailserverdb',
            'MYSQL_MAIL_DB_ADMIN': 'mailserverdbadmin',
            'MYSQL_mailserverdbadmin_PASSWORD': MYSQL_mailserverdbadmin_PASSWORD,
            'MYSQL_MAIL_DB_USER': 'mailserverdbuser',
            'MYSQL_mailserverdbuser_PASSWORD': MYSQL_mailserverdbuser_PASSWORD,
            'MYSQL_ROUNDCUBE_DB': 'roundcubedb',
            'MYSQL_ROUNDCUBE_DB_USER': 'roundcubedbuser',
            'MYSQL_roundcubedbuser_PASSWORD': MYSQL_roundcubedbuser_PASSWORD,
            'MAIL_admin_USER': f'admin@{CONFIG["MAIL_DN"]}',
            'MAIL_admin_PASSWORD': MAIL_admin_PASSWORD
        })
        queries = [
            [[f'mysql -u root', 'CREATE DATABASE mailserverdb;', 'quit'], '[-] Error while creating database:'],
            [[f'mysql -u root', 'CREATE DATABASE roundcubedb;', 'quit'], '[-] Error while creating database:'],
            [[f'mysql -u root', 'USE roundcubedb;', CREATE_ROUNDCUBE_DB_USER_QUERY.replace('##MYSQL_roundcubedbuser_PASSWORD##', MYSQL_roundcubedbuser_PASSWORD), 'FLUSH PRIVILEGES;', 'quit'], '[-] Error while creating databse user:'],
            [[f'mysql -u root', 'USE mailserverdb;', CREATE_MAIL_DB_ADMIN_QUERY.replace('##MYSQL_mailserverdbadmin_PASSWORD##', MYSQL_mailserverdbadmin_PASSWORD), 'FLUSH PRIVILEGES;', 'quit'], '[-] Error while creating databse admin:'],
            [[f'mysql -u root', 'USE mailserverdb;', CREATE_MAIL_DB_USER_QUERY.replace('##MYSQL_mailserverdbuser_PASSWORD##', MYSQL_mailserverdbuser_PASSWORD), 'FLUSH PRIVILEGES;', 'quit'], '[-] Error while creating databse user:'],
            [[f'mysql -u root', 'USE mailserverdb;', CREATE_virtual_domains_TABLE_QUERY, 'quit'], '[-] Error while creating table `virtual_domains`:'],
            [[f'mysql -u root', 'USE mailserverdb;', CREATE_virtual_users_TABLE_QUERY, 'quit'], '[-] Error while creating table `virtual_users`:'],
            [[f'mysql -u root', 'USE mailserverdb;', CREATE_virtual_aliases_TABLE_QUERY, 'quit'], '[-] Error while creating table `virtual_aliases`:'],
            [[f'mysql -u root', 'USE mailserverdb;', CREATE_INIT_DOMAIN_ENTRY_QUERY.replace('##MAIL_DN##', CONFIG["MAIL_DN"]), 'quit'], '[-] Error while creating init domain entry:'],
            [[f'mysql -u root', 'USE mailserverdb;', CREATE_INIT_USER_ENTRY_QUERY.replace('##MAIL_DN##', CONFIG["MAIL_DN"]).replace('##MAIL_admin_PASSWORD_HASHED##', MAIL_admin_PASSWORD_HASHED), 'quit'], '[-] Error while creating init user entry:'],
            [[f'mysql -u root', 'USE mailserverdb;', CREATE_INIT_ALIAS_ENTRY_QUERY.replace('##MAIL_DN##', CONFIG["MAIL_DN"]), 'quit'], '[-] Error while creating init alias entry:']
        ]

        for query in queries:
            _ = run_sql_query(query[0], query[1])
        print(f'{Color.fg.green}[+] [SQL] SETUP DONE{Color.reset}')

        set_installation_progress(setup_mysql_database.__name__)

# setup postfix for mysql
def setup_postfix_for_mysql():
    INSTALLATION_PROGRESS = get_installation_progress()
    if setup_postfix_for_mysql.__name__ not in INSTALLATION_PROGRESS:

        print(f'{Color.fg.blue}[.] SETTING UP [POSTFIX FOR MYSQL]{Color.reset}')
        CONFIG = get_config()
        files = [
            ['/etc/postfix/mysql-virtual-mailbox-domains.cf', POSTFIX_VIRTUAL_DOMAINS_FILE_CONTENT.replace('##MYSQL_mailserverdbuser_PASSWORD##', CONFIG['MYSQL_mailserverdbuser_PASSWORD'])],
            ['/etc/postfix/mysql-virtual-mailbox-maps.cf', POSTFIX_VIRTUAL_USERS_FILE_CONTENT.replace('##MYSQL_mailserverdbuser_PASSWORD##', CONFIG['MYSQL_mailserverdbuser_PASSWORD'])],
            ['/etc/postfix/mysql-virtual-alias-maps.cf', POSTFIX_VIRTUAL_ALIASES_FILE_CONTENT.replace('##MYSQL_mailserverdbuser_PASSWORD##', CONFIG['MYSQL_mailserverdbuser_PASSWORD'])],
            ['/etc/postfix/mysql-email2email.cf', POSTFIX_EMAIL_TO_EMAIL_FILE_CONTENT.replace('##MYSQL_mailserverdbuser_PASSWORD##', CONFIG['MYSQL_mailserverdbuser_PASSWORD'])]
        ]
        for file in files:
            create_new_file(file[0], file[1])
        
        commands = [
            ['postconf virtual_mailbox_domains=mysql:/etc/postfix/mysql-virtual-mailbox-domains.cf', '[-] Error while setting up virtual_mailbox_domains:'],
            ['postconf virtual_mailbox_maps=mysql:/etc/postfix/mysql-virtual-mailbox-maps.cf', '[-] Error while setting up virtual_mailbox_maps:'],
            ['postconf virtual_alias_maps=mysql:/etc/postfix/mysql-virtual-alias-maps.cf,mysql:/etc/postfix/mysql-email2email.cf', '[-] Error while setting up virtual_alias_maps:'],
            ['postconf smtpd_sender_login_maps=mysql:/etc/postfix/mysql-virtual-mailbox-maps.cf', '[-] Error while setting up smtpd_sender_login_maps:'],
            ['chgrp postfix /etc/postfix/mysql-*.cf', '[-] Error while changing group for "/etc/postfix/mysql-*.cf":'],
            ['chmod u=rw,g=r,o= /etc/postfix/mysql-*.cf', '[-] Error while changing permissions for "/etc/postfix/mysql-*.cf":']
        ]
        for command in commands:
            _ = run_command(command[0], command[1])
        print(f'{Color.fg.green}[+] [POSTFIX FOR MYSQL] SETUP DONE{Color.reset}')

        set_installation_progress(setup_postfix_for_mysql.__name__)

# setup dovecot    
def setup_dovecot():
    INSTALLATION_PROGRESS = get_installation_progress()
    if setup_dovecot.__name__ not in INSTALLATION_PROGRESS:

        print(f'{Color.fg.blue}[.] SETTING UP [DOVECOT]{Color.reset}')
        CONFIG = get_config()
        setup_dovecot_edit_files('/etc/dovecot/conf.d/10-auth.conf')
        setup_dovecot_edit_files('/etc/dovecot/conf.d/10-mail.conf')
        setup_dovecot_edit_files('/etc/dovecot/conf.d/10-master.conf')
        setup_dovecot_edit_files('/etc/dovecot/conf.d/10-ssl.conf')
        append_to_file(
            '/etc/dovecot/dovecot-sql.conf.ext',
            DOVECOT_SQL_CONF_FILE_CONTENT.replace('##MYSQL_mailserverdbuser_PASSWORD##', CONFIG['MYSQL_mailserverdbuser_PASSWORD'])
        )

        commands = [
            ['groupadd -g 5000 vmail', '[-] Error while adding group `vmail`:'],
            ['useradd -g vmail -u 5000 vmail -d /var/vmail -m', '[-] Error while adding user `vmail`:'],
            ['chown -R vmail:vmail /var/vmail', '[-] Error while changing permission of `/var/vmail`:'],
            ['chown root:root /etc/dovecot/dovecot-sql.conf.ext', '[-] Error while change ownder of file `/etc/dovecot/dovecot-sql.conf.ext`:'],
            ['chmod go= /etc/dovecot/dovecot-sql.conf.ext', '[-] Error while change permissions of file `/etc/dovecot/dovecot-sql.conf.ext`:'],
            ['service dovecot restart', '[-] Error while restarting dovecot:']
        ]
        for command in commands:
            _ = run_command(command[0], command[1])
        print(f'{Color.fg.green}[+] [DOVECOT] SETUP DONE{Color.reset}')

        set_installation_progress(setup_dovecot.__name__)

# setup lmtp
def setup_lmtp():
    INSTALLATION_PROGRESS = get_installation_progress()
    if setup_lmtp.__name__ not in INSTALLATION_PROGRESS:

        print(f'{Color.fg.blue}[.] SETTING UP [LMTP]{Color.reset}')
        setup_lmtp_edit_file('/etc/dovecot/conf.d/10-master.conf')
        setup_lmtp_edit_file('/etc/dovecot/conf.d/20-lmtp.conf')

        commands = [
            ['systemctl restart dovecot', '[-] Error while restarting dovecot:'],
            ['postconf virtual_transport=lmtp:unix:private/dovecot-lmtp', '[-] Error while setting up virtual_transport:']
        ]
        for command in commands:
            _ = run_command(command[0], command[1])
        print(f'{Color.fg.green}[+] [LMTP] SETUP DONE{Color.reset}')

        set_installation_progress(setup_lmtp.__name__)

# setup quotas
def setup_quotas():
    INSTALLATION_PROGRESS = get_installation_progress()
    if setup_quotas.__name__ not in INSTALLATION_PROGRESS:

        print(f'{Color.fg.blue}[.] SETTING UP [QUOTAS]{Color.reset}')
        CONFIG = get_config()
        append_to_file(
            '/etc/dovecot/conf.d/90-quota.conf',
            DOVECOT_QUOTA_CONF_FILE_CONTENT
        )
        create_new_file(
            '/usr/local/bin/quota-warning.sh',
            DOVECOT_QUOTA_WARNING_BASH_FILE_CONTENT.replace('##SERVER_FQDN##', CONFIG['SERVER_FQDN'])
        )

        commands = [
            ['chmod +x /usr/local/bin/quota-warning.sh', '[-] Error while changing permissions for `/usr/local/bin/quota-warning.sh`:'],
            ['systemctl restart dovecot', '[-] Error while restarting dovecot:'],
            ['postconf smtpd_recipient_restrictions=reject_unauth_destination,"check_policy_service unix:private/quota-status"', '[-] Error while setting up quota for postfix:']
        ]
        for command in commands:
            _ = run_command(command[0], command[1])
        print(f'{Color.fg.green}[+] [QUOTAS] SETUP DONE{Color.reset}')

        set_installation_progress(setup_quotas.__name__)

# setup roundcube
def setup_roundcube():
    INSTALLATION_PROGRESS = get_installation_progress()
    if setup_roundcube.__name__ not in INSTALLATION_PROGRESS:

        print(f'{Color.fg.blue}[.] SETTING UP [ROUNDCUBE]{Color.reset}')
        CONFIG = get_config()
        setup_roundcube_edit_files('/etc/roundcube/config.inc.php')
        append_to_file(
            '/etc/roundcube/config.inc.php',
            f'$config[\'db_dsnw\'] = \'mysql://roundcubedbuser:{CONFIG["MYSQL_roundcubedbuser_PASSWORD"]}@localhost/roundcubedb\';'
        )
        append_to_file(
            '/etc/roundcube/config.inc.php',
            '$config[\'skin_logo\'] = \'/service_logo.png\';'
        )
        create_new_file(
            '/usr/share/roundcube/plugins/password/config.inc.php',
            ROUNDCUBE_PASSWORD_PLUGIN_CONFIG_FILE_CONTENT.replace('##MYSQL_mailserverdbadmin_PASSWORD##', CONFIG['MYSQL_mailserverdbadmin_PASSWORD'])
        )
        create_new_file(
            '/usr/share/roundcube/plugins/managesieve/config.inc.php',
            '''<?php
$config['managesieve_host'] = 'localhost';
?>'''
        )

        commands = [
            [f'mysql -u roundcubedbuser -p\'{CONFIG["MYSQL_roundcubedbuser_PASSWORD"]}\' roundcubedb < /usr/share/roundcube/SQL/mysql.initial.sql', '[-] Error while setting up db for roundcube:'],
            ['chown root:www-data /etc/roundcube/plugins/password/config.inc.php', '[-] Error while changing owner for `/etc/roundcube/plugins/password/config.inc.php`:'],
            ['chmod u=rw,g=r,o= /etc/roundcube/plugins/password/config.inc.php', '[-] Error while changing permissions for `/etc/roundcube/plugins/password/config.inc.php`:'],
            ['cp ./service_logo.png /usr/share/roundcube/skins/elastic/service_logo.png', '[-] Error while copying service logo to roundcube:']
        ]
        for command in commands:
            _ = run_command(command[0], command[1])
        print(f'{Color.fg.green}[+] [ROUNDCUBE] SETUP DONE{Color.reset}')

        set_installation_progress(setup_roundcube.__name__)

# setup postfix relay
def setup_postfix_relay():
    INSTALLATION_PROGRESS = get_installation_progress()
    if setup_postfix_relay.__name__ not in INSTALLATION_PROGRESS:

        print(f'{Color.fg.blue}[.] SETTING UP [POSTFIX RELAY]{Color.reset}')
        CONFIG = get_config()
        create_new_file(
            '/etc/postfix/master.cf',
            POSTFIX_MASTER_CONF_FILE_CONTENT
        )

        commands = [
            ['postconf smtpd_sasl_type=dovecot', '[-] Error while setting up smtpd_sasl_type:'],
            ['postconf smtpd_sasl_path=private/auth', '[-] Error while setting up smtpd_sasl_path:'],
            ['postconf smtpd_sasl_auth_enable=yes', '[-] Error while setting up smtpd_sasl_auth_enable:'],
            ['postconf smtpd_tls_security_level=may', '[-] Error while setting up smtpd_tls_security_level:'],
            ['postconf smtpd_tls_auth_only=yes', '[-] Error while setting up smtpd_tls_auth_only:'],
            [f'postconf smtpd_tls_cert_file=/etc/letsencrypt/live/{CONFIG["SERVER_FQDN"]}/fullchain.pem', '[-] Error while setting up smtpd_tls_cert_file:'],
            [f'postconf smtpd_tls_key_file=/etc/letsencrypt/live/{CONFIG["SERVER_FQDN"]}/privkey.pem', '[-] Error while setting up smtpd_tls_key_file:'],
            ['postconf smtp_tls_security_level=may', '[-] Error while setting up smtp_tls_security_level:'],
            ['systemctl restart postfix', '[-] Error while restarting apache2:']
        ]
        for command in commands:
            _ = run_command(command[0], command[1])
        print(f'{Color.fg.green}[+] [POSTFIX RELAY] SETUP DONE{Color.reset}')

        set_installation_progress(setup_postfix_relay.__name__)

# setup rspamd
def setup_rspamd():
    INSTALLATION_PROGRESS = get_installation_progress()
    if setup_rspamd.__name__ not in INSTALLATION_PROGRESS:

        print(f'{Color.fg.blue}[.] SETTING UP [RSPAMD]{Color.reset}')
        RSPAMD_PASSWORD = generate_random_password(30)
        RSPAMD_PASSWORD_HASH = hash_password(RSPAMD_PASSWORD).replace('{BLF-CRYPT}', '')
        commands = [
            ['mkdir /etc/dovecot/sieve-after', '[-] Error while creating directory `/etc/dovecot/sieve-after`:'],
            ['mkdir /etc/dovecot/sieve', '[-] Error while creating directory `/etc/dovecot/sieve`:']
        ]
        for command in commands:
            _ = run_command(command[0], command[1])
        
        files = [
            ['/etc/rspamd/override.d/milter_headers.conf', 'extended_spam_headers = true;'],
            ['/etc/dovecot/sieve-after/spam-to-folder.sieve', RSPAMD_SPAM_TO_FOLDER_FILE_CONTENTS],
            ['/etc/rspamd/override.d/redis.conf', 'servers = "127.0.0.1";'],
            ['/etc/rspamd/override.d/classifier-bayes.conf', 'autolearn = [-5, 10];'],
            ['/etc/dovecot/conf.d/15-mailboxes.conf', DOVECOT_MAILBOXES_CONF_FILE_CONTENT],
            ['/etc/dovecot/sieve/learn-spam.sieve', DOVECOT_LEARN_SPAM_SIEVE_FILE_CONTENT],
            ['/etc/dovecot/sieve/learn-ham.sieve', DOVECOT_LEARN_HAM_SIEVE_FILE_CONTENT],
            ['/etc/dovecot/sieve/rspamd-learn-spam.sh', '#!/bin/sh\nexec /usr/bin/rspamc learn_spam'],
            ['/etc/dovecot/sieve/rspamd-learn-ham.sh', '#!/bin/sh\nexec /usr/bin/rspamc learn_ham'],
            ['/etc/rspamd/local.d/worker-controller.inc', RSPAMD_PASSWORD_CONF_FILE.replace('##RSPAMD_PASSWORD_HASH##', RSPAMD_PASSWORD_HASH)]
        ]
        for file in files:
            create_new_file(file[0], file[1])

        setup_rspamd_edit_files('/etc/dovecot/conf.d/90-sieve.conf')
        setup_rspamd_edit_files('/etc/dovecot/conf.d/20-imap.conf')

        commands = [
            ['systemctl restart dovecot', '[-] Error while restarting dovecot:'],
            ['postconf smtpd_milters=inet:127.0.0.1:11332', '[-] Error while setting up smtpd_milters:'],
            ['postconf non_smtpd_milters=inet:127.0.0.1:11332', '[-] Error while setting up non_smtpd_milters:'],
            ['postconf milter_mail_macros="i {mail_addr} {client_addr} {client_name} {auth_authen}"', '[-] Errro while setting up milter_mail_macros:'],
            ['sievec /etc/dovecot/sieve-after/spam-to-folder.sieve', '[-] Errow while compiling `/etc/dovecot/sieve-after/spam-to-folder.sieve`:'],
            ['sievec /etc/dovecot/sieve/learn-spam.sieve', '[-] Error while compiling `/etc/dovecot/sieve/learn-spam.sieve`:'],
            ['sievec /etc/dovecot/sieve/learn-ham.sieve', '[-] Error while compiling `/etc/dovecot/sieve/learn-ham.sieve`:'],
            ['chmod u=rw,go= /etc/dovecot/sieve/learn-{spam,ham}.{sieve,svbin}', '[-] Error while changing permissions of learn sieve files:'],
            ['chown vmail:vmail /etc/dovecot/sieve/learn-{spam,ham}.{sieve,svbin}', '[-] Error while change owner of learn sieve files:'],
            ['chmod u=rwx,go= /etc/dovecot/sieve/rspamd-learn-{spam,ham}.sh', '[-] Error while changing permissions of learn bash files:'],
            ['chown vmail:vmail /etc/dovecot/sieve/rspamd-learn-{spam,ham}.sh', '[-] Error while changing owner of learn bash files:'],
            ['systemctl restart rspamd', '[-] Error while restarting rspam:'],
            ['systemctl restart dovecot', '[-] Error while restarting dovecot:']
        ]
        for command in commands:
            _ = run_command(command[0], command[1])
        
        set_config({
            'RSPAMD_PASSWORD': RSPAMD_PASSWORD
        })
        print(f'{Color.fg.green}[+] [RSPAMD] SETUP DONE{Color.reset}')

        set_installation_progress(setup_rspamd.__name__)

def setup_dkim():
    INSTALLATION_PROGRESS = get_installation_progress()
    if setup_dkim.__name__ not in INSTALLATION_PROGRESS:

        print(f'{Color.fg.blue}[.] SETTING UP [DKIM]{Color.reset}')
        CONFIG = get_config()
        commands = [
            ['mkdir /var/lib/rspamd/dkim', '[-] Error while creating folder `/var/lib/rspamd/dkim`:'],
            ['chown _rspamd:_rspamd /var/lib/rspamd/dkim', '[-] Error while changing owner for `/var/lib/rspamd/dkim`'],
            [f'rspamadm dkim_keygen -d {CONFIG["MAIL_DN"]} -s {CONFIG["DKIM_SELECTOR"]}', '[-] Error while creating DKIM keypair:']
        ]
        for command in commands:
            _ = run_command(command[0], command[1])
        dkim_key, dkim_dns = setup_dkim_extract(_)
        
        create_new_file(
            '/etc/rspamd/local.d/dkim_signing.conf',
            'path = "/var/lib/rspamd/dkim/$domain.$selector.key";\
selector_map = "/etc/rspamd/dkim_selectors.map";'
        )
        create_new_file(
            '/etc/rspamd/dkim_selectors.map',
            f'{CONFIG["MAIL_DN"]} {CONFIG["DKIM_SELECTOR"]}'
        )
        create_new_file(
            f'/var/lib/rspamd/dkim/{CONFIG["MAIL_DN"]}.{CONFIG["DKIM_SELECTOR"]}.key',
            dkim_key
        )

        commands = [
            ['chown _rspamd /var/lib/rspamd/dkim/*', '[-] Error while change owner of `/var/lib/rspamd/dkim/*`:'],
            ['chmod u=r,go= /var/lib/rspamd/dkim/*', '[-] Error while change permission of `/var/lib/rspamd/dkim/*`'],
            ['service rspamd restart', '[-] Error while restarting `rspamd`:']
        ]
        for command in commands:
            _ = run_command(command[0], command[1])
        
        set_config({
            'DKIM_DNS': dkim_dns
        })

        print(f'{Color.fg.green}[+] [DKIM] SETUP DONE{Color.reset}')

        set_installation_progress(setup_dkim.__name__)

def print_install_complete_text():
    CONFIG = get_config()
    text = INSTALLATION_COMPLETE_TEXT.replace('###MAIL_admin_USER###', CONFIG['MAIL_admin_USER']).replace('###MAIL_admin_PASSWORD###', CONFIG['MAIL_admin_PASSWORD']).replace('###SERVER_FQDN###', CONFIG['SERVER_FQDN'])
    print(f'{Color.fg.yellow}{text}{Color.reset}')
    for config in CONFIG:
        print(f'\t{Color.fg.cyan}{config}:{Color.reset} {Color.fg.green}{CONFIG[config]}{Color.reset}')
    
    print(f'{Color.fg.yellow}\nThis all config is also stored in `.CONFIG` file created in this directory. Save it locally in a secure manner.{Color.reset}')