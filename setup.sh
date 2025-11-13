#!/usr/bin/env bash
set -euo pipefail

sudo yum update -y
sudo yum install -y python3 python3-pip git

PROJECT_DIR="AWS-PrimeraEntrega"
REPO_URL="<URL_DEL_REPOSITORIO>"

if [[ ! -d ${PROJECT_DIR} ]]; then
  git clone "${REPO_URL}" "${PROJECT_DIR}"
fi

cd "${PROJECT_DIR}"
pip3 install --upgrade pip
pip3 install -r requirements.txt
python3 app.py
