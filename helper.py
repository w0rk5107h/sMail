import json
import sys
import sys
import subprocess
import random
import string
import bcrypt
import datetime
import inspect
import os
import re
from color import *
from text import *


# log init
def log_init():
    if os.path.exists('./install.log'):
        with open('install.log', 'a') as file:
            file.write('\n\n\n==========STARTING EXECUTION==========\n\n')
    else:
        with open('install.log', 'w') as file:
            file.write('==========STARTING EXECUTION==========\n\n')

# log
def log(log_type, log_place, log_message):
    log_line = f'[{datetime.datetime.now()}]{"-" * 10}'
    log_line += f'[{log_type}]{"-" * (15 - len(log_type))}'
    log_line += f'[{log_place}]{"-" * (30 - len(log_place))}'
    if '\n' in log_message:
        length = len(log_line)
        log_message = log_message.split('\n')
        log_message = [x for x in log_message if x]
        log_line += log_message[0]
        for line in log_message[1:]:
            log_line += f'\n{" " * length}{line}'
    else:
        log_line += log_message

    with open('install.log', 'a') as file:
        file.write(f'\n{log_line}')

# get installation progress
def get_installation_progress():
    INSTALLATION_PROGRESS = list()
    try:
        with open('.INSTALLATION_PROGRESS') as file:
            INSTALLATION_PROGRESS = json.loads(file.read())
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f'{Color.fg.red}[-] Error while reading ".INSTALLATION_PROGRESS" file:{Color.reset}')
        print(f'{Color.bg.red}{str(e)}{Color.reset}')
        sys.exit()

    return INSTALLATION_PROGRESS

# set installation progress
def set_installation_progress(task):
    INSTALLATION_PROGRESS = list()
    try:
        with open('.INSTALLATION_PROGRESS') as file:
            INSTALLATION_PROGRESS = json.loads(file.read())
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f'{Color.fg.red}[-] Error while reading ".INSTALLATION_PROGRESS" file:{Color.reset}')
        print(f'{Color.bg.red}{str(e)}{Color.reset}')
        sys.exit()

    INSTALLATION_PROGRESS.append(task)
    try:
        with open('.INSTALLATION_PROGRESS', 'w') as file:
            file.write(json.dumps(INSTALLATION_PROGRESS, indent=4))
    except Exception as e:
        print(f'{Color.fg.red}[-] Error while writing in ".INSTALLATION_PROGRESS" file:{Color.reset}')
        print(f'{Color.bg.red}{str(e)}{Color.reset}')
        sys.exit()

# get config
def get_config():
    CONFIG = dict()
    try:
        with open('.CONFIG') as file:
            CONFIG = json.loads(file.read())
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f'{Color.fg.red}[-] Error while reading ".CONFIG" file:{Color.reset}')
        print(f'{Color.bg.red}{str(e)}{Color.reset}')
        sys.exit()

    return CONFIG

# set config
def set_config(config):
    CONFIG = dict()
    try:
        with open('.CONFIG') as file:
            CONFIG = json.loads(file.read())
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f'{Color.fg.red}[-] Error while reading ".CONFIG" file:{Color.reset}')
        print(f'{Color.bg.red}{str(e)}{Color.reset}')
        sys.exit()

    CONFIG.update(config)
    try:
        with open('.CONFIG', 'w') as file:
            file.write(json.dumps(CONFIG, indent=4))
    except Exception as e:
        print(f'{Color.fg.red}[-] Error while writing in ".CONFIG" file:{Color.reset}')
        print(f'{Color.bg.red}{str(e)}{Color.reset}')
        sys.exit()

