WELCOME_TEXT = r"""
      __  __       _ _ 
  ___|  \/  | __ _(_) |
 / __| |\/| |/ _` | | |
 \__ \ |  | | (_| | | |
 |___/_|  |_|\__,_|_|_| 
                                                                                  
        - by: w0rk5107h
"""

SERVER_FQDN_INPUT_MESSAGE = """Server Fully Qualified Domain Name (FQDN)
Please enter the FQDN you wish to assign to your mail server. This is how your server will be known on the internet.
For example, if your domain is example.com, your FQDN could be one of the following:
    1. mail.example.com
    2. webmail.example.com
    3. smtp.example.com
    4. imap.example.com
    etc.
In general, it's recommended to use 'mail.' or 'webmail.' as the prefix.

NOTES:
    1. Whichever option you choose should also be set as the hostname of this server.
    2. Before proceeding, ensure you have set up a DNS 'A' record as follows:
        <YOUR_CHOSEN_OPTION> -> <SERVER_IP>
    3. You must also set the reverse DNS (rDNS) for this server to match your chosen option.
Completing these steps is crucial to avoid potential issues during the installation process.

ENTER YOUR SERVER_FQDN: """

MAIL_DN_INPUT_MESSAGE = """Mail Domain Name
Please enter the domain name you wish to use for your email addresses. 
For example, if you want your email addresses to end with '@example.com', 
your MAIL_DN should be:
    example.com
Generally, this is the base domain name without any prefixes.

ENTER YOUR MAIL_DN: """

DKIM_SELECTOR_INPUT_MESSAGE = """DKIM Key Selector
Please enter the DKIM key selector you wish to use for your mail server. This selector will be used in the DNS TXT record for DKIM.
For example, you can use:
    1. default
    2. mail
    3. selector1
    4. domainkey
    etc.
Choose a descriptive selector that represents your domain or organization.

NOTES:
    1. The DKIM key selector should be unique and easy to remember.
    2. It's recommended to use alphanumeric characters and underscores (_) only.
    3. Avoid using special characters or spaces in the selector.

ENTER YOUR DKIM KEY SELECTOR: """

SERVICE_NAME_INPUT_MESSAGE = """Service Name
Please enter what you would like to call this mail service:
For example,
	1. sMail
	2. PersonalMail
	3. MyMail
This won't change the functional behaviour of the service.

ENTER YOUR SERVICE NAME: """

SERVICE_LOGO_INPUT_MESSAGE = """Service Logo
Please copy an image file in this folder that you want to use as the logo of your service.
The image file must be named `service_logo.png`.
After doing this press enter to continue.
If you dont wish to have a custom logo just press enter without copying the image.

PRESS ENTER..."""

APACHE_HTTP_VHOST_FILE_CONTENT = r"""<VirtualHost *:80>
  ServerName ##SERVER_FQDN##
  DocumentRoot /var/www/##SERVER_FQDN##

  RewriteEngine On
  RewriteCond %{REQUEST_URI} !\.well-known/acme-challenge
  RewriteRule ^(.*)$ https://%{SERVER_NAME}$1 [R=301,L]
</VirtualHost>
"""

APACHE_HTTPS_VHOST_FILE_CONTENT = r"""<VirtualHost *:443>
  ServerName ##SERVER_FQDN##
  DocumentRoot /var/lib/roundcube/public_html
  # Roundcube
  Include /etc/roundcube/apache.conf

  # Mail client auto-configuration
  Alias /.well-known/autoconfig/mail /var/www/html/autoconfig-mail

  <Location /rspamd>
    Options Indexes FollowSymLinks
    AllowOverride None
  </Location>
  RewriteEngine on
  RewriteRule ^/rspamd$ /rspamd/ [R,L]
  RewriteRule ^/rspamd/(.*) http://localhost:11334/$1 [P,L]

  SSLEngine on
  SSLCertificateFile /etc/letsencrypt/live/##SERVER_FQDN##/fullchain.pem
  SSLCertificateKeyFile /etc/letsencrypt/live/##SERVER_FQDN##/privkey.pem
Include /etc/letsencrypt/options-ssl-apache.conf
</VirtualHost>"""

