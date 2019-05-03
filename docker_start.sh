docker run -it -d --name slave1 python bash
docker run -it -d --name slave2 python bash
docker run -it -d --name slave3 python bash

docker exec -t slave1 bash -c 'git clone https://github.com/guilhermePaciulli/BerkeleyAlgorithm.git;cd BerkeleyAlgorithm;git pull;cd test;bash slave_1.sh'
sleep 1
docker exec -t slave2 bash -c 'git clone https://github.com/guilhermePaciulli/BerkeleyAlgorithm.git;cd BerkeleyAlgorithm;git pull;cd test;bash slave_2.sh'
sleep 1
docker exec -t slave3 bash -c 'git clone https://github.com/guilhermePaciulli/BerkeleyAlgorithm.git;cd BerkeleyAlgorithm;git pull;cd test;bash slave_3.sh'
sleep 1
bash test/master.sh
