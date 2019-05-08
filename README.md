# Berkeley Algorithm

### Integrantes
* Guilherme Horcaio Paciulli - 41606574
* Ane Caroline Gomes - 41627571

## Documentação
* A execução do algoritmo começa no módulo main.py, ele recebe cada um dos parâmetros de execução e direciona para execução      como um master ou como um slave:
    - No caso do master:
        1. ele lê os argumentos na seguinte ordem: endereço que o master escutará, tempo atual do master, tolerância de falha, arquivo com a relação de cada um dos escravos e arquivo para escrever os logs.
        2. o módulo passa esses argumentos para uma função que instancia um Server e automaticamente começa o processo executando o método run() da classe Server.
        3. Ao instanciar a classe Server, ele define como propriedades da instância o ip e a porta de escuta na qual os clients mandam seus tempos dividindo uma string por ':' do tipo ip.ip.ip:port e fazendo os devidos casts, depois já se cria o socket que escutará nessa porta e ip faz-se o bind necessário, depois define-se o tempo atual do master e depois a falha. Uma rotina com a assinatura ```def _read_slaves_file(self, file_name)``` abre o arquivo definido como a lista de slaves lê cada linha e para cada uma divide em ':' obtendo o ip e a porta e com isso cria uma instância da classe Slave que também contém o último tempo obtido daquele slave (que no primeiro momento é -1 pois ainda não foi definido) retornando uma lista de slaves que vira propriedade da classe. Por último a instância abre o arquivo de logs para facilitar.
        4. A função ```run()``` começa escutando o número de slaves da lista e por tempo indeterminado (a.k.a. ```while True:```) para cada slave ela roda uma rotina ```def _receive_time(self, slave):``` que requisita o tempo dele. Essa rotina abre um socket para se comunicar com o slave, tenta se conectar no ip e porta definidos na instância e manda uma mensagem ```"request_time"``` e depois recebe uma mensagem com o tempo do slave e retorna esse valor e fecha a conexão deste socket. Caso não consiga conectar, ele faz o log constando que o slave está down.
        5. Uma vez recebidos todos os tempos (possíveis) o master filtra o os slaves por aqueles que foram atingidos (tempo não é -1) e cujo delta seja menor que a tolerância d definida. Depois cria-se outra lista com os valores dos deltas (lembrando de se adicionar 0 que é a diferença entre o tempo do master e ele mesmo), por fim calcula-se a média.
        6. Se a a nova média obtida for diferente de zero, o master soma a média ao próprio tempo e para cada slave ele roda uma rotina para enviar a o novo tempo obtido. Essa rotina com a assinatura de ```def _send_time(self, slave, avg):``` abre um outro socket para se comunicar com o slave, tenta conectar com o slave e manda uma mensagem ```"update_time:"+str(time)``` contendo o novo tempo a ser atualizado. Caso dê errado o master faz o log que o slave está inatingível.
        7. Por último, antes da próxima iteração, o master espera 5 segundos para requisitar tudo novamente.
    - No caso do slave:
        1. ele lê os argumentos na seguinte ordem: endereço que o slave ficará escutando, o tempo atual dele e um arquivo para escrever os logs.
        2. o módulo passa esses argumentos para uma função que instancia um Client e automaticamente começa o processo executando o método run() da classe Client.
        3. Ao instanciar um client com esses argumentos, ele define como propriedades da instância o ip e a porta de escuta pela qual o master se comunicará com o slave dividindo uma string por ':' do tipo ip.ip.ip:port e fazendo os devidos casts, depois já se cria o socket que escutará nessa porta e ip faz-se o bind necessário, define-se o tempo atual do client e por último abre-se o arquivo de logs do client em questão.
        4. A rotina de run() é bem simples, ela primeiro começa escutar o socket que o master se conectará e começa por um tempo indeterminado um loop. Cada iteração desse loop espera pela conexão do master, quando atingida tenta decodificar a mensagem que ele envia.
        5. Se essa mensagem for ```"request_time"``` o slave apenas manda seu tempo e faz o log com essa informação e depois fecha a conexão.
        6. Senão deduz-se que essa mensagem seja de atualização de tempo. Para tal o slave faz o log do tempo antigo, pega a mensagem recebida, divide ela por ':' e pega o segundo valor (referente ao tempo do master) e define seu valor como este (fazendo-se os devidos casts). Depois faz o log com o novo tempo e fecha a conexão.
    - Notas:
        * Ambos têm um mecanismo de tanto fazer os logs no arquivo em questão quanto na tela do command prompt para tal implementou-se uma função nos dois que faz isso com o nome de ```def _log(self, log):```.

## Teste
Detalhes do teste:

* O teste encontra-se na pasta /test

* Ambiente de teste:
    - Master:
      No endereço 127.0.0.1:8080 com tempo 185 e tolerância d 15 apontando para
      o arquivo slaves.txt com a lista dos slaves e com logs para
      logs/master_log.txt
    - Slaves:
        - No endereço 127.0.0.1:9000 com tempo 175 e logs para logs/slave_log_1.txt
        - No endereço 127.0.0.1:9001 com tempo 180 e logs para logs/slave_log_2.txt
        - No endereço 127.0.0.1:9002 com tempo 205 e logs para logs/slave_log_3.txt

    - Resultados (considerando a execução simultânea dos 3 slaves e o
      funcionamento correto de cada um deles - nenhum deles down):
        - Master 127.0.0.1:8080 com tempo 180
        - Slave  127.0.0.1:9000 com tempo 180
        - Slave  127.0.0.1:9001 com tempo 180
        - Slave  127.0.0.1:9002 com tempo 205 (não mudou pois fugiu da falha)

### Teste local:
    - Bash exec.sh executa o processo inteiro, executando o exec.py.

    - O exec.py instancia quatro threads (os 3 slaves e o master) e espera indefinidamente a execução de todos. Esse arquivo utiliza para cada thread a flag Daemon para criar dependência das threads com a thread do exec.py.

    - No arquivo /test/slaves.txt temos uma relação dos 3 slaves com a porta e o ip de cada um

    - Os logs todos ficam na pasta /test/logs.

    - Os resultados com os prints de cada slave e do master deste teste encontram-se em /test/results.

### Teste em máquinas virtuais:
    - O start_docker.sh execeuta o processo inteiro, ele cria três containers docker com imagem python dentro, inicialza cada um dos três, para cada um ele clona esse projeto, entra na pasta e executa um bash correspondente com os argumentos corretos para cada um dos três slaves. O master é depois desses executado localmente.
    
    - Cada bash executa uma instância de um client ou de um master com os argumentos que criam o ambiente de teste acima.
    
    - Os containers expõem suas portas para habilitar a comunicação com o master.
    
    - Utilize o bash stop_docker.sh para parar todo o processo.
