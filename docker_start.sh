docker run -it -d -p 127.0.0.1:9000:9000/tcp --name slave1 python bash
# docker run -it -d -p 127.0.0.1:9001:9001/tcp --name slave2 python bash
# docker run -it -d -p 127.0.0.1:9002:9002/tcp --name slave3 python bash

docker exec -t -d slave1 bash -c 'git clone https://github.com/guilhermePaciulli/BerkeleyAlgorithm.git;cd BerkeleyAlgorithm;git pull;cd test;bash slave_1.sh'
sleep 1
# docker exec -t -d slave2 bash -c 'git clone https://github.com/guilhermePaciulli/BerkeleyAlgorithm.git;cd BerkeleyAlgorithm;git pull;cd test;bash slave_2.sh'
# sleep 1
# docker exec -t -d slave3 bash -c 'git clone https://github.com/guilhermePaciulli/BerkeleyAlgorithm.git;cd BerkeleyAlgorithm;git pull;cd test;bash slave_3.sh'
# sleep 1

# bash test/master.sh
