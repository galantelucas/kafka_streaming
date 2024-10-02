# Kafka Streaming Project

Este projeto implementa um processamento de dados em tempo real utilizando **Apache Kafka**. Abaixo está uma visão geral da arquitetura e principais componentes.

Elaborado para disciplina de processamento de dados em streaming da Universidade de Fortaleza (UNIFOR), professor Nauber Goes.

## índice
* [Arquitetura do Projeto](#arquitetura-do-projeto)
* [Componentes Principais](#componentes-principais)
* [Redes e Volumes](#redes-e-volumes)
* [Fluxo de Dados](#fluxo-de-dados)
* [Interdependências](#interdependências)
* [Como Executar](#como-executar)
* [Funcionalidades Principais](#funcionalidades-principais)


## Arquitetura do Projeto
É baseado em uma solução de **streaming de dados** que utiliza contêineres Docker para integrar várias tecnologias, como Kafka, Zookeper, PostgreSQL, e Streamlit, coordenadas pelo Docker Compose. O projeto segue uma estrutura orientada a microsserviços, onde cada componente está isolado em um contêiner, garantindo modularidade e escalabilidade.

![Architecture](/images/architecture.png)
## Componentes Principais

### 1. Zookeeper
- Coordena o serviço do **Kafka**, gerenciando o estado dos brokers e facilitando a sincronização.
- Utiliza a porta padrão `2181` para comunicação.

### 2. Kafka
- Plataforma de mensagens distribuídas que envia e recebe eventos em tempo real.
- Recebe dados de um **Produtor** e disponibiliza para o **Consumidor** através do tópico `sales`.
- Depende do **Zookeeper** para gerenciar o cluster Kafka e garantir alta disponibilidade.

### 3. PostgreSQL
- Banco de dados relacional que armazena os dados consumidos do **Kafka**.
- Contém o banco de dados `sales_db`, que armazena os dados de vendas processados.
- O **Consumidor** envia os dados do **Kafka** para o **PostgreSQL**.

### 4. Produtor Kafka (Producer)
- Gera e envia dados de vendas em formato `.json` para o tópico `sales` no **Kafka**.
- Depende de um broker Kafka saudável para iniciar.

### 5. Consumidor Kafka (Consumer)
- Consome dados do tópico `sales` no **Kafka** e os insere no banco de dados **PostgreSQL**.
- Depende tanto do **Kafka** quanto do **PostgreSQL** para operar corretamente.

### 6. Streamlit
- Aplicação web interativa que exibe os dados armazenados no **PostgreSQL** em um dashboard.
- A interface é disponibilizada na porta `8501` e permite a visualização em tempo real dos dados de vendas processados.
- Possui atualização em tempo real a cada 5 segundos.

## Redes e Volumes

### Redes
- Todos os serviços estão conectados à rede Docker personalizada `app-network`, que facilita a comunicação entre os serviços sem expor todos os contêineres diretamente ao host. Isso melhora a segurança e a performance.

### Volumes
- Volumes Docker são usados para persistir dados dos serviços principais, como **Zookeeper**, **Kafka** e **PostgreSQL**. Eles garantem que os dados não sejam perdidos quando os contêineres são reiniciados ou recriados.

## Fluxo de Dados

1. O **Produtor** envia dados de vendas para o **Kafka**, que distribui esses dados pelo tópico `sales`.
2. O **Consumidor** consome esses dados do **Kafka** e os insere no banco de dados **PostgreSQL**.
3. A aplicação **Streamlit** se conecta ao **PostgreSQL** para exibir os dados de vendas em tempo real em uma interface gráfica acessível via navegador.

## Interdependências

- **Kafka** depende do **Zookeeper** para gerenciar seus brokers.
- O **Produtor** depende do **Kafka** para enviar dados.
- O **Consumidor** depende do **Kafka** e do **PostgreSQL** para processar e armazenar os dados.
- O **Streamlit** depende do **PostgreSQL** para acessar os dados e apresentá-los aos usuários.

## Como Executar
### Passo a Passo

 **Clone o Repositório**:
   ```bash
   git clone https://github.com/galantelucas/kafka_streaming.git
   cd kafka_streaming
   Docker composse up --build -d
   Verificar no localhost a aplicação http://localhost:8501/
   ```

O **Dashboard de Vendas** fornece uma visualização clara dos dados de vendas de um banco de dados PostgreSQL. Suas principais funcionalidades incluem:

## Funcionalidades Principais

1. **Conexão com o Banco de Dados**:
   - Busca dados de vendas, como ID, produto, valor, localização e data.

2. **Visualização Georreferenciada**:
   - Exibe um mapa interativo mostrando onde as vendas ocorrem, facilitando a identificação de padrões geográficos.

3. **Resumo de Vendas**:
   - Apresenta métricas chave, como total de vendas e número de transações, em cards.

4. **Tabela de Vendas por Produto**:
   - Mostra detalhes de cada transação, permitindo análise granular.

5. **Distribuição de Vendas por Produto**:
   - Um gráfico de rosca ilustra a participação de cada produto nas vendas totais.

6. **Vendas ao Longo do Tempo**:
   - Um gráfico de linha mostra tendências de vendas mensais, ajudando a identificar sazonalidades.

## Benefícios

O dashboard facilita a tomada de decisões informadas, permitindo análises de desempenho e oportunidades de melhoria nas vendas.
O incremento de visualizações e organizações poderá ser muito bem explorado pelo stakeholder.

---

![4](https://github.com/user-attachments/assets/a765f7ee-edd5-474d-b91e-2564f720ce16)
![1](https://github.com/user-attachments/assets/4a85a56a-0d37-4fde-a3e0-7781320d75cc)
![2](https://github.com/user-attachments/assets/28e4ddb1-bebd-460d-946d-8da4f1411435)
![3](https://github.com/user-attachments/assets/33a33465-23a5-47c2-92b0-4f9b09a3e890)






