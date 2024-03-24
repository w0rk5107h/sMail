import subprocess
from color import Color
import sys
import os

# run sql query
def run_sql_query(lines, error_message):
    shell = ''
    try:
        shell = subprocess.Popen(['/bin/bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except Exception as e:
        print(f'{Color.fg.red}[-] Some error occured while opening a /bin/bash shell:{Color.reset}')
        print(f'{Color.bg.red}{str(e)}{Color.reset}')
        sys.exit()
    try:
        n = '\n'
        for line in lines:
            shell.stdin.write(line + '\n')
        shell.stdin.flush()
        out, err = shell.communicate()
        shell.terminate()
        err = err.split('\n')
        err = [x for x in err if x]
        if len(err):
            err = '\n'.join(err)
            print(f'{Color.fg.red}{error_message}{Color.reset}')
            print(f'{Color.bg.red}{err}{Color.reset}')
            sys.exit()
    except Exception as e:
        shell.terminate()
        n = '\n'
        print(f'{Color.fg.red}[-] Some error occured while running the command: {Color.reset}{Color.bg.red}{n.join(lines)}{Color.reset}')
        print(f'{Color.bg.red}{str(e)}{Color.reset}')
        sys.exit()

    n = '\n'
    return out

# run command
def run_command(command, error_message):
    shell = ''
    try:
        shell = subprocess.Popen(['/bin/bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except Exception as e:
        print(f'{Color.fg.red}[-] Some error occured while opening a /bin/bash shell:{Color.reset}')
        print(f'{Color.bg.red}{str(e)}{Color.reset}')
        sys.exit()
    try:
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
            print(f'{Color.fg.red}{error_message}{Color.reset}')
            print(f'{Color.bg.red}{err}{Color.reset}')
            sys.exit()
    except Exception as e:
        shell.terminate()
        print(f'{Color.fg.red}[-] Some error occured while running the command: {Color.reset}{Color.bg.red}{command}{Color.reset}')
        print(f'{Color.bg.red}{str(e)}{Color.reset}')
        sys.exit()

    return out

if __name__ == '__main__':

    if os.getuid():
        print(f'{Color.fg.red}[-] Run this with sudo or as root.{Color.reset}')
        sys.exit()
    domain = input(f'{Color.fg.cyan}[>] Enter the domain that you want to add: {Color.reset}')
    command_lines = [
        'mysql -u root',
        'USE mailserverdb;',
        'SELECT * FROM virtual_domains;',
        'quit'
    ]
    out = run_sql_query(command_lines, '[-] Error while fetching all domains from table `virtual_domains`:')
    out = out.split('\n')
    out = [x for x in out if x]
    for i in range(len(out)):
        out[i] = out[i].split('\t')
        out[i] = [x for x in out[i] if x]
    command_lines = [
        'mysql -u root',
        'USE mailserverdb;',
        f'INSERT INTO virtual_domains VALUES({int(out[-1][0]) + 1}, \'{domain}\');',
        'quit'
    ]
    _ = run_sql_query(command_lines, f'[-] Error while adding `{domain}` to `virtual_domains`:')
    print(f'{Color.fg.green}[+] `{domain}` added to `virtual_domains`.{Color.reset}')
    _ = run_command('service postfix restart', '[-] Error while restarting postfix:')