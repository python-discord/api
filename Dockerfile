FROM python:3.9.2-buster as builder

ENV PIP_NO_CACHE_DIR=false \
    PIPENV_HIDE_EMOJIS=1 \
    PIPENV_NOSPIN=1

WORKDIR /builder

COPY "Pipfile*" ./

# Build uvicorn with uvloop and other packages
# that require gcc to compile. We'll copy them
# over to a slim container later.
# In addition, we specify the uvicorn dependency
# here to prevent a `pipenv lock` on Windows from
# stopping us from using `uvloop`.
RUN pip install -U pipenv==2020.11.15 \
 && pipenv install --system --deploy \
 && pip install uvicorn[standard]~=0.13.4

FROM python:3.9.2-slim-buster

STOPSIGNAL SIGQUIT

RUN groupadd -g 61000 api \
 && useradd -g 61000 -l -r -u 61000 api

# Copy over the built dependencies and
# script_entrypoint for uvicorn.
COPY --from=builder /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn

WORKDIR /app

COPY . .

# Switch over to an unprivileged user.
USER api

ENV commit_sha="development"
ENTRYPOINT ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
