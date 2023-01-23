# Dockerfile to launch the python app
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install poetry
RUN poetry install
CMD ["poetry", "run", "discordpibot"]