FROM ubuntu:latest

ENV PYTHONUNBUFFERED=1

ARG APP_HOME=/usr/share/app/
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

ARG USERNAME=node
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    python3-pip \
    curl

RUN apt-get install -y --no-install-recommends \
    poppler-utils \
    libfile-mimeinfo-perl \
    libimage-exiftool-perl \
    ghostscript \
    libsecret-1-0 \
    zlib1g-dev \
    libjpeg-dev \
    imagemagick \
    libmagic1 \
    webp

RUN apt-get install -y --no-install-recommends\
    libreoffice \
    inkscape \
    ffmpeg \
    xvfb

ARG DRAWIO_VERSION=15.7.3
RUN curl -LO https://github.com/jgraph/drawio-desktop/releases/download/v${DRAWIO_VERSION}/drawio-x86_64-${DRAWIO_VERSION}.AppImage && \
    mv drawio-x86_64-${DRAWIO_VERSION}.AppImage /usr/local/bin/drawio && \
    chmod +x /usr/local/bin/drawio

USER $USERNAME

COPY app app/
COPY wsgi.py .
COPY requirements.txt .

ENV PATH=/home/${USERNAME}/.local/bin:$PATH
RUN pip install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
