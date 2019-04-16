# Copyright (c) 2009-2019 Emanuel Borsboom.  See COPYING.txt for license.
FROM ubuntu:18.04
RUN sed -i.bak 's/ main$/ main contrib non-free/' /etc/apt/sources.list
RUN apt-get update \
 && apt-get install -y \
    curl \
    fontconfig \
    libjpeg-turbo8 \
    libxrender1 \
    python \
    tzdata \
    xfonts-75dpi \
    xtide \
    xtide-data-nonfree \
 && rm -rf /var/lib/apt/lists/*
RUN curl -Lo /tmp/wkhtmltox.deb https://downloads.wkhtmltopdf.org/0.12/0.12.5/wkhtmltox_0.12.5-1.bionic_amd64.deb \
 && dpkg -i /tmp/wkhtmltox.deb \
 && rm -f /tmp/wkhtmltox.deb
ENV TZ=America/Vancouver
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN touch $HOME/.disableXTidedisclaimer
COPY / /current-atlas-tables
WORKDIR /current-atlas-tables
