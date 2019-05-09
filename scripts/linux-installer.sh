#!/bin/sh -e

# Installer script for PasswordSafe
# Supports at the moment all linux distributions that use pacman, zypper and apt-get
# (Arch, openSUSE, Ubuntu / Debian etc).

# Name of the program
NAME=PasswordSafe

# where to install python files (will be installed in $DEFAULT_INSTALL_PATH/$NAME)
DEFAULT_INSTALL_PATH="/opt"

# where to install executable (should be in PATH)
DEFAULT_BIN_PATH="/usr/local/bin"

# where to same settings etc.
DEFAULT_PROFILE_PATH=".$NAME" #relative to home

# Password Safe is compatible with python 2.7 and python 3.4
REQUIRED_PYTHON_PARSER=python3

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
    if $(test "$(expr match "$PM" '.*\(pacman\)')" = "pacman" ); then
        #echo "archlinux compatible system"
	# default python is python 3.5
        prerequisite_list="
            python
            tk
            gnupg
       "

        for p in ${prerequisite_list}
        do
            sudo pacman -S $p || exit 1
        done

        # only in AUR
        scripting_prerequisites="
                python-gnupg
            "

        for sp in ${scripting_prerequisites}
        do
            sudo yaourt -S $sp || exit 1
        done

    # assume all zypper systems like openSUSE have same prerequisites
    elif $(test "$(expr match "$PM" '.*\(zypper\)')" = "zypper" ); then
        #echo "openSUSE compatible system"
	# default python is python 2.7
        prerequisite_list="
            python
            python-tk
            python-gnupg
            python-enum34
        "

        for p in ${prerequisite_list}
        do
            sudo zypper in $p || exit 1
        done
    elif $(test "$(expr match "$PM" '.*\(apt-get\)')" = "apt-get" ); then
        #echo "Ubuntu / Debian compatible system"
        prerequisite_list="
            python3
            python3-tk
            python3-gnupg
        "

	sudo apt-get install ${prerequisite_list}
#        for p in ${prerequisite_list}; do
#            sudo apt-get install $p || exit 1
#        done
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
    if $(test -d "$DEFAULT_INSTALL_PATH/$NAME" ); then
        sudo rm -r "$DEFAULT_INSTALL_PATH/$NAME"
    fi
    sudo mkdir -p "$DEFAULT_INSTALL_PATH/$NAME"
    sudo cp -r src/* "$DEFAULT_INSTALL_PATH/$NAME"
    sudo cp -r freedesktop/* /usr/share
    cd "$DEFAULT_INSTALL_PATH/$NAME"
    sudo sed -i "s,/Documents/.PasswordSafe,/$DEFAULT_PROFILE_PATH,g" controller/Environment.py
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
    if $(test -f "$NAME" ); then
        rm "$NAME"
    fi
    sudo sh -c "echo \"#!/bin/bash\n\" \
                 \"$REQUIRED_PYTHON_PARSER $DEFAULT_INSTALL_PATH/$NAME/$NAME.py\n\" > \"$NAME\""
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
    echo "Uninstalling desktop files"
    pushd ../freedesktop
    for i in $(find . -type f); do
	if [ -e /usr/share/"$i" ]; then
	    sudo rm /usr/share/"$i"
	fi
	done
    popd
    echo "Uninstalling of $NAME complete"
}

if $(test $# -eq 1 -a "$1" = "--install" ); then
    install_it
    exit
fi

if $(test $# -eq 1 -a "$1" = "--uninstall" ); then
    uninstall_it
    exit
fi

usage
