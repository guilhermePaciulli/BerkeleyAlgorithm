docker run -it -d --name slave1 python bash
docker run -it -d --name slave2 python bash
docker run -it -d --name slave3 python bash
docker run -it -d --name master python bash

docker exec -t slave1 bash -c 'git clone https://github.com/guilhermePaciulli/BerkeleyAlgorithm.git;cd BerkeleyAlgorithm;git pull;cd test;bash slave_1.sh'
docker exec -t slave2 bash -c 'git clone https://github.com/guilhermePaciulli/BerkeleyAlgorithm.git;cd BerkeleyAlgorithm;git pull;cd test;bash slave_2.sh'
docker exec -t slave3 bash -c 'git clone https://github.com/guilhermePaciulli/BerkeleyAlgorithm.git;cd BerkeleyAlgorithm;git pull;cd test;bash slave_3.sh'
docker exec -t master bash -c 'git clone https://github.com/guilhermePaciulli/BerkeleyAlgorithm.git;cd BerkeleyAlgorithm;git pull;cd test;bash master.sh'
