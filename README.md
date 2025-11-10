# Buscador de ofertas pelando

O intuito desse script é pesquisar por ofertas no Pelando e notificarmos via Bot no Telegram.

## Instruções
Crie um arquivo .env e adicione três informações:
- token=INSIRA_TOKEN
- chat_id=INSIRA_CHAT_ID
- itens_file=INSIRA_NOME_DO_ARQUIVO_COM_OS_ITENS_MONITORADOS.txt

### Como obter o token e chat.id
- No telegram, chame o @BotFather e crie seu bot, ao final do processo, copie o token que ele fornecer e salve no arquivo **.env**
- Após a criação do Bot, converse com ele e abra a página: https://api.telegram.org/botSEUTOKEN/getUpdates, você precisa do chat.id que aparece conforme o print abaixo. Salve no arquivo **.env** também
![chat.id](image.png)

### Configuração

Caso queira modificar o formato da mensagem, dentro do arquivo pesquisa.py, procure pela função *async def processar_encontrados(encontrados):* e edite a variável **mensagem**, lembrando que ela está formatada em HTML, então, use o formato HTML para modificar da forma que preferir.

Há também uma lista chamada *produtos_monitorados*, nela você pode adicionar os itens que deseja monitorar. Lembrando que a busca será rigorosa, se você colocar Smart TV 50 e a oferta postada no site for de TV 50, ele não localizará, portanto, é recomendável evitar acrescentar termos que podem provocar que o produto não seja encontrado.

Antes de rodar o script, rode o comando `pip install -r requirements.txt` para instalar as bibliotecas necessárias para rodar o script.

PS.: A busca não é case sensitive, pois tanto na lista dos produtos monitorados como na lista das ofertas do site é usada a função **.lower()** para transformar tudo em mínuscula na hora de comparar os termos.

## Alertas
Caso queira que o script rode "eternamente", você pode fazer isso via **Agendador de Tarefas** (Windows) ou **cron** (Linux/macOS)

### Agendador de Tarefas
- Abra o Agendador de tarefas (Task Scheduler)
- Criar tarefa
- Na aba gatilho (Triggers) clique em Novo, Escolha o periodo (diariamente por exemplo) e configure o intervalo, como Repetir a cada 15 minutos e por 1 dia por exemplo.
- Na aba ações, clique em Nova, escolha Iniciar um programa e em programa/script coloque o caminho do python, ex.:
    - C:\Users\SeuUsuario\AppData\Local\Programs\Python\Python39\python.exe
- Em adicionar argumentos, coloque o caminho do script, exemplo:
    - "C:\caminho\para\pesquisa.py"

OBS.: Você pode substituir o executável *python.exe* por *pythonw.exe* caso não queira que suba a janela do prompt enquanto o script estiver rodando, ou seja, vai rodar silenciosamente sem que você perceba a ação.

### cron
- Abra o editor do crontab usando o comando `crontab -e`
- Caso queira rodá-lo a cada 15 minutos, acrescente:
```bash
*/15 * * * * /usr/bin/python3 /caminho/para/pesquisa.py
```

**Exemplos de frequência**:
<table border=2>
  <tr>
    <th>Frequência</th>
    <th>Linha do crontab</th>
  </tr>
  <tr>
    <td>A cada 15 minutos</td>
    <td>*/15 * * * * /usr/bin/python3 /caminho/para/pesquisa.py</td>
  </tr>
  <tr>    
    <td>A cada 30 minutos</td>
    <td>*/30 * * * * /usr/bin/python3 /caminho/para/pesquisa.py</td>
  </tr>
  <tr>
    <td>A cada 60 minutos</td>
    <td>*/60 * * * * /usr/bin/python3 /caminho/para/pesquisa.py</td>
  </tr>
</table>

Certifique-se que o cron esteja ativo rodando `sudo service cron status`, caso não esteja, rode `sudo service cron start`

É possível também criar loop dentro do próprio script para rodar o arquivo indefinidamente, porém, não recomendo. Caso opte por seguir dessa forma, envolve todo o código do arquivo pesquisa.py dentro de uma função e no final do arquivo, adicione o código abaixo

```python
import time

while True:
    # Chama sua função principal aqui
    executar_scraper() #coloque o nome que você deu para a função que envolve todo o código

    # Aguarda 15 minutos
    time.sleep(15 * 60)
```

## TO-DO
- [x] Configurar notificações no desktop em caso de ofertas localizadas (além de receber via Telegram).