# <p style="text-align: center;">sMail</p>
###### <p style="text-align: center;">A personal self hosted/managed mail service.</p>

---

This project aims to set up a personal mail service using various components like Postfix, Dovecot, Rspamd etc providing you with a robust email infrastructure for personal or very small enterprise use.

---

## 1. Components Used
| **Component** | **Description**       |
|-----------|-------------------|
| Postfix   | Mail transfer agent (MTA) for routing and delivering email. |
| Dovecot   | IMAP and POP3 server for managing user mailboxes. |
| Rspamd    | Spam filtering system for protecting against unwanted emails. |
| Roundcube | Web-based IMAP email client for accessing emails through a browser. |
| MariaDB | Backend database for postfix to store users, domains and aliases. |
| Redis | Database used by Rspamd to store ham/spam rules. |
| Apache2 | Webserver for accessing the service on web. |
| Certbot | For issuing SSL certificates. |

---

## 2. Pre-Requisites
Before you begin, these are some things that are needed to be done/checked:

### 2.1 *OS*
This installer only works with `Debian 12` and it has only been tested on that. If you wish to install this on some other distribution, do that on your own risk.

It is also advised to install this on a brand new server.

### 2.2 *Update/Upgrade*
Before installing you should update and upgrade all the packages of your server. This can be done with a simple command:

    sudo apt update && sudo apt upgrade -y

### 2.3 *Packages*
Before you begin make sure these 3 packages are installed:
- `python3`: To run the scripts.
- `python3-bcrypt`: To hash passwords in Blf-Crpt algo.
- `git`: To clone this repo to the server.
- `tmux`: [Optional] [Recommended] For redundancy if ssh session crashes.

This can be done with a simple command:

    sudo apt install -y python3 python3-bcrypt git tmux

### 2.4 *DNS and Hostname*
Before you begin you must decide a hostname for your server. This is how your server will be known on the internet.

For example, if you are making a mail service for `@foo.bar`, then you can keep your hostname either one:
- `mail.foo.bar`
- `webmail.foo.bar` etc...

After deciding a hostname, you must change your servers hostname to the chosen hostname. You can do this by editting the file `/etc/hostname`.

You also must add this chosen hostname as an 'A' record in your DNS, and it should point to the mail server's IP.

    mail.foo.bar	A	x.x.x.x

It is also recommended to also set the rDNS record for the mail server which should point to `mail.foo.bar`

    x.x.x.x -> mail.foo.bar

### 2.5 *Allow HTTP traffic*
You need to allow http traffic to your server as in the installation process, an SSL certificate will be requested using HTTP. 

For this allow inbound connection from port 80 on your server.

### 2.6 *Reboot*
After all this it is advised to reboot your system once. This can be done with the command:

    reboot

---

## 3. Installation
The installation process is fairly simple and self-explanatory.

First, it is advices to launch a `tmux` session, so that way even if the ssh session crashes during the installation. You wont loose your terminals. This can be done by running:

    tmux

Second, clone this repo, and change directory:

    git clone https://github.com/w0rk5107h/sMail
    cd sMail

Now to install the service just run this command (make sure you either run this with `sodu` or as `root`):

    python3 install.py

During the execution of this, you will be prompted to enter a few inputs:

- `Server FQDN`: In this enter the hosname that you decided the the above step.
- `Mail DN`: In the enter the domain that you with to have in your email address.
- `DKIM Selector`: In this enter the DKIM selector that you wish to use. (If you are not aware what DKIM is `google it`).

When the installation is complete you will be greeted with a `Congratulations` message, with all the config that was used for the installation. The same config is also present in the `.CONFIG` file that was created. You can save that fiel locally in a secure manner.

Basic installation logs will be displayed on the screen while the `install.py` script runs. If you want more detailed logs there is a dedicated log file for the same `install.log`.

---

## 4. Post-Requisites
After the installation is successfull, you still need to do a couple of things for your mail server to run.

### 4.1 *DNS Records*
You will need to add some DNS records for this service to work, here is a list of DNS records that are needed to be added. I won't be explaining in detail of how/why to add these records. You can find all this on google easily.

| DNS Record | Description |
|------------|-------------|
| MX Records | These records are used by other mail servers to know who handles the mail for a specific domain. |
| SPF Records | Indicating that only the mail server is permitted to send emails from the domain. |
| DKIM Records | Providing a way for recipients to verify emails sent from the domain. |
| DMARC Records | DMARC records define policies for how email receiving servers should handle emails that fail authentication checks performed by SPF and DKIM. |

These are the basic DNS records required for the mail service.

The DKIM public key is present in the `.CONFIG` file.

### 4.2 *Port Forwarding*
You will need to allow some inbound ports for this mail server to work. Here is a list of all the ports you need to allow:

| Ports | Description |
|-------|-------------|
| 80 | HTTP |
| 443 | HTTPS |
| 143 | IMAP |
| 993 | IMAPS |
| 110 | POP3 |
| 995 | POP3S |
| 25 | SMTP |
| 587 | SMTPS |
| 4190 | Maanage SIEVE |

---

## 5. Accessing Mail
You can access your mail either from the web or you can also add the mail accounts in any other mail client.

To add account in the 3rd party mail client you'll need to add the server details manually, find below the configuration to enter in the mail client:

    #SMTP Conf# (Sometimes mentioned as `Outgoing Server`)

    Username: user@foo.bar
    Password: password
    Server: mail.foo.bar
    Security Type: STARTTLS
    Port: 587



    #IMAP Conf# (Sometimes mentioned as `Incomming Server`)

    Username: user@foo.bar
    Password: password
    Server: mail.foo.bar
    Security Type: SSL/TLS
    Port: 993

Please note that `Email` and `Username` are used interchangeably in most cases. So you can use email as the username while setting up your mail in 3rd party mail clients.

I personally prefer using [MailSpring](https://github.com/Foundry376/Mailspring) as a mail client. It s compatible with all operating systems (*nix and windows).
For MacOS the default mail client is also good enough.

---

## 6. Manage Users/Aliases/Domains
There are scripts in the repo to create/view/edit/delete Users/Aliases/Domains. You can run those for the respective tasks.

Below mentioned are all the scripts:

### 6.1 *Scripts for managing users*
- `./scripts/user/add.py`: To add a user.
- `./scripts/user/view.py`: To view all users.
- `./scripts/user/edit.py`: To edit a user.
- `./scripts/user/delete.py`: To delete a user.
### 6.2 *Scripts for managing domains*
- `./scripts/domain/add.py`: To add a domain.
- `./scripts/domain/view.py`: To view all domains.
- `./scripts/domain/edit.py`: To edit a domain.
- `./scripts/domain/delete.py`: To delete a domain.
### 6.3 *Scripts for managing aliases*
- `./scripts/alias/add.py`: To add an alias.
- `./scripts/alias/view.py`: To view all aliases.
- `./scripts/alias/edit.py`: To edit an alias.
- `./scripts/alias/delete.py`: To delete an alias.

These all scripts are pretty self explanatory you just have to run them and it will tell you what it needs.

---

## 7. Upcoming features
- A web based dashboard to manage the service.
- MTA-STS

---

## 8. Bug report
If you happen to find a bug in this, please feel free to create an issue in github itself. I will check it as soon as possible.

---

## 9. Contribution
If you feel you can improve this project or just want to contribute something to this, feel free to create a pull request.

---

### 10. License
This project is licenced under the [MIT LICENSE](https://mit-license.org/)

---
