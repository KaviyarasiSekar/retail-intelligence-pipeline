from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, lit


REPO_ROOT = Path(__file__).resolve().parents[2]

LANDING_BASE_PATH = REPO_ROOT / "data" / "landing"
BRONZE_BASE_PATH = REPO_ROOT / "data" / "bronze"
VALIDATION_OUTPUT_PATH = REPO_ROOT / "docs" / "validation" / "spark" / "bronze_ingestion_counts.txt"

LOAD_DATE = "2026-05-09"

ENTITIES = [
    "customers",
    "orders",
    "order_items",
    "products",
    "reviews",
]

print(ENTITIES)
def create_spark_session() -> SparkSession:
    return (
        SparkSession.builder
        .appName("Retail Bronze Ingestion")
        .master("local[*]")
        .getOrCreate()
    )

def ingest_entity(spark: SparkSession, entity: str) -> str:
    print("hlooooo")
    input_path = LANDING_BASE_PATH / entity / LOAD_DATE
    output_path = BRONZE_BASE_PATH / entity

    if not input_path.exists():
        raise FileNotFoundError(f"Input path does not exist: {input_path}")
    
    df = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(str(input_path))
    )

    print(df.show(5))
    df = (
        df
        .withColumn("load_date", lit(LOAD_DATE))
        .withColumn("ingestion_timestamp", current_timestamp())
    )

    row_count = df.count()

    (
        df.write
        .mode("overwrite")
        .partitionBy("load_date")
        .parquet(str(output_path))
    )

    return f"{entity}: {row_count}"


def main() -> None:
    spark = create_spark_session()

    try:
        results = []

        for entity in ENTITIES:
            print(entity)
            result = ingest_entity(spark, entity)
            print(result)
            results.append(result)
        
        VALIDATION_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

        with open(VALIDATION_OUTPUT_PATH, "w", encoding="utf-8") as file:
            file.write("\n".join(results))
            
        input("Process complete! Press Enter to close the Spark Session and exit...")

    finally:
        spark.stop()

if __name__ == "__main__":
    main()