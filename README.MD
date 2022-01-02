# DGB Project 

Rest API to deliver predictive data.

## Preparando o Ambiente
Requerimentos:
- Python 3.8  

Sera necessário a criação de um ambiente virtual python:
```bash
pip install virtualenv 
virtualenv dgvenv
```

As dependecias necessárias podem ser instalar usando o comando: 
```bash
pip install -r requirements
```

As dependencias que devem ser instaladas com o comando são:
- flask 
- pandas 
- firebase-admin 
- google-cloud-firestore 
- google-api-python-client 
- google-cloud-storage 
- pytest

## Uso

A solução consiste de 2 partes principais:
- Script de pre-processamento;
```
O SCRIPT de pre-processamento faz a integração com a solução cloud GOOGLE STORAGE
da onde baixa os arquivos de dados guardados como blob. Os dados são processados
para a criação de um novo dataframe com as informações de PREDICTED_AUDIENCE.
O resultado é então enviado a um banco de dados não-relacional(NoSQL) da solução 
FIRESTORE.
```
- Flask REST API: 
```
A REST API é organizada em 3 instancias: main controller e services;
Em main são definidas as rotas de acesso ao servidor web;
Em controller os dados são solicitados para o banco de dados e quando retornados
preparados para liberação da mensagem json final;
Em services é definida a conexão com o banco de dados GOOGLE FIRESTORE e feita
as queries necessárias para o retorno dos endpoints;
```

O banco de dados foi organizado com as seguintes coleções:
- PREDICTED_AUDIENCE
- PROGRAM_AUDIENCE
- INVENTORY_AVAILABILATY
- MIGRATION_HISTORY

```
As coleções Program_Audience e Inventory_availability trazem os dados de entrada
extraidos do cloud storage. A coleção program_audience traz os novos dados resultantes
do pre-processamento. A coleção migration_history traz os dados referentes aos 
arquivos de entrada processados e o timestamp de sua criação, de maneira a ter sempre
um controle dos dados que estão sendo migrados para o ambiente, ou que devem ser removidos.
```

Para inicializar o ambiente use o comando:
```bash
./env
```
O script deve :
- Inicializar o ambiente virtual python criado;
- Exportar as variaveis de ambiente necessárias;
- Inicializar a REST API localmente em modo produção;

Obs: Para essa solução as chaves de acesso a ambos os repositorios cloud 
utilizados foram guardadas na pasta ```/keys```. Essa não seria a pratica correta
e que oferece uma boa segurança para o ambiente, no entando, ela foi utilizada para 
facilitar a inicialização e funcionamento em um ambiente desconhecido;

## Testes
A solução acompanha um set de testes para verificação:

```bash
./test-env.sh

```
Quando executado o script é esparado que os seguintes testes apresentem resultados:
- test_index_page                                                      
- test_dataPrg_UNIT                                                    
- test_dataPrd_UNIT                                                    
- test_dataPrg                                                         
- test_NO_DATA_FOUND                                                   
- test_INVALID_DATE_FORMAT                                             
- test_VERY_LARGE_RANGE                                                
- test_NO_RANGE

## 
