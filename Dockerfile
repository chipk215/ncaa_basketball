FROM jupyter/tensorflow-notebook:latest

RUN conda install -c conda-forge python-graphviz
RUN pip install anytree

