# MySQL Migrations with Flyway + Ansible Automation & GitHub Actions (CRUD tests)

End-to-end DB automation with everything run inside Docker: Ansible control container, Flyway containers, and Python test container. CI uses GitHub Actions.

## Run locally (all in Docker)
1) Build the Ansible control image:
```bash
docker build -t prog8850/ansiblectl:latest ansible

Bring up MySQL and run V1 via Ansible (mount Docker socket + mount repo):

docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "$PWD":/work \
  -e HOST_REPO=/work \
  -w /work \
  prog8850/ansiblectl:latest ansible/up.yml -i ansible/hosts.ini

Apply V2 (mount both migration folders) using Flyway container:

docker run --rm --network prog8850_net \
  --mount type=bind,source="$PWD/flyway/migrations_initial",target=/flyway/sql_initial,ro \
  --mount type=bind,source="$PWD/flyway/migrations_incremental",target=/flyway/sql_incremental,ro \
  flyway/flyway:10 \
  -locations=filesystem:/flyway/sql_initial,filesystem:/flyway/sql_incremental \
  -url="jdbc:mysql://mysql_prog8850:3306/prog8850_db?allowPublicKeyRetrieval=true&useSSL=false" \
  -user=app_user -password=app_password \
  -connectRetries=20 \
  migrate

Run tests (pytest) in a Python container:

docker run --rm \
  --network prog8850_net \
  -v "$PWD":/work -w /work \
  python:3.11-slim bash -lc "pip install -r requirements.txt && pytest -q"

Tear down:

docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "$PWD":/work \
  -w /work \
  prog8850/ansiblectl:latest ansible/down.yml -i ansible/hosts.ini

CI/CD (GitHub Actions)

MySQL service → Flyway V1 → Flyway V2 (both locations) → pytest → upload JUnit XML → echo “Deployment done for commit …”.

Q1 Report

See Q1_Tools_Analysis.md and export to PDF.