AUTOCONFIG_FILE_CONTENTS = """<?xml version="1.0" encoding="UTF-8"?>

<clientConfig version="1.1">
  <emailProvider id="###SERVER_FQDN###">
    <domain>###MAIL_DN###</domain>
    <displayName>###SERVICE_NAME###</displayName>
    <displayShortName>###SERVICE_NAME###</displayShortName>
    <incomingServer type="imap">
      <hostname>###SERVER_FQDN###</hostname>
      <port>143</port>
      <socketType>STARTTLS</socketType>
      <authentication>password-cleartext</authentication>
      <username>%EMAILADDRESS%</username>
    </incomingServer>
    <incomingServer type="pop3">
      <hostname>###SERVER_FQDN###</hostname>
      <port>110</port>
      <socketType>STARTTLS</socketType>
      <authentication>password-cleartext</authentication>
      <username>%EMAILADDRESS%</username>
    </incomingServer>
    <outgoingServer type="smtp">
      <hostname>###SERVER_FQDN###</hostname>
      <port>587</port>
      <socketType>STARTTLS</socketType>
      <authentication>password-cleartext</authentication>
      <username>%EMAILADDRESS%</username>
    </outgoingServer>
  </emailProvider>
</clientConfig>"""

CREATE_MAIL_DB_ADMIN_QUERY = r"""grant all on mailserverdb.* to 'mailserverdbadmin'@'localhost' identified by '##MYSQL_mailserverdbadmin_PASSWORD##';"""

CREATE_MAIL_DB_USER_QUERY = r"""grant select on mailserverdb.* to 'mailserverdbuser'@'127.0.0.1' identified by '##MYSQL_mailserverdbuser_PASSWORD##';"""

CREATE_ROUNDCUBE_DB_USER_QUERY = r"""grant all on roundcubedb.* to 'roundcubedbuser'@'localhost' identified by '##MYSQL_roundcubedbuser_PASSWORD##';"""

