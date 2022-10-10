FROM continuumio/miniconda3

WORKDIR /src/bluejay

COPY environment.yml /src/bluejay/

RUN conda install -c conda-forge gcc python=3.10 \
    && conda env update -n base -f environment.yml

COPY . /src/bluejay

RUN pip install --no-deps -e .
