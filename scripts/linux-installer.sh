#!/bin/sh -e

# Installer script for PasswordSafe
# Supports at the moment all linux distributions that use pacman or zypper
# (Arch, openSUSE, Ubuntu etc).

# Name of the program
NAME=PasswordSafe

# where to install python files (will be installed in $DEFAULT_INSTALL_PATH/$NAME)
DEFAULT_INSTALL_PATH="/opt"

# where to install executable (should be in PATH)
DEFAULT_BIN_PATH="/usr/local/bin"

# where to same settings etc.
DEFAULT_PROFILE_PATH=".$NAME" #relative to home

REQUIRED_PYTHON_PARSER=python2 #at the moment 2 (aka 2.7) maybe 3.x in the future

usage()
{
    echo ""
    echo "Usage:"
    echo ""
    echo "./linux-installer.sh <cmd>"
    echo "    where <cmd> is one of:"
    echo "      --install     (does full installation.)"
    echo "      --uninstall   (uninstalls all of $NAME)"
    echo ""
    echo "example:"
    echo '    $ ./linux-installer.sh --install'
}


install_prerequisites()
{
    # Find a package manager, PM
    PM=$( command -v pacman || command -v zypper || command -v apt-get )

    # assume all arch systems have same prerequisites
    if [ "$(expr match "$PM" '.*\(pacman\)')" == "pacman" ]; then
        #echo "debian compatible system"
        prerequisite_list="
            python2
            tk
            gnupg
       "

        for p in ${prerequisite_list}
        do
            sudo pacman -S $p || exit 1
        done

        # only in AUR
        aur_prerequisites="
                python2.7-gnupg
            "

        for sp in ${scripting_prerequisites}
        do
            sudo yaourt -S $sp || exit 1
        done

    # assume all zypper systems like openSUSE have same prerequisites
    elif [ "$(expr match "$PM" '.*\(zypper\)')" == "zypper" ]; then
        #echo "openSUSE compatible system"
        prerequisite_list="
            python
            python-tk
            python-gnupg
        "

        for p in ${prerequisite_list}
        do
            sudo zypper in $p || exit 1
        done
    elif [ "$(expr match "$PM" '.*\(apt-get\)')" == "apt-get" ]; then
        #echo "Ubuntu compatible system"
        prerequisite_list="
            python
            python-tk
            python-gnupg
        "

        for p in ${prerequisite_list}; do
            sudo apt-get install $p || exit 1
        done
    else
        echo
        echo "Incompatible System. Neither 'pacman' nor 'zypper' nor 'apt-get' found. Not possible to continue."
        echo
        exit 1
    fi

}

install_files()
{
    cd ..
    if [ -d "$DEFAULT_INSTALL_PATH/$NAME" ]; then
        sudo rm -r "$DEFAULT_INSTALL_PATH/$NAME"
    fi
    sudo mkdir -p "$DEFAULT_INSTALL_PATH/$NAME"
    sudo cp -r src/* "$DEFAULT_INSTALL_PATH/$NAME"
    cd "$DEFAULT_INSTALL_PATH/$NAME"
    sudo sed -i "s,/Documents/.PasswordSafe,/$DEFAULT_PROFILE_PATH,g" controller/maincontroller.py
}

install_it()
{
    echo "step 1) installing pre-requisites"
    install_prerequisites

    echo "step 2) installing $NAME program files..."
    install_files
    echo " $NAME program files installed."


    echo "step 3) installing starter..."
    cd "$DEFAULT_BIN_PATH"
    if [ -f "$NAME" ]; then
        rm "$NAME"
    fi
    sudo sh -c "echo -e \"#!/bin/bash\n\" \
                 \"$REQUIRED_PYTHON_PARSER $DEFAULT_INSTALL_PATH/$NAME/$NAME.py\n\" >> \"$NAME\""
    sudo chmod +x "$NAME"
    echo " $NAME installed."

    echo
    echo "All $NAME "--install" steps completed, you are up to date."
    echo
}

uninstall_it()
{
    echo "Uninstalling program files"
    sudo rm -r "$DEFAULT_INSTALL_PATH/$NAME"
    sudo rm "$DEFAULT_BIN_PATH/$NAME"
    echo "Uninstalling of $NAME complete"
}

if [ $# -eq 1 -a "$1" == "--install" ]; then
    install_it
    exit
fi

if [ $# -eq 1 -a "$1" == "--uninstall" ]; then
    uninstall_it
    exit
fi

usage
