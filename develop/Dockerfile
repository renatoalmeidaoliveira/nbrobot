ARG python_ver=3.12
FROM python:${python_ver}

ARG netbox_ver=v4.2.2S
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /opt

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install worktory

# -------------------------------------------------------------------------------------
# Install NetBox
# -------------------------------------------------------------------------------------
RUN git clone --single-branch --branch ${netbox_ver} https://github.com/netbox-community/netbox.git /opt/netbox/ && \
    cd /opt/netbox/ && \
    pip install -r /opt/netbox/requirements.txt

# Work around https://github.com/rq/django-rq/issues/421
#RUN pip install django-rq==2.3.2
# Work around https://github.com/pallets/markupsafe/issues/284
RUN pip install markupsafe==2.0.1
RUN pip install git+https://github.com/python/tzdata
RUN pip install tblib

# -------------------------------------------------------------------------------------
# Install Netbox Plugin
# -------------------------------------------------------------------------------------
RUN mkdir -p /source
WORKDIR /source
COPY . /source

#RUN pip install -r requirements.txt
RUN python setup.py develop

WORKDIR /opt/netbox/netbox/
