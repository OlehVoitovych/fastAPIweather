# set up your .env in Config/
```bash
AWS_ACCESS_KEY_ID=some_value
AWS_SECRET_ACCESS_KEY=some_value
AWS_DEFAULT_REGION=some_value
API_KEY=some_value
S3_BUCKET_NAME=some_value
DYNAMODB_TABLE=some_value
```

# run localy 
```bash
cd ~/fastAPIweather
uvicorn main:app --reload
```

# run docker
```bash
cd ~/fastAPIweather
docker compose up --build
```
