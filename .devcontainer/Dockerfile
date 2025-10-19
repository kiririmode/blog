FROM mcr.microsoft.com/devcontainers/javascript-node:24-bullseye

ENV BLOGSYNC_VERSION v0.20.1
ENV HADOLINT_VERSION v2.12.0

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt-get update \
    # Install shellcheck
    && apt-get install -y shellcheck \
    # Install Chromium and its dependencies for Puppeteer
    && apt-get install -y \
        chromium \
        ca-certificates \
        fonts-liberation \
        libappindicator3-1 \
        libasound2 \
        libatk-bridge2.0-0 \
        libatk1.0-0 \
        libc6 \
        libcairo2 \
        libcups2 \
        libdbus-1-3 \
        libexpat1 \
        libfontconfig1 \
        libgbm1 \
        libgcc1 \
        libglib2.0-0 \
        libgtk-3-0 \
        libnspr4 \
        libnss3 \
        libpango-1.0-0 \
        libpangocairo-1.0-0 \
        libstdc++6 \
        libx11-6 \
        libx11-xcb1 \
        libxcb1 \
        libxcomposite1 \
        libxcursor1 \
        libxdamage1 \
        libxext6 \
        libxfixes3 \
        libxi6 \
        libxrandr2 \
        libxrender1 \
        libxss1 \
        libxtst6 \
        lsb-release \
        wget \
        xdg-utils \
    # Install hadolint
    && curl -SL "https://github.com/hadolint/hadolint/releases/download/${HADOLINT_VERSION}/hadolint-Linux-arm64" -o /usr/local/bin/hadolint \
    && chmod +x /usr/local/bin/hadolint \
    # Install blogsync
    && curl -SL "https://github.com/x-motemen/blogsync/releases/download/${BLOGSYNC_VERSION}/blogsync_${BLOGSYNC_VERSION}_linux_arm64.tar.gz" | tar -xzC /tmp/ \
    && mv /tmp/blogsync_${BLOGSYNC_VERSION}_linux_arm64/blogsync /usr/local/bin/ \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*
