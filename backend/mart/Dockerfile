# Use an official Python runtime as a parent image
FROM python:3.12.5-slim AS base-build

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM base-build AS base-dev

# Install protobuf compiler Poetry
RUN apt-get update && apt-get install -y build-essential \
libpq-dev curl protobuf-compiler libprotobuf-dev  && \
rm -rf /var/lib/apt/lists/* && apt-get clean

# Add Poetry to PATH
ENV POETRY_VERSION=1.8.2

RUN pip install poetry==${POETRY_VERSION}
# Configuration to avoid creating virtual environments inside the Docker container
RUN touch README.md 
#&& poetry config virtualenvs.create false
WORKDIR $PYSETUP_PATH
# Install any needed packages specified in requirements.txt
COPY ./backend/mart/pyproject.toml ./backend/mart/poetry.lock ./
RUN poetry install --only main

FROM base-dev AS dev-build
# Copying poetry and venv into image
COPY --from=base-dev $POETRY_HOME $POETRY_HOME
COPY --from=base-dev $PYSETUP_PATH $PYSETUP_PATH


# Copying the rest of the application code
# Copying in our entrypoint
COPY conf/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# venv already has runtime deps installed we get a quicker install
WORKDIR $PYSETUP_PATH
RUN poetry install

WORKDIR /app
COPY ./backend/mart /app
EXPOSE 8000
ENTRYPOINT /entrypoint.sh $0 $@
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8000", "--reload"]

# 'test' stage runs our unit tests with pytest and
# coverage.  Build will fail if test coverage is under 95%
FROM dev-build AS test
RUN coverage run --rcfile ./pyproject.toml -m pytest ./backend/mart/tests
RUN coverage report --fail-under 95

# Generate Python classes from Protobuf definitions
#RUN protoc --python_out=. schemas.proto

# Start a new, final image
FROM base-build AS prod-build
# Install rsyslog in the final stage
RUN apt-get update && apt-get install -y rsyslog rsyslog-kafka  curl \
    protobuf-compiler libprotobuf-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

   
ENV FASTAPI_ENV=production

COPY --from=base-dev $VENV_PATH $VENV_PATH
COPY conf/gunicorn_conf.py /gunicorn_conf.py
    
   # Copy rsyslog configuration
COPY conf/rsyslog.conf /etc/rsyslog.conf

# Copy the entrypoint script
COPY conf/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

    
COPY ./backend/mart /app
WORKDIR /app

ENTRYPOINT /entrypoint.sh $0 $@
CMD [ "gunicorn", "--worker-class uvicorn.workers.UvicornWorker", "--config /gunicorn_conf.py", "app.main:app"]


