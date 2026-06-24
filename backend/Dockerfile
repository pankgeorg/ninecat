# FastAPI backend (ninecat-py). The pinned scientific stack predates arm64
# wheels, so numpy/pandas/psycopg2 are compiled from source: install a toolchain
# + BLAS/LAPACK, pin a build-isolation-free pip/setuptools/Cython, build numpy
# first, then resolve the rest with the legacy resolver (the frozen pins are
# internally inconsistent under the 2020+ resolver). default-jdk is for tabula-py.
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

ENV PIP_PREFER_BINARY=1 \
    SETUPTOOLS_USE_DISTUTILS=stdlib

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential gfortran pkg-config python3-dev \
        libopenblas-dev liblapack-dev libfreetype6-dev libpng-dev libpq-dev \
        default-jdk \
    && rm -rf /var/lib/apt/lists/*

RUN pip install "pip==22.3.1" "setuptools==59.8.0" "wheel==0.37.1" "Cython==0.29.36"

COPY requirements.txt /tmp/
RUN pip install --no-build-isolation "numpy==1.18.4"
RUN pip install --no-build-isolation --use-deprecated=legacy-resolver \
        --requirement /tmp/requirements.txt

COPY ./app /app/app
