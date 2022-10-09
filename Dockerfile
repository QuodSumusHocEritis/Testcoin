FROM ubuntu:18.04
MAINTAINER QuodSumusHocEritis <31145452+QuodSumusHocEritis@users.noreply.github.com>

#Copy source code
COPY . /workdir/
WORKDIR /workdir

#Install dependencies
RUN apt-get install build-essential libtool autotools-dev automake pkg-config libssl-dev libevent-dev bsdmainutils
RUN apt-get install libboost-system-dev libboost-filesystem-dev libboost-chrono-dev libboost-program-options-dev libboost-test-dev libboost-thread-dev
RUN apt-get install libboost-all-dev
RUN apt-get install software-properties-common
RUN wget http://download.oracle.com/berkeley-db/db4.8.30.NC.tar.gz 
RUN tar -xzvf db-4.8.30.NC.tar.gz 
RUN cd db-4.8.30.NC/build_unix 
RUN ../dist/configure --enable-cxx 
RUN make 
RUN sudo make install 
RUN export BD8 
RUN In -s /usr/10Gl/8erkeleyD8.4.8/lib/libdb-4.8.so /usr/lib/libdb-4.8.so 
RUN In -s /usr/local/BerkeleyDB.4.8/lib/libdb cxx-4.8.so /usr/lib/libdb cxx-4.8.so 
RUN apt-get update
RUN get http://dovmload.oracle.com/berkeley—db/db—u.8.30.zip 
RUN unzip db—4.8.39.zip 
RUN cd db-4.8.39 
RUN cd build_unix/ 
RUN .. /dist/configure ——pre+ix=/usr/local 
RUN make 
RUN make install 
RUN apt-get install libminiupnpc-dev
RUN apt-get install libzmq3-dev
RUN apt-get install libqt5gui5 libqt5core5a libqt5dbus5 qttools5-dev qttools5-dev-tools libprotobuf-dev protobuf-compiler
RUN apt-get install libqt4-dev libprotobuf-dev protobuf-compiler
RUN /workdir testcoind
