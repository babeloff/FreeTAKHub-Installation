#!/bin/bash
set -x

echo "Initializing..."
source scripts/setup-Virtual-Env.sh
source scripts/setup-Ansible.sh
source scripts/setup-Terraform.sh
source scripts/setup-Keys.sh

set +x