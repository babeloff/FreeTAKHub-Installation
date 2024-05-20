![CI](https://github.com/FreeTAKTeam/FreeTAKHub-Installation/actions/workflows/zerotouch.yml/badge.svg)

This page is for developers of the Zero Touch Installer for [FreeTAKServer](https://github.com/FreeTAKTeam/FreeTakServer).
Please refer to the [official documentation ](https://freetakteam.github.io/FreeTAKServer-User-Docs/) for usage.

# Configuring the Development Environment

## Cloning the Repository

Clone the origin repository.
The following is the official repository.
```bash
git clone --origin upstream https://github.com/FreeTAKTeam/FreeTAKHub-Installation.git ${HOME}/fth-install
```

You will want to commit your work into a fork of the repository.
```bash
pushd  ${HOME}/fth-install
git remote add origin <url-of-fork>
```

# Running the ZTI locally

You will need some variant of Ubuntu 22.04 on your development machine.
The following will install FTS on your development machine.
```bash
cat ./scripts/easy_install.sh | sudo bash -s -- --verbose
```

This will install the production repository,
unless you are modifying `scripts/easy_install.sh` you will want your cloned repository.

The following will remove any previously retrieved repository replacing it with a clone of the provided one.
```bash
pushd  ${HOME}/fth-install
cat ./scripts/easy_install.sh | sudo bash -s -- --verbose --repo file://$(pwd)/.git --ip-addr 127.0.0.1
```

So long as you are working with the same git repository the `--repo` option could (and should)
be omitted from subsequent runs as the default is to reuse the clone.


## Regression Testing the ZTI

The ZTI is officially supported on the following platforms:

* Raspberry Pi
* [Ubuntu Server](docs/ubuntu_vm_test.md)
* Digital Ocean Cloud


# Running Ansible Remotely

The ZT installer is a bash script which installs Ansible and runs a playbook.
During development, it will be more efficient to run Ansible remotely.
Remotely is the typical mode for running Ansible.

You will need some variant of Ubuntu 22.04 on your target machine.

## Setup (mimic `scripts/easy_install.sh`)

This will install the production repository,
unless you are modifying `scripts/easy_install.sh` you will want your cloned repository.

Note that Ansible does not run on Windows.
https://docs.ansible.com/ansible/latest/os_guide/windows_faq.html

It does run from the Windows Subsystem for Linux (WSL2).
```bash
git clone https://github.com/FreeTAKTeam/FreeTAKHub-Installation.git fts-install
```

https://docs.ansible.com/ansible/latest/cli/ansible-playbook.html

```bash
export FTS_IP_CUSTOM="172.23.80.2"

export CODENAME="jammy"
export INSTALL_TYPE="stable"
export PY3_VER="3.11"
export FTS_VERSION="2.2.1"
export FTS_VENV="/opt/fts.venv"
export CFG_RPATH="core/configuration"
export OS_REQD="Ubuntu"
export OS_VER_REQD="22.04"

env_vars1="python3_version=$PY3_VER codename=$CODENAME itype=$INSTALL_TYPE"
env_vars2="fts_version=$FTS_VERSION cfg_rpath=$CFG_RPATH fts_venv=$FTS_VENV"
env_vars3="fts_ip_addr_extra=$FTS_IP_CUSTOM"
env_vars4="pypi_url=$PYPI_URL"
env_vars5="webmap_force_install=true"

```
Now we can install using a playbook on a target machine
```bash
export APB=install_all

ansible-playbook \
  --user root  \
  --connection ssh \
  --inventory mcp-x \
  --extra-vars "$env_vars1" \
  --extra-vars "$env_vars2" \
  --extra-vars "$env_vars3" \
  --extra-vars "$env_vars4" \
  --extra-vars "$env_vars5" \
  -vvvv \
  ${APB}.yml
```
Adding multiple -v will increase the verbosity,
the builtin plugins currently evaluate up to -vvvvvv.
A reasonable level to start is -vvv,
connection debugging might require -vvvv.

