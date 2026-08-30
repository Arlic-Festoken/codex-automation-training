FROM python:3.12-slim

WORKDIR /app
COPY mock_incident_api.py check_incident_api.py ./
EXPOSE 8014
CMD ["python", "mock_incident_api.py"]
