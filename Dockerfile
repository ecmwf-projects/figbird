FROM continuumio/miniconda3

WORKDIR /src/figbird

COPY environment.yml /src/figbird/

RUN conda install -c conda-forge gcc python=3.10 \
    && conda env update -n base -f environment.yml

COPY . /src/figbird

RUN pip install --no-deps -e .
