FROM python:3.12-slim
LABEL authors="halone"
WORKDIR /app
ARG GIT_USERNAME
ARG GIT_PAT
COPY . .
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry config repositories.git-iu-datamodels "https://github.com/Halone228/iu_datamodels" &&  \
    poetry config http-basic.git-iu-datamodels ${GIT_USERNAME} ${GIT_PAT} &&  \
    apt-get update && apt-get install git -y && \
    poetry install
ENTRYPOINT ["poetry", "run", "dev"]