FROM odoo:18.0

USER root

# Install Python dependencies for connector-prestashop and OCA connector
RUN pip3 install --break-system-packages \
    html2text \
    prestapyt \
    bs4 \
    vcrpy \
    freezegun \
    cachetools

USER odoo
