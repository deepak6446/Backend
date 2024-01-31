# Get Linux
FROM centos:7

# Install Java
RUN yum update -y \
&& yum install java-11-openjdk-devel -y \
&& yum clean all \
&& rm -rf /var/cache/yum

# Set JAVA_HOME environment var
ENV JAVA_HOME="/usr/lib/jvm/java-11-openjdk"

# Install Python
RUN yum install python3 -y \
&& pip3 install --upgrade pip setuptools wheel \
&& if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi \
&& if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi \
&& yum clean all \
&& rm -rf /var/cache/yum

# Download spark binary
RUN yum -y update && yum -y install wget
# RUN wget -c https://mirrors.estointernet.in/apache/spark/spark-3.1.1/spark-3.0.2-bin-hadoop3.2.tgz
RUN wget -c https://archive.apache.org/dist/spark/spark-3.0.2/spark-3.0.2-bin-hadoop3.2.tgz
RUN tar -xvzf spark-3.0.2-bin-hadoop3.2.tgz

# Set env variables
ENV SPARK_HOME="/spark-3.0.2-bin-hadoop3.2"
ENV PYTHONPATH="$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.9-src.zip:$PYTHONPATH"
ENV PYSPARK_PYTHON=python3
ENV PATH="$SPARK_HOME/bin:$SPARK_HOME/python:$PATH"

RUN yum -y install make
RUN mkdir /<repo>-spark-dashboard
RUN mkdir /spark-history

#Install zip
RUN yum -y install zip

# Copy history config
COPY ./spark-config/spark-defaults.conf /spark-3.0.2-bin-hadoop3.2/conf/spark-defaults.conf

CMD ["bash"]