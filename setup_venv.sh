#!/bin/bash
print_green(){
	printf "\033[32m%s\033[0m\n" "$*"
}

print_done() {
    print_green "Done"
}

python_venv_setup(){
	print_green "Setting up virtual environment" 
	python virtualenv.py --no-setuptools `pwd`/venv_setup 2>/dev/null
	rm -f "virtualenv.pyc"
	print_done
	`pwd`/venv_setup/bin/python get-pip.py
	`pwd`/venv_setup/bin/pip install pip
}

python_install_pip(){
	print_green "Install pip"
	python get-pip.py
	print_done
}

python_install_pip
python_venv_setup
