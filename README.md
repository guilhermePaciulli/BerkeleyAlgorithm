# Berkeley Algorithm

## Integrantes
* Guilherme Horcaio Paciulli - 41606574
* Ygor Lima - 41607589

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
