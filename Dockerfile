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
RUN curl -fLo /tmp/wkhtmltox.deb https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.bionic_amd64.deb \
 && dpkg -i /tmp/wkhtmltox.deb \
 && rm -f /tmp/wkhtmltox.deb
# Ubuntu 18.04's tzdata predates British Columbia's move to permanent UTC-7
# (tzdata 2026b), so compile current North American rules from IANA.  Leave
# TZDATA_VERSION empty to keep the distribution's rules.
ARG TZDATA_VERSION=2026e
RUN if [ -n "$TZDATA_VERSION" ]; then \
      mkdir /tmp/tzdata \
   && curl -fsSL "https://data.iana.org/time-zones/releases/tzdata$TZDATA_VERSION.tar.gz" | tar xz -C /tmp/tzdata \
   && zic -d /usr/share/zoneinfo /tmp/tzdata/northamerica \
   && rm -rf /tmp/tzdata; \
    fi
ENV TZ=America/Vancouver
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN touch $HOME/.disableXTidedisclaimer
COPY / /current-atlas-tables
WORKDIR /current-atlas-tables
