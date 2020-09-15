# Base Images
FROM registry.cn-shanghai.aliyuncs.com/tcc-public/pytorch:1.4-cuda10.1-py3

CMD ["bash", "mkdir -p media_ai"]

ADD . /media_ai

WORKDIR /media_ai

#confg environment
RUN apt-get update
RUN apt-get install libgl1-mesa-dev
RUN apt-get install libglib2.0-dev
RUN pip install packages/certifi-2020.6.20-py2.py3-none-any.whl
RUN pip install wget
RUN python3 -m pip install paddlepaddle-gpu==1.8.4.post107 -i https://mirror.baidu.com/pypi/simple
RUN pip install packages/h5py-2.10.0-cp37-cp37m-manylinux1_x86_64.whl

RUN pip install packages/joblib-0.16.0-py3-none-any.whl
RUN pip install packages/threadpoolctl-2.1.0-py3-none-any.whl
RUN pip install packages/scipy-1.5.2-cp37-cp37m-manylinux1_x86_64.whl
RUN pip install packages/scikit_learn-0.23.2-cp37-cp37m-manylinux1_x86_64.whl
RUN pip install packages/terminaltables-3.1.0.tar.gz
RUN pip install packages/python_dateutil-2.8.1-py2.py3-none-any.whl
RUN pip install packages/pandas-1.1.0-cp37-cp37m-manylinux1_x86_64.whl
RUN pip install packages/ruamel.yaml.clib-0.2.0-cp37-cp37m-manylinux1_x86_64.whl
RUN pip install packages/ruamel.yaml-0.16.10-py2.py3-none-any.whl

# install zip
RUN dpkg -i packages/zip_3.0-8_amd64.deb


# CMD ["sh", "run.sh"]
