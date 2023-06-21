#This is not ready for widespread distibution yet.#

## What does PasswordSafe do?##

PasswordSafe Tkinter based UI to store your passwords, logins, gpg-keys and
smime-keys in a single file.
The passwordfile is PGP-encrypted and use your selected PGP-key.

Features are:
- can store web logins
- can store ascii-based GPG and SMime secret and public keys
- stores additional information (i.e. notes) on secrets
- keeps history when changing information on secrets
- auto locks the user interface
- easy searchable and selectable secrets
- can handle multiple password files with multiple keys
  (when configured in options manually)

## INSTALL INSTRUCTIONS##

### Linux (with provided script)

We provide a script to install PasswordSafe:

1.   clone the project (git clone...)
2.   switch into scripts directory
3.   execute 
     ```
     ./linux-installer.sh --install
     ```
4.   For help use
     ```
     ./linux-installer.sh --usage
     ```

### Manual installation

#### Dependencies

* python
* gnupg
* python-gnupg
* tk
* python-tk
* python-enum34 (when using python2)

##### Archlinux:

	you need python-gnupg (available in aur)

##### Other:

	see the above and get your own packages
