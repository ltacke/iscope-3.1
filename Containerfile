FROM registry.access.redhat.com/ubi9/python-312 as builder

RUN pip install uv==0.4.24

# ENV POETRY_NO_INTERACTION=1 \
#     POETRY_VIRTUALENVS_IN_PROJECT=1 \
#     POETRY_VIRTUALENVS_CREATE=1

WORKDIR /src

RUN python -m venv venv
RUN . /src/venv/bin/activate

ADD pyproject.toml uv.lock ./

RUN uv sync

FROM registry.access.redhat.com/ubi9/python-312 as runtime

USER 1001

ENV VIRTUAL_ENV=/src/.venv \
    PATH="/src/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

ADD --chown=1001:0 src src
# ADD --chown=1001:0 frontend frontend
# ADD --chown=1001:0 .streamlit .streamlit

EXPOSE 4000

ENTRYPOINT ["python", "-m", "streamlit", "run", "src/frontend/main.py", "--server.port", "4000"]
