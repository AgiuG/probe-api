FROM python:3.12.8-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git

RUN pip install pipx && \
    pipx install poetry==2.1.3

ENV PATH="/root/.local/bin:${PATH}"
    
RUN poetry config virtualenvs.create true

COPY ./pyproject.toml .

COPY ./main.py .

COPY ./src /app/src

RUN poetry install --no-interaction --no-ansi --no-root

EXPOSE 8000

WORKDIR /app

CMD ["poetry", "run", "python", "main.py"]