# run command
def run_command(command, error_message):
    caller_function = inspect.stack()[1].function
    shell = ''
    try:
        shell = subprocess.Popen(['/bin/bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except Exception as e:
        log('ERROR', caller_function, 'Error in opening bash shell')
        print(f'{Color.fg.red}[-] Some error occured while opening a /bin/bash shell:{Color.reset}')
        print(f'{Color.bg.red}{str(e)}{Color.reset}')
        sys.exit()
    try:
        log('INFO', caller_function, f'Running command `{command}`')
        shell.stdin.write(command + '\n')
        shell.stdin.flush()
        out, err = shell.communicate()
        shell.terminate()
        err = err.split('\n')
        err = [x for x in err if not 'WARNING' in x]
        err = [x for x in err if x != 'Saving debug log to /var/log/letsencrypt/letsencrypt.log'] # FOR FCKN LETS-ENCRYPT
        err = [x for x in err if x]
        if len(err):
            err = '\n'.join(err)
            log('ERROR', caller_function, f'{error_message}\n{err}')
            print(f'{Color.fg.red}{error_message}{Color.reset}')
            print(f'{Color.bg.red}{err}{Color.reset}')
            sys.exit()
    except Exception as e:
        shell.terminate()
        log('ERROR', caller_function, f'Some error occured while running the command: `{command}`\n{str(e)}')
        print(f'{Color.fg.red}[-] Some error occured while running the command: {Color.reset}{Color.bg.red}{command}{Color.reset}')
        print(f'{Color.bg.red}{str(e)}{Color.reset}')
        sys.exit()

    log('SUCCESS', caller_function, f'`{command}` ran successfully:\n{out}')
    return out

# create new file
def create_new_file(file_path, file_content):
    caller_function = inspect.stack()[1].function
    try:
        log('INFO', caller_function, f'Creating file " `{file_path}`')
        with open(file_path, 'w') as file:
            file.write(file_content)
    except Exception as e:
        log('ERROR', caller_function, f'Error while creating file: `{file_path}`\n{str(e)}')
        print(f'{Color.fg.red}[-] Error while writing in `{file_path}`:{Color.reset}')
        print(f'{Color.bg.red}{str(e)}{Color.reset}')
        sys.exit()
    
    log('SUCCESS', caller_function, f'Successfully created file `{file_path}`:\n{file_content}')

# append to file
def append_to_file(file_path, file_content):
    caller_function = inspect.stack()[1].function
    try:
        log('INFO', caller_function, f'Appending in file " `{file_path}`')
        with open(file_path, 'a') as file:
            file.write('\n' + file_content)
    except Exception as e:
        log('ERROR', caller_function, f'Error while appending in file: `{file_path}`\n{str(e)}')
        print(f'{Color.fg.red}[-] Error while writing in `{file_path}`:{Color.reset}')
        print(f'{Color.bg.red}{str(e)}{Color.reset}')
        sys.exit()

    log('SUCCESS', caller_function, f'Successfully appended in file `{file_path}`:\n{file_content}')

# generate random password
def generate_random_password(length):
    password_characters = []
    password_characters.extend(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length))
    random.shuffle(password_characters)
    password = ''.join(password_characters)

    return password

# hash password
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return f'{{BLF-CRYPT}}{hashed_password.decode()}'

# run sql query
def run_sql_query(lines, error_message):
    caller_function = inspect.stack()[1].function
    shell = ''
    try:
        shell = subprocess.Popen(['/bin/bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except Exception as e:
        log('ERROR', caller_function, 'Error in opening bash shell')
        print(f'{Color.fg.red}[-] Some error occured while opening a /bin/bash shell:{Color.reset}')
        print(f'{Color.bg.red}{str(e)}{Color.reset}')
        sys.exit()
    try:
        n = '\n'
        log('INFO', caller_function, f'Running sql query: {n.join(lines)}')
        for line in lines:
            shell.stdin.write(line + '\n')
        shell.stdin.flush()
        out, err = shell.communicate()
        shell.terminate()
        err = err.split('\n')
        err = [x for x in err if x]
        if len(err):
            err = '\n'.join(err)
            log('ERROR', caller_function, f'{error_message}\n{err}')
            print(f'{Color.fg.red}{error_message}{Color.reset}')
            print(f'{Color.bg.red}{err}{Color.reset}')
            sys.exit()
    except Exception as e:
        shell.terminate()
        n = '\n'
        log('ERROR', caller_function, f'Some error occured while running the sql query: `{n.join(lines)}`\n{str(e)}')
        print(f'{Color.fg.red}[-] Some error occured while running the command: {Color.reset}{Color.bg.red}{n.join(lines)}{Color.reset}')
        print(f'{Color.bg.red}{str(e)}{Color.reset}')
        sys.exit()

    n = '\n'
    log('SUCCESS', caller_function, f'{n.join(lines)} ran successfully:\n{out}')
    return out

# edit dovecot setup files
def setup_dovecot_edit_files(file_name):
    caller_function = inspect.stack()[1].function
    try:
        log('INFO', caller_function, f'Editing file: `{file_name}`')
        if file_name == '/etc/dovecot/conf.d/10-auth.conf':
            file_content = str()
            with open('/etc/dovecot/conf.d/10-auth.conf', 'r') as file:
                file_content = file.read().split('\n')
            for i in range(len(file_content)):
                if file_content[i].startswith('auth_mechanisms ='):
                    file_content[i] = 'auth_mechanisms = plain login'
                if file_content[i].startswith('!include auth-system.conf.ext'):
                    file_content[i] = '#!include auth-system.conf.ext'
                if file_content[i].startswith('#!include auth-sql.conf.ext'):
                    file_content[i] = '!include auth-sql.conf.ext'
            with open('/etc/dovecot/conf.d/10-auth.conf', 'w') as file:
                file.write('\n'.join(file_content))
        
        elif file_name == '/etc/dovecot/conf.d/10-mail.conf':
            file_content = str()
            with open('/etc/dovecot/conf.d/10-mail.conf', 'r') as file:
                file_content = file.read().split('\n')
            for i in range(len(file_content)):
                if file_content[i].startswith('mail_location = '):
                    file_content[i] = 'mail_location = maildir:~/Maildir'
                if file_content[i].startswith('#mail_plugins ='):
                    file_content[i] = 'mail_plugins = quota'
            with open('/etc/dovecot/conf.d/10-mail.conf', 'w') as file:
                file.write('\n'.join(file_content))

        elif file_name == '/etc/dovecot/conf.d/10-master.conf':
            file_content = str()
            with open('/etc/dovecot/conf.d/10-master.conf', 'r') as file:
                file_content = file.read().split('\n')
            index = int()
            for i in range(len(file_content)):
                if file_content[i].startswith('  # Postfix smtp-auth'):
                    index = i + 1
                    break
            content_to_add = ['  unix_listener /var/spool/postfix/private/auth {', '    mode = 0660', '    user = postfix', '    group = postfix', '  }']
            for line in content_to_add[::-1]:
                file_content.insert(index, line)
            with open('/etc/dovecot/conf.d/10-master.conf', 'w') as file:
                file.write('\n'.join(file_content))

        elif file_name == '/etc/dovecot/conf.d/10-ssl.conf':
            file_content = str()
            CONFIG = get_config()
            with open('/etc/dovecot/conf.d/10-ssl.conf', 'r') as file:
                file_content = file.read().split('\n')
            for i in range(len(file_content)):
                if file_content[i].startswith('ssl = '):
                    file_content[i] = 'ssl = required'
                if file_content[i].startswith('ssl_cert = '):
                    file_content[i] = f'ssl_cert = </etc/letsencrypt/live/{CONFIG["SERVER_FQDN"]}/fullchain.pem'
                if file_content[i].startswith('ssl_key = '):
                    file_content[i] = f'ssl_key = </etc/letsencrypt/live/{CONFIG["SERVER_FQDN"]}/privkey.pem'
            with open('/etc/dovecot/conf.d/10-ssl.conf', 'w') as file:
                file.write('\n'.join(file_content))

    except Exception as e:
        log('ERROR', caller_function, f'Error while editing file `{file_name}`\n{set(e)}')
        print(f'{Color.fg.red}[-] Error while editting the file `{file_name}`:{Color.reset}')
        print(f'{Color.bg.red}{str(e)}{Color.reset}')
        sys.exit()
    
    log('SUCCESS', caller_function, f'Successfully edited the file `{file_name}`')

# edit lmtp setup file
def setup_lmtp_edit_file(file_name):
    caller_function = inspect.stack()[1].function
    try:
        log('INFO', caller_function, f'Editing file: `{file_name}`')
        if file_name == '/etc/dovecot/conf.d/10-master.conf':
            file_content = str()
            with open('/etc/dovecot/conf.d/10-master.conf', 'r') as file:
                file_content = file.read().split('\n')
            index = int()
            for i in range(len(file_content)):
                if file_content[i].startswith('  unix_listener lmtp {'):
                    file_content[i] = '  unix_listener /var/spool/postfix/private/dovecot-lmtp {'
                    index = i + 1
                    break
            content_to_add = ['    group = postfix', '    mode = 0600', '    user = postfix']
            for line in content_to_add[::-1]:
                file_content.insert(index, line)
            with open('/etc/dovecot/conf.d/10-master.conf', 'w') as file:
                file.write('\n'.join(file_content))
        
        elif file_name == '/etc/dovecot/conf.d/20-lmtp.conf':
            file_content = str()
            with open('/etc/dovecot/conf.d/20-lmtp.conf', 'r') as file:
                file_content = file.read().split('\n')
            for i in range(len(file_content)):
                if file_content[i].startswith('  #mail_plugins ='):
                    file_content[i] = '  mail_plugins = $mail_plugins sieve'
                    break
            with open('/etc/dovecot/conf.d/20-lmtp.conf', 'w') as file:
                file.write('\n'.join(file_content))

    except Exception as e:
        log('ERROR', caller_function, f'Error while editing file `{file_name}`\n{set(e)}')
        print(f'{Color.fg.red}[-] Error while editting the file `{file_name}`:{Color.reset}')
        print(f'{Color.bg.red}{str(e)}{Color.reset}')
        sys.exit()

    log('SUCCESS', caller_function, f'Successfully edited the file `{file_name}`')

# edit roundcube setup files
def setup_roundcube_edit_files(file_name):
    caller_function = inspect.stack()[1].function
    try:
        log('INFO', caller_function, f'Editing file: `{file_name}`')
        if file_name == '/etc/roundcube/config.inc.php':
            file_content = str()
            CONFIG = get_config()
            with open('/etc/roundcube/config.inc.php', 'r') as file:
                file_content = file.read().split('\n')
            index = int()
            for i in range(len(file_content)):
                if file_content[i].startswith('$config[\'imap_host\'] ='):
                    file_content[i] = f'$config[\'imap_host\'] = "tls://{CONFIG["SERVER_FQDN"]}:143";'
                if file_content[i].startswith('$config[\'smtp_host\'] ='):
                    file_content[i] = f'$config[\'smtp_host\'] = "tls://{CONFIG["SERVER_FQDN"]}:587";'
                if file_content[i].startswith('$config[\'product_name\'] ='):
                    file_content[i] = f'$config[\'product_name\'] = \'{CONFIG["SERVICE_NAME"]}\';'
                if file_content[i].startswith('$config[\'skin_logo\'] ='):
                    file_content[i] = f'$config[\'skin_logo\'] = /service_logo.png'
                if file_content[i].startswith('$config[\'plugins\'] ='):
                    index = i + 1
            content_to_add = ['    \'managesieve\',', '    \'password\',']
            for line in content_to_add[::-1]:
                file_content.insert(index, line)
            with open('/etc/roundcube/config.inc.php', 'w') as file:
                file.write('\n'.join(file_content))

    except Exception as e:
        log('ERROR', caller_function, f'Error while editing file `{file_name}`\n{set(e)}')
        print(f'{Color.fg.red}[-] Error while editting the file `{file_name}`:{Color.reset}')
        print(f'{Color.bg.red}{str(e)}{Color.reset}')
        sys.exit()
    
    log('SUCCESS', caller_function, f'Successfully edited the file `{file_name}`')


def setup_rspamd_edit_files(file_name):
    caller_function = inspect.stack()[1].function
    try:
        log('INFO', caller_function, f'Editing file: `{file_name}`')
        if file_name == '/etc/dovecot/conf.d/90-sieve.conf':
            file_content = str()
            with open('/etc/dovecot/conf.d/90-sieve.conf', 'r') as file:
                file_content = file.read().split('\n')
            index = int()
            for i in range(len(file_content)):
                if file_content[i].startswith('  #sieve_after ='):
                    file_content[i] = '  sieve_after = /etc/dovecot/sieve-after'
                if file_content[i].startswith('plugin {'):
                    index = i + 1
            content_to_add = DOVECOT_AUTO_LEARN_CONF_FILE_CONTENT.split('\n')
            for line in content_to_add[::-1]:
                file_content.insert(index, line)
            with open('/etc/dovecot/conf.d/90-sieve.conf', 'w') as file:
                file.write('\n'.join(file_content))
        
        elif file_name == '/etc/dovecot/conf.d/20-imap.conf':
            file_content = str()
            with open('/etc/dovecot/conf.d/20-imap.conf', 'r') as file:
                file_content = file.read().split('\n')
            for i in range(len(file_content)):
                if file_content[i].startswith('  #mail_plugins ='):
                    file_content[i] = '  mail_plugins = $mail_plugins quota imap_sieve'
                    break
            with open('/etc/dovecot/conf.d/20-imap.conf', 'w') as file:
                file.write('\n'.join(file_content))

    except Exception as e:
        log('ERROR', caller_function, f'Error while editing file `{file_name}`\n{set(e)}')
        print(f'{Color.fg.red}[-] Error while editting the file `{file_name}`:{Color.reset}')
        print(f'{Color.bg.red}{str(e)}{Color.reset}')
        sys.exit()

    log('SUCCESS', caller_function, f'Successfully edited the file `{file_name}`')

def setup_dkim_extract(output):
    pattern = re.compile(r'(-+BEGIN PRIVATE KEY-+)(.*?)(-+END PRIVATE KEY-+)', re.DOTALL)
    dkim_key_match = pattern.search(output)
    key = dkim_key_match.group(0)
    dns = f'{output.replace(key, "").strip()}'

    return key, dns