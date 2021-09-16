# -*- coding: utf-8 -*-
"""Test simplistic protobuf parser."""
from mkdocs_protobuf.plugin import find_and_replace
from mkdocs_protobuf.plugin import read_proto


def test_read() -> None:
    """Read protobuf and assert results."""
    messages = read_proto("tests/proto/test.proto")
    assert len(messages) == 6
    assert set(messages.keys()) == {"Test", "TestMessageA", "TestMessageB", "Map", "KeyValue", "TestMessageB", "Foo"}
    assert "TestMessageB" not in messages["TestMessageA"]

    messages = read_proto("tests/proto/test2.proto")
    assert len(messages) == 5
    assert set(messages.keys()) == {"Bob", "TestMessageC", "Dict", "KV", "TestMessageD"}


def test_find_and_replace() -> None:
    """Replace template with protobuf."""
    messages = read_proto("tests/proto/test.proto")
    with open("tests/docs/index.md") as f:
        content = f.read()
    result = find_and_replace(content, messages)
    assert expected == result


expected = """Test

```
message TestMessageA {
    oneof test_message_a_type{
        int32 i32 = 1;
        int64 i64 = 2;
        string var_char = 3;
        Map map = 4;
    }

    message Map {
        message KeyValue {
            string key = 1;
            string value = 2;
        }

        repeated KeyValue key_values = 1;
    }
}
```

```
message Test {
    oneof test_type {
        TestMessageA testA= 1;
        TestMessageB testB = 2;
    }

    message TestMessageA {
        oneof test_message_a_type{
            int32 i32 = 1;
            int64 i64 = 2;
            string var_char = 3;
            Map map = 4;
        }

        message Map {
            message KeyValue {
                string key = 1;
                string value = 2;
            }

            repeated KeyValue key_values = 1;
        }
    }

    message TestMessageB {
      int32 foo = 1;
      string bar = 2;
    }

}
```
"""
