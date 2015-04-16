#This is not ready for widespread distibution yet.#

## What does PasswordSafe do?##

PasswordSafe is an easy (soon) to use piece of software that can store your passwords and logins.
Best part is, they are PGP-encrypted and use your own keyfile, so no bad, bad person or government can get them without the password.

## INSTALL INSTRUCTIONS##

### Linux (with provided script)

We provide a script to install PasswordSafe:

1.   clone the project (git clone...)
2.   switch into scripts directory
3.   execute 
     ```
     linux-installer.sh
     ```
4.   For help use
     ```
     linuxinstaller.sh --usage
     ```

### Manual installation

#### Dependencies

* python 2.7
* gnupg
* python-gnupg
* tk
* python-tk

##### Archlinux:

	you need to have python2.7 installed as wenn as tk and python2.7-gnupg (available in aur)

##### Other:

	see the above and get your own packages
