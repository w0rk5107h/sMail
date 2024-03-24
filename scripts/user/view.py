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

if __name__ == '__main__':

    if os.getuid():
        print(f'{Color.fg.red}[-] Run this with sudo or as root.{Color.reset}')
        sys.exit()
    command_lines = [
        'mysql -u root',
        'USE mailserverdb;',
        'SELECT * FROM virtual_users;',
        'quit'
    ]
    out = run_sql_query(command_lines, '[-] Error while fetching all users from table `virtual_users`:')
    out = out.split('\n')
    out = [x for x in out if x]
    for i in range(len(out)):
        out[i] = out[i].split('\t')
        out[i] = [x for x in out[i] if x]
    print(f'{Color.fg.green}[+] {len(out[1:])} users found:{Color.reset}\n')
    lines = []
    for i in out[1:]:
        item = []
        for j in range(len(i)):
            if out[0][j] == 'password':
                continue
            item.append(f'{Color.fg.cyan}{out[0][j]}:{Color.reset} {Color.fg.green}{i[j]}{Color.reset}')
        item = '\n'.join(item)
        lines.append(item)
    print('\n\n'.join(lines))