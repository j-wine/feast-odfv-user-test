# Setup

1. Start the required services:
```bash
docker compose up -d registry redis
````

2. Prepare `feature_store.yaml` for local execution:
* **Temporarily change `feature_store.yaml` to use local paths:**

```yaml
registry:
 registry_type: sql
 path: postgresql+psycopg://postgres:mysecretpassword@localhost:55001/feast

online_store:
 type: redis
 connection_string: localhost:6379
  ```

3. Set up the offline store:

* Manually run the following script to generate the required Parquet files:

```bash
python generate_parquet_files.py
```

4. Apply Feast:

* Run:

```bash
feast apply
```

inside the `/feature_repo` directory using your local virtual environment.

5. Revert `feature_store.yaml` back to production / container paths:

```yaml
registry:
  registry_type: sql
  path: postgresql+psycopg://postgres:mysecretpassword@registry:5432/feast

online_store:
  type: redis
  connection_string: redis:6379
```

6. Start the respective Feast versionof [43,47,49]
```docker compose up feast{version}
```
