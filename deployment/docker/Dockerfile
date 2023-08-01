FROM python:3.10.4-buster AS base

RUN apt-get update -y && apt-get upgrade -y && \
    apt-get install -y \
    gcc gettext cron \
    spatialite-bin libsqlite3-mod-spatialite \
    python3-dev python3-gdal python3-psycopg2 python3-ldap \
    python3-pip python3-pil python3-lxml python3-pylibmc \
    uwsgi uwsgi-plugin-python3 libgdal-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY deployment/docker/requirements.txt /requirements.txt
RUN pip install --upgrade pip && \
    pip install -r /requirements.txt

FROM base AS node

RUN curl -sL https://deb.nodesource.com/setup_16.x -o nodesource_setup.sh && \
    bash nodesource_setup.sh && \
    apt-get install -y nodejs && \
    rm nodesource_setup.sh

# Tegola
RUN wget https://github.com/go-spatial/tegola/releases/download/v0.16.0/tegola_linux_amd64.zip -P /home/web/ && \
    unzip /home/web/tegola_linux_amd64.zip -d /opt/ && \
    rm /home/web/tegola_linux_amd64.zip

FROM node AS prod

ADD django_project /home/web/django_project

EXPOSE 8080

ADD deployment/docker/uwsgi.conf /uwsgi.conf

# Build front end
WORKDIR /home/web/django_project/frontend
RUN npm install --legacy-peer-deps && npm run build

WORKDIR /home/web/django_project
ENTRYPOINT ["/home/web/django_project/entrypoint.sh"]
CMD ["uwsgi", "--ini", "/uwsgi.conf"]

FROM prod as vscode

ADD deployment/docker/requirements-dev.txt /requirements-dev.txt
RUN pip install -r /requirements-dev.txt

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    #
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# ********************************************************
# * Anything else you want to do like clean up goes here *
# ********************************************************

# [Optional] Set the default user. Omit if you want to keep the default as root.
USER $USERNAME

FROM node as dev
# Install ssh server
RUN apt-get update && apt-get install -y openssh-server sudo && \
    mkdir /var/run/sshd && \
    echo 'root:docker' | chpasswd && \
    sed -i 's/^PermitRootLogin */#PermitRootLogin /' /etc/ssh/sshd_config && \
    echo "PermitRootLogin yes" >> /etc/ssh/sshd_config && \
    sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
# SSH login fix. Otherwise user is kicked off after login
ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile
# End of cut & paste section
# Install dev dependencies
COPY deployment/docker/requirements-dev.txt /requirements-dev.txt
RUN pip install -r /requirements-dev.txt

WORKDIR /home/web/django_project


# Open port 8080 as we will be running our django dev server on
EXPOSE 8080
# Open port 22 as we will be using a remote interpreter from pycharm
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]

FROM node as test

ADD django_project /home/web/django_project

WORKDIR /home/web/django_project

# Open port 8080 as we will be running our django dev server on
EXPOSE 8080
