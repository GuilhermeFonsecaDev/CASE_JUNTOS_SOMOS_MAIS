import dlt
from pyspark.sql.functions import col

@dlt.table(
  comment="Tabela Silver",
  table_properties={
    "quality": "silver"})

def transac_vendas_silver():
    # Lendo nossa tabela bronze ingerida pelo autoloader e tratando os nomes das colunas para que fiquem mais amigáveis de fácil entendimento
    tabela_bronze = spark.table("catalogo.database.transac_vendas_bronze").select(
      col('TransactionNo').alias('ID_TRANSACAO'),
      col('Date').alias('DATA_TRANSACAO'),
      col('ProductNo').alias('ID_PRODUTO'),
      col('ProductName').alias('NOME_PRODUTO'),
      col('Price').alias('PRECO_PRODUTO'),
      col('Quantity').alias('QUANTIDADE_COMPRA'),
      col('CustomerNo').alias('ID_CLIENTE'),
      col('Country').alias('PAIS'))
    
    # Filtrando dados nulos para limpeza da tabela, criando campo de VALOR_TOTAL e de DATA_PROCESSAMENTO
    tabela_silver = tabela_bronze.where(
        (col("ID_TRANSACAO").isNotNull()) &
        (col("DATA_TRANSACAO").isNotNull()) &
        (col("PRECO_PRODUTO") > 0) &
        (col("QUANTIDADE_COMPRA") > 0))\
        .withColumn("VALOR_TOTAL", col("PRECO_PRODUTO") * col("QUANTIDADE_COMPRA"))\
        .withColumn("DATA_PROCESSAMENTO", current_date())
        

    tabela_silver = tabela_silver.dropDuplicates(["ID_TRANSACAO"])

    return tabela_silver

# Definindo CONSTRAINTS para processo de QUALIDADE DE DADOS, impedindo que dados com problema não afetem a camada GOLD futuramente
@dlt.expect_or_fail("ID_TRANSACAO unico", "ID_TRANSACAO IS DISTINCT")
@dlt.expect_or_fail("Valores válidos para as colunas PRECO_PRODUTO e QUANTIDADE_COMPRA", "PRECO_PRODUTO > 0 AND QUANTIDADE_COMPRA > 0")
def data_quality_check():
    return dlt.read("transac_vendas_silver")


