import pytest
import cudf
import pandas
import os

from rapidscyber.io.factory.factory import Factory
from rapidscyber.io.reader.kafka_reader import KafkaReader
from rapidscyber.io.writer.kafka_writer import KafkaWriter
from rapidscyber.io.reader.fs_reader import FileSystemReader
from rapidscyber.io.writer.fs_writer import FileSystemWriter

test_input_base_path = "%s/input" % os.path.dirname(os.path.realpath(__file__))

kafka_config = {
    "kafka_brokers": "localhost:9092",
    "group_id": "cyber-dp",
    "batch_size": 100,
    "consumer_kafka_topics": ["consumer_topic_t1", "consumer_topic_t2"],
    "publisher_kafka_topic": "publisher_topic_t1",
    "output_delimiter": ",",
}

fs_config = {
    "input_path": "test_input",
    "output_path": "test_output",
    "schema": ["_col1", "_col2", "_col3"],
    "delimiter": ",",
    "required_cols": ["_col1", "_col2", "_col3"],
    "dtype": ["str", "str", "str"],
    "input_format": "text",
    "output_format": "text",
}

# Temporarily changing over cuDF to pandasDF because of issue with equality checks.
# Issue: https://github.com/rapidsai/cudf/issues/1750
expected_df = cudf.DataFrame(
    [
        ("firstname", ["Emma", "Ava", "Sophia"]),
        ("lastname", ["Olivia", "Isabella", "Charlotte"]),
        ("gender", ["F", "F", "F"]),
    ]
).to_pandas()


@pytest.mark.parametrize("kafka_config", [kafka_config])
def test_get_io_reader_kafka(kafka_config):
    reader = Factory.get_reader("kafka", kafka_config)
    expected_cls = KafkaReader
    assert isinstance(reader, expected_cls)


@pytest.mark.parametrize("kafka_config", [kafka_config])
def test_get_io_writer_kafka(kafka_config):
    writer = Factory.get_writer("kafka", kafka_config)
    expected_cls = KafkaWriter
    assert isinstance(writer, expected_cls)


@pytest.mark.parametrize("fs_config", [fs_config])
def test_get_io_reader_fs(fs_config):
    reader = Factory.get_reader("fs", fs_config)
    expected_cls = FileSystemReader
    assert isinstance(reader, expected_cls)


@pytest.mark.parametrize("fs_config", [fs_config])
def test_get_io_writer_fs(fs_config):
    writer = Factory.get_writer("fs", fs_config)
    expected_cls = FileSystemWriter
    assert isinstance(writer, expected_cls)


@pytest.mark.parametrize("test_input_base_path", [test_input_base_path])
@pytest.mark.parametrize("expected_df", [expected_df])
def test_get_reader_text(test_input_base_path, expected_df):
    test_input_path = "%s/person.csv" % (test_input_base_path)
    config = {
        "input_path": test_input_path,
        "schema": ["firstname", "lastname", "gender"],
        "delimiter": ",",
        "required_cols": ["firstname", "lastname", "gender"],
        "dtype": ["str", "str", "str"],
        "header": 0,
        "input_format": "text",
    }
    reader_from_factory = Factory.get_reader("fs", config)
    fetched_df = reader_from_factory.fetch_data()

    # Temporarily changing over cuDF to pandasDF because of issue with equality checks.
    # Issue: https://github.com/rapidsai/cudf/issues/1750
    assert fetched_df.to_pandas().equals(expected_df)


@pytest.mark.parametrize("test_input_base_path", [test_input_base_path])
@pytest.mark.parametrize("expected_df", [expected_df])
def test_get_reader_parquet(test_input_base_path, expected_df):
    test_input_path = "%s/person.parquet" % (test_input_base_path)
    config = {
        "input_path": test_input_path,
        "required_cols": ["firstname", "lastname", "gender"],
        "input_format": "parquet",
    }
    reader_from_factory = Factory.get_reader("fs", config)
    fetched_df = reader_from_factory.fetch_data()

    # Temporarily changing over cuDF to pandasDF because of issue with equality checks.
    # Issue: https://github.com/rapidsai/cudf/issues/1750
    assert fetched_df.to_pandas().equals(expected_df)


@pytest.mark.parametrize("test_input_base_path", [test_input_base_path])
@pytest.mark.parametrize("expected_df", [expected_df])
def test_get_reader_orc(test_input_base_path, expected_df):
    test_input_path = "%s/person.orc" % (test_input_base_path)
    config = {
        "input_path": test_input_path,
        "required_cols": ["firstname", "lastname", "gender"],
        "input_format": "orc",
    }
    reader_from_factory = Factory.get_reader("fs", config)
    fetched_df = reader_from_factory.fetch_data()

    # Temporarily changing over cuDF to pandasDF because of issue with equality checks.
    # Issue: https://github.com/rapidsai/cudf/issues/1750
    assert fetched_df.to_pandas().equals(expected_df)