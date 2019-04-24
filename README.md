# Berkeley Algorithm

### Integrantes
* Guilherme Horcaio Paciulli - 41606574
* Ygor Lima - 41607589

## Documentação
* A execução do algoritmo começa no módulo main.py, ele recebe cada um dos parâmetros de execução e direciona para execução      como um master ou como um slave:
    - No caso do master: 
        1. ele lê os argumentos na seguinte ordem: endereço que o master escutará, tempo atual do master, tolerância de falha, arquivo com a relação de cada um dos escravos e arquivo para escrever os logs.
        2. o módulo passa esses argumentos para uma função que instancia um Server e automaticamente começa o processo executando o método run() da classe Server.
        3. Ao instanciar a classe Server, ele define como propriedades da instância o ip e a porta de escuta na qual os clients mandam seus tempos dividindo uma string por ':' do tipo ip.ip.ip:port e fazendo os devidos casts, depois já se cria o socket que escutará nessa porta e ip faz-se o bind necessário, depois define-se o tempo atual do master e depois a falha. Uma rotina com a assinatura ```def _read_slaves_file(self, file_name)``` abre o arquivo definido como a lista de slaves lê cada linha e para cada uma divide em ':' obtendo o ip e a porta e com isso cria uma instância da classe Slave que também contém o último tempo obtido daquele slave (que no primeiro momento é -1 pois ainda não foi definido) retornando uma lista de slaves que vira propriedade da classe. Por último a instância abre o arquivo de logs para facilitar.
        4. A função ```run()``` começa escutando o número de slaves da lista e por tempo indeterminado (a.k.a. ```while True:```) para cada slave ela roda uma rotina ```def _receive_time(self, slave):``` que requisita o tempo dele. Essa rotina abre um socket para se comunicar com o slave, tenta se conectar no ip e porta definidos na instância e manda uma mensagem ```"request_time"``` e depois recebe uma mensagem com o tempo do slave e retorna esse valor e fecha a conexão deste socket. Caso não consiga conectar, ele faz o log constando que o slave está down.
    - No caso do slave: 
        1. ele lê os argumentos na seguinte ordem: endereço que o slave ficará escutando, o tempo atual dele e um arquivo para escrever os logs.

## Teste
Detalhes do teste:

* O teste encontra-se na pasta /test

* Ambiente de teste:
    - Master:
      No endereço 127.0.0.1:8080 com tempo 185 e tolerância d 15 apontando para
      o arquivo slaves.txt com a lista dos slaves e com logs para
      logs/master_log.txt
    - Slaves:
      No endereço 127.0.0.1:9000 com tempo 175 e logs para logs/slave_log_1.txt
      No endereço 127.0.0.1:9001 com tempo 180 e logs para logs/slave_log_2.txt
      No endereço 127.0.0.1:9002 com tempo 205 e logs para logs/slave_log_3.txt

    - Resultados (considerando a execução simultânea dos 3 slaves e o
      funcionamento correto de cada um deles - nenhum deles down):
      Master 127.0.0.1:8080 com tempo 180
      Slave  127.0.0.1:9000 com tempo 180
      Slave  127.0.0.1:9001 com tempo 180
      Slave  127.0.0.1:9002 com tempo 205 (não mudou pois fugiu da falha)

* Arquivos:
    - Master: Bash correspondente: /test/master.sh, com as flags já
      configuradas
      ```python ../main.py -m 127.0.0.1:8080 185 15 ../slaves.txt logs/master_log.txt```

    - Slaves: No arquivo /slaves.txt temos uma relação dos 3 slaves com a porta
      e o ip de cada um. Para cada um dos 3 slaves foram criados scripts do
      tipo bash com as flags, são os três arquivos: slave_1.sh, slave_2.sh e
      slave_3.sh todos no diretório /test.
        1. ```python ../main.py -s 127.0.0.1:9000 175 logs/slave_log_1.txt```
        2. ```python ../main.py -s 127.0.0.1:9001 180 logs/slave_log_2.txt```
        3. ```python ../main.py -s 127.0.0.1:9002 205 logs/slave_log_3.txt```

* Atenção:
    - **os bash's não podem ser movidos pois usam execução relativa de suas
      pastas.**
    - **para exeução correta primeiro executar cada um dos slaves depois executar
      o master para todos os 3 atingirem o master ao mesmo tempo.**

* Os resultados com os prints de cada slave e do master deste teste
  encontram-se em /test/results.
