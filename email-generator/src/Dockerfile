FROM python:3.11

##Install Cron
RUN apt-get update &&\
    apt-get install -y cron


WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade pip &&\
    pip install --no-cache-dir -r requirements.txt

COPY .. .

# Add crontab file in the cron directory
COPY crontab /etc/cron.d/crontab

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/crontab

# Apply cron job
RUN /usr/bin/crontab /etc/cron.d/crontab

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Give execution rights on python scripts
RUN chmod +x /app/cron_jobs

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log
