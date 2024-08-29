FROM mysql:8.0.39

ARG BASE_DIRECTORY

COPY ${BASE_DIRECTORY}/mysql/scripts /docker-entrypoint-initdb.d/

CMD ["mysqld"]
