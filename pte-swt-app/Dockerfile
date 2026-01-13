# -------- Base Image (GPU + Python) --------
FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

# -------- System Setup --------
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-venv \
    python3-pip \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3.10 /usr/bin/python

# -------- Python Setup --------
WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# -------- App Code --------
COPY api /app/api
COPY app /app/app
COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

# -------- Ports --------
EXPOSE 8080

# -------- Start --------
ENTRYPOINT ["/app/entrypoint.sh"]
