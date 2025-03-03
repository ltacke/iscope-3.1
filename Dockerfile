FROM registry.access.redhat.com/ubi9/python-312 as builder

RUN pip install uv==0.4.24

WORKDIR /src

RUN python -m venv venv
RUN . /src/venv/bin/activate

ADD pyproject.toml ./

RUN uv sync

FROM registry.access.redhat.com/ubi9/python-312 as runtime

USER 1001

ENV VIRTUAL_ENV=/src/.venv \
    PATH="/src/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

ADD --chown=1001:0 src src

EXPOSE 4000

ENTRYPOINT ["python", "-m", "streamlit", "run", "src/main.py", "--server.port", "4000"]
