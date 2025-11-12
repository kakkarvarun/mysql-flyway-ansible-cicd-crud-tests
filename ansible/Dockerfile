FROM python:3.11-slim

# Ansible + Docker SDK for Python + MySQL client for quick checks
RUN pip install --no-cache-dir ansible docker \
 && apt-get update \
 && apt-get install -y --no-install-recommends mysql-client curl \
 && rm -rf /var/lib/apt/lists/*

# Pull the community.docker collection (gives docker_* modules)
RUN ansible-galaxy collection install community.docker

WORKDIR /work
ENTRYPOINT ["ansible-playbook"]
