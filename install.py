from tasks import *

try:
    '''START'''
    init_log()
    clear_screen()
    print_welcome_text()
    print()

    '''PRE CHECKS'''
    print(f'{Color.fg.pink}===== STARTING PRE-CHECKS ====={Color.reset}')
    check_os()
    check_user()
    print()

    '''VARIABLE COLLECTION'''
    print(f'{Color.fg.pink}===== STARTING VARIABLE COLLECTION ====={Color.reset}')
    collect_variables()
    print()

    '''INSTALLATION'''
    print(f'{Color.fg.pink}===== STARTING INSTALLATION ====={Color.reset}')
    install_packages()
    setup_http_site()
    get_ssl_cert()
    setup_https_site()
    setup_mysql_database()
    setup_postfix_for_mysql()
    setup_dovecot()
    setup_lmtp()
    setup_quotas()
    setup_roundcube()
    setup_postfix_relay()
    setup_rspamd()
    setup_dkim()
    print()

    '''COMPLETE'''
    print(f'{Color.fg.pink}===== INSTALLATION COMPLETE ====={Color.reset}')
    print_install_complete_text()



except KeyboardInterrupt:
    n = '\n'
    print(f'{n}{Color.fg.red}[-] ^C Detected, Stopping....{Color.reset}')
except Exception as e:
    print(f'{Color.fg.red}[-] Some unhandled exception occured:{Color.reset}')
    print(f'{Color.bg.red}{str(e)}{Color.reset}')