# Case Juntos Somos Mais 

" O objetivo desse case é criar um desenho de solução, com passo a passo para orientar um engenheiro de dados desenvolver uma solução de dados real time para a squad de pedidos. O resultado desse desenho deverá orientar as pessoas de dados e da squad com a solução. Esses documentos servirão como insumo para iniciar o desenvolvimento.

A squad de produtos hoje conta com um(a) PM e pessoas de engenharia de software. Esse time fará parte da solução, criando o transacional da nossa solução de dados, portanto é necessário desenharmos a solução que contemple eles. Aqui é necessário sugerir uma arquitetura e ferramentas para a Squad, contextualizando tecnicamente e funcionalmente o time. A stack do lado de dados conta com um Databricks na Azure, mas ainda não tem uma solução para dados real time.
Os dados que receberemos estão nesse modelo (https://www.kaggle.com/datasets/gabrielramos87/an-online-shop-business)

É necessário também desenvolver um trecho de código para servir de exemplo para os engenheiros de software e de dados. Aqui, deixamos a sua escolha qual parte do código deseja construir para servir de exemplo. Podemos utilizar, Python, Pyspark, Sql e/ou Scala. Precisamos também explicar os motivadores para a escolha de tecnologia."

# ARQUITETURA SUGERIDA

![image](https://github.com/user-attachments/assets/62a1b30a-6bf9-47f6-bdd1-03a66b84f371)

# ESCOLHA DAS FERRAMENTAS 

- EVENT HUBS
Escolhi o EVENT HUBS para ingestão de dados por ser um serviço de mensageria nativo da Azure, plataforma em que estamos trabalhando, ele cumpre bem a missão para a ingestão em um alto fluxo de dados e também é facilmente integrado com o Databricks e com outros serviçoes da Microsfot.

- BLOB STORAGE (OPCIONAL)
O Blob Storage foi adicionado como uma opção para armazenar os dados, caso seja necessário backup ou reprocessamento dos eventos vindos do Event Hubs. Essa decisão depende da necessidade de latência do projeto. 

- DATABRICKS AUTOLOADER
Terá a missão de ingerir os dados em nossa tabela bronze, vindo diretamente do Event HUBS ou consumindo os arquivos parquet disponíveis no Blob Storage, o autoloader é capaz de ingerir volumes de dados gigantescos de uma vez só, sua escalabilidade é feita do forma automática com base no volume de dados.

 - DELTA LAKE E DELTA LIVE TABLES
O Delta Lake será responsável por armazenar os nossos dados, utilizando as propriedades ACID, teremos mais consistência e confiabilidade aos armazenar os dados. Em nosso projeto, as Delta Live tables serão responsáveis por fazer toda a parte de processamento de dados do nosso projeto, desde a ingestão (via autoloader), orquestração da pipeline, transformação dos dados entre as camadas (Bronze, Silver, Gold), até a aplicação de processos de qualidade de dados.

- ARQUITETURA MEDALHÃO
Escolhi esse modelo de arquitetura por ser recomendada pela própria Databricks ao trabalhar com o Delta Lake. Essa arquitetura permite organizar o pipeline de forma clara e eficiente, separando as camadas de dados (Bronze, Silver, Gold) de acordo com seus propósitos. Isso facilita o refinamento e transformação dos dados em cada etapa.
