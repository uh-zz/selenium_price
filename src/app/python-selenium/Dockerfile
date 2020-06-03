FROM python:3

ARG project_dir=/root/src/app/

WORKDIR $project_dir

RUN set -x && \
  apt-get update && \
  pip install selenium　&& \
  pip install flask

CMD [ "python", "run.py" ]