CREATE_virtual_domains_TABLE_QUERY = r"""CREATE TABLE IF NOT EXISTS `virtual_domains` (
 `id` int(11) NOT NULL auto_increment,
 `name` varchar(50) NOT NULL,
 PRIMARY KEY (`id`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""

CREATE_virtual_users_TABLE_QUERY = r"""CREATE TABLE IF NOT EXISTS `virtual_users` (
 `id` int(11) NOT NULL auto_increment,
 `domain_id` int(11) NOT NULL,
 `email` varchar(100) NOT NULL,
 `password` varchar(150) NOT NULL,
 `quota` bigint(11) NOT NULL DEFAULT 0,
 PRIMARY KEY (`id`),
 UNIQUE KEY `email` (`email`),
 FOREIGN KEY (domain_id) REFERENCES virtual_domains(id) ON DELETE CASCADE
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""

CREATE_virtual_aliases_TABLE_QUERY = r"""CREATE TABLE IF NOT EXISTS `virtual_aliases` (
 `id` int(11) NOT NULL auto_increment,
 `domain_id` int(11) NOT NULL,
 `source` varchar(100) NOT NULL,
 `destination` varchar(100) NOT NULL,
 PRIMARY KEY (`id`),
 FOREIGN KEY (domain_id) REFERENCES virtual_domains(id) ON DELETE CASCADE
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""

CREATE_INIT_DOMAIN_ENTRY_QUERY = r"""REPLACE INTO virtual_domains (id,name) VALUES ('1','##MAIL_DN##');"""

CREATE_INIT_USER_ENTRY_QUERY = r"""REPLACE INTO virtual_users (id,domain_id,password,email)
 VALUES ('1', '1', '##MAIL_admin_PASSWORD_HASHED##', 'admin@##MAIL_DN##');"""

CREATE_INIT_ALIAS_ENTRY_QUERY = r"""REPLACE INTO virtual_aliases (id,domain_id,source,destination)
 VALUES ('1', '1', 'administrator@##MAIL_DN##', 'admin@##MAIL_DN##');"""

POSTFIX_VIRTUAL_DOMAINS_FILE_CONTENT = r"""user = mailserverdbuser
password = ##MYSQL_mailserverdbuser_PASSWORD##
hosts = 127.0.0.1
dbname = mailserverdb
query = SELECT name FROM virtual_domains WHERE name='%s'"""

POSTFIX_VIRTUAL_USERS_FILE_CONTENT = r"""user = mailserverdbuser
password = ##MYSQL_mailserverdbuser_PASSWORD##
hosts = 127.0.0.1
dbname = mailserverdb
query = SELECT email FROM virtual_users WHERE email='%s'"""

POSTFIX_VIRTUAL_ALIASES_FILE_CONTENT = r"""user = mailserverdbuser
password = ##MYSQL_mailserverdbuser_PASSWORD##
hosts = 127.0.0.1
dbname = mailserverdb
query = SELECT destination FROM virtual_aliases WHERE source='%s'"""

POSTFIX_EMAIL_TO_EMAIL_FILE_CONTENT = r"""user = mailserverdbuser
password = ##MYSQL_mailserverdbuser_PASSWORD##
hosts = 127.0.0.1
dbname = mailserverdb
query = SELECT email FROM virtual_users WHERE email='%s'"""

DOVECOT_SQL_CONF_FILE_CONTENT = r"""driver = mysql

connect = \
  host=127.0.0.1 \
  dbname=mailserverdb \
  user=mailserverdbuser \
  password=##MYSQL_mailserverdbuser_PASSWORD##

user_query = SELECT email as user, \
  concat('*:bytes=', quota) AS quota_rule, \
  '/var/vmail/%d/%n' AS home, \
  5000 AS uid, 5000 AS gid \
  FROM virtual_users WHERE email='%u'

password_query = SELECT password FROM virtual_users WHERE email='%u'

iterate_query = SELECT email AS user FROM virtual_users"""

DOVECOT_QUOTA_CONF_FILE_CONTENT = """plugin {
  quota = count:User quota
  quota_vsizes = yes

  quota_status_success = DUNNO
  quota_status_nouser = DUNNO
  quota_status_overquota = "452 4.2.2 Mailbox is full and cannot receive any more emails"
}

service quota-status {
  executable = /usr/lib/dovecot/quota-status -p postfix
  unix_listener /var/spool/postfix/private/quota-status {
    user = postfix
  }
}

plugin {
   quota_warning = storage=95%% quota-warning 95 %u
   quota_warning2 = storage=80%% quota-warning 80 %u
}

service quota-warning {
   executable = script /usr/local/bin/quota-warning.sh
   unix_listener quota-warning {
     user = vmail
     group = vmail
     mode = 0660
   }
}"""

DOVECOT_QUOTA_WARNING_BASH_FILE_CONTENT = r"""#!/bin/sh
PERCENT=$1
USER=$2
cat << EOF | /usr/lib/dovecot/dovecot-lda -d $USER -o "plugin/quota=maildir:User quota:noenforcing"
From: postmaster@##SERVER_FQDN##
Subject: Quota warning - $PERCENT% reached

Your mailbox can only store a limited amount of emails.
Currently it is $PERCENT% full. If you reach 100% then
new emails cannot be stored. Thanks for your understanding.
EOF"""

ROUNDCUBE_PASSWORD_PLUGIN_CONFIG_FILE_CONTENT = r"""<?php
// Plugin configuration for password
// See /usr/share/roundcube/plugins/password/config.inc.php.dist for instructions
// Check the access right of the file if you put sensitive information in it.
$config['password_driver'] = 'sql';
$config['password_minimum_length'] = 12;
$config['password_force_save'] = true;
$config['password_algorithm'] = 'blowfish-crypt';
$config['password_algorithm_prefix'] = '{CRYPT}';
$config['password_db_dsn'] = 'mysql://mailserverdbadmin:##MYSQL_mailserverdbadmin_PASSWORD##@localhost/mailserverdb';
$config['password_query'] = "UPDATE virtual_users SET password=%P WHERE email=%u";
?>"""

POSTFIX_MASTER_CONF_FILE_CONTENT = r"""#
# Postfix master process configuration file.  For details on the format
# of the file, see the master(5) manual page (command: "man 5 master" or
# on-line: http://www.postfix.org/master.5.html).
#
# Do not forget to execute "postfix reload" after editing this file.
#
# ==========================================================================
# service type  private unpriv  chroot  wakeup  maxproc command + args
#               (yes)   (yes)   (no)    (never) (100)
# ==========================================================================
smtp      inet  n       -       y       -       -       smtpd
#smtp      inet  n       -       y       -       1       postscreen
#smtpd     pass  -       -       y       -       -       smtpd
#dnsblog   unix  -       -       y       -       0       dnsblog
#tlsproxy  unix  -       -       y       -       0       tlsproxy
submission inet n       -       y       -       -       smtpd
  -o syslog_name=postfix/submission
  -o smtpd_tls_security_level=encrypt
  -o smtpd_sasl_auth_enable=yes
  -o smtpd_tls_auth_only=yes
  -o smtpd_reject_unlisted_recipient=no
  -o smtpd_recipient_restrictions=
  -o smtpd_relay_restrictions=permit_sasl_authenticated,reject
  -o milter_macro_daemon_name=ORIGINATING
  -o smtpd_sender_restrictions=reject_sender_login_mismatch,permit_sasl_authenticated,reject
#smtps     inet  n       -       y       -       -       smtpd
#  -o syslog_name=postfix/smtps
#  -o smtpd_tls_wrappermode=yes
#  -o smtpd_sasl_auth_enable=yes
#  -o smtpd_reject_unlisted_recipient=no
#  -o smtpd_client_restrictions=$mua_client_restrictions
#  -o smtpd_helo_restrictions=$mua_helo_restrictions
#  -o smtpd_sender_restrictions=$mua_sender_restrictions
#  -o smtpd_recipient_restrictions=
#  -o smtpd_relay_restrictions=permit_sasl_authenticated,reject
#  -o milter_macro_daemon_name=ORIGINATING
#628       inet  n       -       y       -       -       qmqpd
pickup    unix  n       -       y       60      1       pickup
cleanup   unix  n       -       y       -       0       cleanup
qmgr      unix  n       -       n       300     1       qmgr
#qmgr     unix  n       -       n       300     1       oqmgr
tlsmgr    unix  -       -       y       1000?   1       tlsmgr
rewrite   unix  -       -       y       -       -       trivial-rewrite
bounce    unix  -       -       y       -       0       bounce
defer     unix  -       -       y       -       0       bounce
trace     unix  -       -       y       -       0       bounce
verify    unix  -       -       y       -       1       verify
flush     unix  n       -       y       1000?   0       flush
proxymap  unix  -       -       n       -       -       proxymap
proxywrite unix -       -       n       -       1       proxymap
smtp      unix  -       -       y       -       -       smtp
relay     unix  -       -       y       -       -       smtp
        -o syslog_name=postfix/$service_name
#       -o smtp_helo_timeout=5 -o smtp_connect_timeout=5
showq     unix  n       -       y       -       -       showq
error     unix  -       -       y       -       -       error
retry     unix  -       -       y       -       -       error
discard   unix  -       -       y       -       -       discard
local     unix  -       n       n       -       -       local
virtual   unix  -       n       n       -       -       virtual
lmtp      unix  -       -       y       -       -       lmtp
anvil     unix  -       -       y       -       1       anvil
scache    unix  -       -       y       -       1       scache
postlog   unix-dgram n  -       n       -       1       postlogd
#
# ====================================================================
# Interfaces to non-Postfix software. Be sure to examine the manual
# pages of the non-Postfix software to find out what options it wants.
#
# Many of the following services use the Postfix pipe(8) delivery
# agent.  See the pipe(8) man page for information about ${recipient}
# and other message envelope options.
# ====================================================================
#
# maildrop. See the Postfix MAILDROP_README file for details.
# Also specify in main.cf: maildrop_destination_recipient_limit=1
#
#maildrop  unix  -       n       n       -       -       pipe
#  flags=DRhu user=vmail argv=/usr/bin/maildrop -d ${recipient}
#
# ====================================================================
#
# Recent Cyrus versions can use the existing "lmtp" master.cf entry.
#
# Specify in cyrus.conf:
#   lmtp    cmd="lmtpd -a" listen="localhost:lmtp" proto=tcp4
#
# Specify in main.cf one or more of the following:
#  mailbox_transport = lmtp:inet:localhost
#  virtual_transport = lmtp:inet:localhost
#
# ====================================================================
#
# Cyrus 2.1.5 (Amos Gouaux)
# Also specify in main.cf: cyrus_destination_recipient_limit=1
#
#cyrus     unix  -       n       n       -       -       pipe
#  user=cyrus argv=/cyrus/bin/deliver -e -r ${sender} -m ${extension} ${user}
#
# ====================================================================
# Old example of delivery via Cyrus.
#
#old-cyrus unix  -       n       n       -       -       pipe
#  flags=R user=cyrus argv=/cyrus/bin/deliver -e -m ${extension} ${user}
#
# ====================================================================
#
# See the Postfix UUCP_README file for configuration details.
#
#uucp      unix  -       n       n       -       -       pipe
#  flags=Fqhu user=uucp argv=uux -r -n -z -a$sender - $nexthop!rmail ($recipient)
#
# Other external delivery methods.
#
#ifmail    unix  -       n       n       -       -       pipe
#  flags=F user=ftn argv=/usr/lib/ifmail/ifmail -r $nexthop ($recipient)
#bsmtp     unix  -       n       n       -       -       pipe
#  flags=Fq. user=bsmtp argv=/usr/lib/bsmtp/bsmtp -t$nexthop -f$sender $recipient
#scalemail-backend unix -       n       n       -       2       pipe
#  flags=R user=scalemail argv=/usr/lib/scalemail/bin/scalemail-store ${nexthop} ${user} ${extension}
#mailman   unix  -       n       n       -       -       pipe
#  flags=FR user=list argv=/usr/lib/mailman/bin/postfix-to-mailman.py
#  ${nexthop} ${user}"""

RSPAMD_SPAM_TO_FOLDER_FILE_CONTENTS = """require ["fileinto"];

if header :contains "X-Spam" "Yes" {
 fileinto "Junk";
 stop;
}"""

DOVECOT_MAILBOXES_CONF_FILE_CONTENT = """##
## Mailbox definitions
##

# Each mailbox is specified in a separate mailbox section. The section name
# specifies the mailbox name. If it has spaces, you can put the name
# "in quotes". These sections can contain the following mailbox settings:
#
# auto:
#   Indicates whether the mailbox with this name is automatically created
#   implicitly when it is first accessed. The user can also be automatically
#   subscribed to the mailbox after creation. The following values are
#   defined for this setting:
#
#     no        - Never created automatically.
#     create    - Automatically created, but no automatic subscription.
#     subscribe - Automatically created and subscribed.
#
# special_use:
#   A space-separated list of SPECIAL-USE flags (RFC 6154) to use for the
#   mailbox. There are no validity checks, so you could specify anything
#   you want in here, but it's not a good idea to use flags other than the
#   standard ones specified in the RFC:
#
#     \All       - This (virtual) mailbox presents all messages in the
#                  user's message store.
#     \Archive   - This mailbox is used to archive messages.
#     \Drafts    - This mailbox is used to hold draft messages.
#     \Flagged   - This (virtual) mailbox presents all messages in the
#                  user's message store marked with the IMAP \Flagged flag.
#     \Important - This (virtual) mailbox presents all messages in the
#                  user's message store deemed important to user.
#     \Junk      - This mailbox is where messages deemed to be junk mail
#                  are held.
#     \Sent      - This mailbox is used to hold copies of messages that
#                  have been sent.
#     \Trash     - This mailbox is used to hold messages that have been
#                  deleted.
#
# comment:
#   Defines a default comment or note associated with the mailbox. This
#   value is accessible through the IMAP METADATA mailbox entries
#   "/shared/comment" and "/private/comment". Users with sufficient
#   privileges can override the default value for entries with a custom
#   value.

# NOTE: Assumes "namespace inbox" has been defined in 10-mail.conf.
namespace inbox {
  # These mailboxes are widely used and could perhaps be created automatically:
  mailbox Drafts {
    special_use = \Drafts
    auto = subscribe
  }
  mailbox Junk {
    special_use = \Junk
    auto = subscribe
    autoexpunge = 30d
  }
  mailbox Trash {
    special_use = \Trash
    auto = subscribe
    autoexpunge = 30d
  }
  mailbox Sent {
    special_use = \Sent
    auto = subscribe
  }
  mailbox Archive {
    special_use = \Archive
    auto = subscribe
  }

  # For \Sent mailboxes there are two widely used names. We'll mark both of
  # them as \Sent. User typically deletes one of them if duplicates are created.
  
  mailbox "Sent Messages" {
    special_use = \Sent
  }

  # If you have a virtual "All messages" mailbox:
  #mailbox virtual/All {
  #  special_use = \All
  #  comment = All my messages
  #}

  # If you have a virtual "Flagged" mailbox:
  #mailbox virtual/Flagged {
  #  special_use = \Flagged
  #  comment = All my flagged messages
  #}

  # If you have a virtual "Important" mailbox:
  #mailbox virtual/Important {
  #  special_use = \Important
  #  comment = All my important messages
  #}
}"""

DOVECOT_AUTO_LEARN_CONF_FILE_CONTENT = """  # From elsewhere to Junk folder
  imapsieve_mailbox1_name = Junk
  imapsieve_mailbox1_causes = COPY
  imapsieve_mailbox1_before = file:/etc/dovecot/sieve/learn-spam.sieve

  # From Junk folder to elsewhere
  imapsieve_mailbox2_name = *
  imapsieve_mailbox2_from = Junk
  imapsieve_mailbox2_causes = COPY
  imapsieve_mailbox2_before = file:/etc/dovecot/sieve/learn-ham.sieve

  sieve_pipe_bin_dir = /etc/dovecot/sieve
  sieve_global_extensions = +vnd.dovecot.pipe
  sieve_plugins = sieve_imapsieve sieve_extprograms"""

DOVECOT_LEARN_SPAM_SIEVE_FILE_CONTENT = """require ["vnd.dovecot.pipe", "copy", "imapsieve"];
pipe :copy "rspamd-learn-spam.sh";"""

DOVECOT_LEARN_HAM_SIEVE_FILE_CONTENT = """require ["vnd.dovecot.pipe", "copy", "imapsieve", "variables"];
if string "${mailbox}" "Trash" {
  stop;
}
pipe :copy "rspamd-learn-ham.sh";"""

RSPAMD_PASSWORD_CONF_FILE = """hash = "blf-crypt";
    password = "##RSPAMD_PASSWORD_HASH##";
"""

INSTALLATION_COMPLETE_TEXT = """Congratulations!!!
You have successfully setup your personal mail service.
Sadly, the work doesn't end here, you'll still need to do a couple of things:
	1. DNS RECORDS: There are some DNS records that need to be set in order for this mail service to work. (Check out the doc for more on this.)
	2. PORT FORWARDING: You'll need to allow some inbound ports for this server. (Again, check the doc for more on this.)
These 2 steps are crutial for the mail serverice to work.

There is one mail account already created for you:
	username: ###MAIL_admin_USER###
	password: ###MAIL_admin_PASSWORD###
You can use these creds to log into `https://###SERVER_FQDN###`
To create/manage/delete users check out the doc.

Below is all the config for this mailserver:"""