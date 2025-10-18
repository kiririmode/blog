FROM mcr.microsoft.com/devcontainers/javascript-node:24-bullseye

ENV BLOGSYNC_VERSION v0.20.1
ENV HADOLINT_VERSION v2.12.0

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt-get update \
    # Install shellcheck
    && apt-get install -y shellcheck \
    # Install hadolint
    && curl -SL "https://github.com/hadolint/hadolint/releases/download/${HADOLINT_VERSION}/hadolint-Linux-arm64" -o /usr/local/bin/hadolint \
    && chmod +x /usr/local/bin/hadolint \
    # Install blogsync
    && curl -SL "https://github.com/x-motemen/blogsync/releases/download/${BLOGSYNC_VERSION}/blogsync_${BLOGSYNC_VERSION}_linux_arm64.tar.gz" | tar -xzC /tmp/ \
    && mv /tmp/blogsync_${BLOGSYNC_VERSION}_linux_arm64/blogsync /usr/local/bin/ \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*
