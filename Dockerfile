# Dockerfile to launch the python app
FROM python:3.9
WORKDIR /app

# copy only the files needed to install dependencies
RUN pip install poetry
COPY poetry.lock pyproject.toml poetry.toml /app/
RUN poetry install

# copy the rest of the files
COPY . /app

CMD ["poetry", "run", "discordpibot"]