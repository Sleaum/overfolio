FROM debian:12.11

# Variables d'environnement
#ENV PYTHON_VERSION=3.12.1

# Mise à jour des paquets système
RUN apt-get update && apt-get install -y \
    wget \
    build-essential \
    libssl-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    zlib1g-dev \
    curl \
    git \
    libffi-dev \
    libncursesw5-dev \
    libgdbm-dev \
    libnss3-dev \
    liblzma-dev \
    tk-dev \
    xz-utils \
    ca-certificates \
    tree \
    python3-venv \
    python3 \
    python3-pip \
    && apt-get clean
    #&& rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python

## Installer Python 3.13.3 depuis les sources
#WORKDIR /usr/src
#RUN wget https://www.python.org/ftp/python/3.12.1/Python-3.12.1.tgz && \
#    tar xvf Python-3.12.1.tgz && \
#    cd Python-3.12.1 && \
#    ./configure --enable-optimizations && \
#    make -j$(nproc) && \
#    make altinstall && \
#    ln -s /usr/local/bin/python3.12 /usr/local/bin/python && \
#    ln -s /usr/local/bin/pip3.12 /usr/local/bin/pip

# Créer un dossier pour le code
WORKDIR /app

# Copier les fichiers
COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

# Copier le code Django (à adapter selon ta structure)
COPY ./app /app

# Port par défaut de Django
#EXPOSE 8000

# Commande par défaut : lancer le serveur
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

