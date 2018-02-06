FROM alpine:latest
MAINTAINER Joshua Haertel <joshua.haertel@gmail.com>

RUN apk add --update \
        curl \
        ca-certificates \
        bash \
        git \
        openssl-dev \
        readline-dev \
        bzip2-dev \
        sqlite-dev \
        ncurses-dev \
        linux-headers \
        build-base && \
        curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash && \
        touch .bashrc && \
        echo 'export PATH="/root/.pyenv/bin:$PATH"' >> .bashrc && \
        echo 'eval "$(pyenv init -)"' >> .bashrc && \
        echo 'eval "$(pyenv virtualenv-init -)"' >> .bashrc && \
        . ./.bashrc && \
        for rev in '3.6.4' '3.5.4' '3.4.7' '2.7.14'; \
        do \
            pyenv install $rev & \
        done

CMD bash
