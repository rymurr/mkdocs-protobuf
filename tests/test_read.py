# -*- coding: utf-8 -*-
"""Test simplistic protobuf parser."""
from mkdocs_protobuf.plugin import read_proto


def test_read() -> None:
    """Read protobuf and assert results."""
    messages = read_proto("tests/proto/test.proto")
    assert len(messages) == 6
    assert set(messages.keys()) == {"Test", "TestMessageA", "TestMessageB", "Map", "KeyValue", "TestMessageB", "Foo"}

    messages = read_proto("tests/proto/test2.proto")
    assert len(messages) == 5
    assert set(messages.keys()) == {"Bob", "TestMessageC", "Dict", "KV", "TestMessageD"}
