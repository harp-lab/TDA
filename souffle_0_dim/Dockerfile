FROM ubuntu:20.04

# Update package lists and install necessary packages
RUN apt-get update && \
    apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Download and add the Souffle repository key
RUN wget -q https://souffle-lang.github.io/ppa/souffle-key.public -O /usr/share/keyrings/souffle-archive-keyring.gpg

# Add the Souffle repository to the sources list
RUN echo "deb [signed-by=/usr/share/keyrings/souffle-archive-keyring.gpg] https://souffle-lang.github.io/ppa/ubuntu/ stable main" | tee /etc/apt/sources.list.d/souffle.list

# Update package lists again and install Souffle
RUN apt-get update && \
    apt-get install -y \
    souffle

# Set entrypoint to bash
CMD ["/bin/bash"]
