# Kafka Streaming Project

Este projeto implementa um pipeline de dados em tempo real utilizando Apache Kafka. Abaixo está uma visão geral das principais componentes e funcionalidades do projeto.

## Estrutura do Projeto

### 1. Configuração do Kafka
- Configuração necessária para iniciar e gerenciar um cluster Kafka.
- Definição de tópicos, produtores e consumidores.
### 2. Produção de Dados
- Scripts ou aplicações que geram dados e os enviam para os tópicos Kafka.
- Fontes de dados podem incluir logs de aplicativos, transações financeiras, etc.
### 3. Processamento de Dados
- Utilização da Kafka Streams API para processar dados em tempo real.
- Operações incluem filtragem, agregação e transformação dos dados.
### 4. Armazenamento de Dados
- Dados processados são armazenados em um banco de dados ou enviados para outro sistema para análise posterior, utilizamos Postgres SQL para armazenamento.
### 5. Monitoramento e Logs
- Ferramentas para monitorar o fluxo de dados e registrar eventos importantes.
- Garantia de funcionamento correto do sistema e facilitação da detecção de problemas.
## Como Executar
## Passo a Passo

 **Clone o Repositório**:
   ```bash
   git clone https://github.com/galantelucas/kafka_streaming.git
   cd kafka_streaming
   Docker composse up -d
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

![image](![Dashboard de Vendas em Streaming](image.png))


