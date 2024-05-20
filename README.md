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

Typically, Ansible is run from a control-node which updates managed-nodes.
In this case we have just one managed-node.

### Install Ansible on the control-node

```bash
which apt-add-repository >/dev/null || sudo apt-get install --yes software-properties-common
sudo apt-add-repository -y ppa:ansible/ansible

sudo apt-get update
sudo apt-get install -y ansible
sudo apt-get install -y git
```

## Clone Repository onto a control-node

Typically, Ansible is run from a control-node which updates managed-nodes. 

### Clone from the Github Project Repository
Note that the control-node can not be running Windows.
* https://docs.ansible.com/ansible/latest/os_guide/windows_faq.html
* https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#control-node-requirements

Therefore, this first approach does not work on Windows.
```bash
git clone https://github.com/FreeTAKTeam/FreeTAKHub-Installation.git fts-install
```

### ... onto a `multipass` Ubuntu VM from a Working git Repository
```powershell
multipass mount C:\Users\feisele\ primary:/home/ubuntu/self
```
Then from the `multipass` VM instance.
```bash
git clone file:///home/ubuntu/self/fts-install/.git fts-install
```

### ... onto a Windows Subsystem for Linux (WSL2) from a Working git Repository
```powershell
multipass mount C:\Users\feisele\ primary:/home/ubuntu/self
```
Then from the `multipass` VM instance.
```bash
git clone file:///mnt/c/Users/feisele/fts-install/.git fts-install
```

## Run the Playbook on the control-node

https://docs.ansible.com/ansible/latest/cli/ansible-playbook.html

`sample_config/latest_vars.yml`
```yaml
---
fts_ip_addr_extra: 172.23.80.2
python3_version: 3.11
codename: jammy
itype: stable
fts_version: 2.2.1
cfg_rpath: core/configuration
fts_venv: /opt/fts.venv
pypi_url: https://pypi.org/simple/
webmap_force_install: true
...
```

Select a playbook.
```bash
export APB=install_mainserver
export APB=install_murmur
export APB=install_noderedserver
export APB=install_videoserver
export APB=install_all
```

Now we can install using the playbook on a target machine.
```bash
ansible-playbook \
  --user mcp  \
  --connection ssh \
  --inventory inventory.yml \
  --private-key ~/.ssh/mcp_rsa \
  --limit phreed \
  --extra-vars "@sample_config/latest_vars.yml" \
  -vvvv \
  ${APB}.yml
```
Adding multiple -v will increase the verbosity,
the builtin plugins currently evaluate up to -vvvvvv.
A reasonable level to start is -vvv,
connection debugging might require -vvvv.

