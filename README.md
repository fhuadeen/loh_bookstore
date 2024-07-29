# loh_bookstore

## Architecture Approach
Following a somewhat Layered-Microservice architecture, we have the data access (database and messaging) layer in a different project (deployed on Github), which can be installed via `pip`.

With this design, it decouples the app from the type of data access tools used. Although we currently implemented Postgres with SQLAlchemy for the database, and RabbitMQ for between-app communications, it allows us to easily extend or modify the API to support other tools.

## How to set up
1. Create a github token for installing the `loh_utils` private repo package.

2. Open `requirements.txt` in each service and replace `<github-access-key>` in `git+https://<github-access-key>@github.com/fhuadeen/loh_utils.git` with the Github token generated.

3. Use any of the below set up options:
### Run without Docker
1. Create Python virtual environment
```bash
python3 -m venv venv
```
2. Navigate to service directory and run to create `.env` file (Modify the file with right values after creating):
```bash
cp .env.template .env
```

3. Run:
```bash
python api/app.py
```

### Run in Docker
Navigate to each service directory and:
1. Run to build the image (replace `service_name` with service name)
```bash
docker build -t service_name .
```
2. Navigate to service directory and run to create `.env` file (Modify the file with right values after creating):
```bash
cp .env.template .env
```

3. Run command to start the container (Change port names for each service respectively)
```bash
docker run --env-file .env -p 5000:5000 service_name
```

### Run in Kubernetes (Recommended)
Check `loh_infra` repo for instructions

### service: port
- gateway: 5000
- inventory: 5001
- oms: 5002
- payment: 5003
- notifications: 5004
- ai_service: 5005
