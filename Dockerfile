FROM apache/airflow:latest

# Switch to root to install packages and copy files
USER root

# Update package list and install required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Switch back to airflow user for pip install
USER airflow

# Install specific versions of pendulum and any other specific dependencies
RUN pip install --no-cache-dir pendulum==2.0.3

# Copy requirements.txt and install necessary Python packages
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Ensure the correct Airflow version is installed (optional, if needed)
RUN pip install --no-cache-dir apache-airflow-providers-openlineage==1.9.1 \
    apache-airflow-providers-hashicorp==3.7.1

# Set environment variables if necessary
ENV AIRFLOW__CORE__FERNET_KEY=${AIRFLOW__CORE__FERNET_KEY}
ENV AIRFLOW__CORE__SQL_ALCHEMY_CONN=${AIRFLOW__CORE__SQL_ALCHEMY_CONN}
ENV AIRFLOW__CORE__EXECUTOR=LocalExecutor
ENV AIRFLOW__CORE__LOAD_EXAMPLES=false

# Switch to root to copy DAGs and other resources
USER root

# Copy your DAGs folder and any other required files
COPY airflow_dags/ /opt/airflow/dags/
COPY plugins/ /opt/airflow/plugins/

# Updated path to copy kafka_scripts to the correct location
COPY kafka_scripts/ /youtube_sentiment_pipeline/kafka_scripts/

# Switch back to airflow user for the runtime
USER airflow

# Remove the ENTRYPOINT line to avoid conflicts
# ENTRYPOINT ["airflow"]
