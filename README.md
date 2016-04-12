# Flock

### Requirements

- MongoDB
- Redis

### Ubuntu Install Notes

#### Libraries

**LXML**

- apt-get install -y libxml2-dev libxslt1-dev zlib1g-dev python3-pip
- apt-get install libxml2-dev libxslt1-dev python-dev
- apt-get install python-lxml

#### Startup Scripts

**App**
- chown root flock
- chmod a+x flock
- update-rc.d flock defaults

**Celery**
- chown ubuntu flock-celery
- chmod a+x flock-celery
- update-rc.d flock-celery defaults
