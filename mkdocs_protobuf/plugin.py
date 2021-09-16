# -*- coding: utf-8 -*-
"""Protobuf plugin for mkdocs."""
import logging
import os
import re
from typing import Any
from typing import Dict
from typing import Optional

import jinja2
from mkdocs.config import Config
from mkdocs.config.config_options import Type
from mkdocs.exceptions import PluginError
from mkdocs.plugins import BasePlugin
from mkdocs.structure.pages import Page
from mkdocs.utils import warning_filter

log = logging.getLogger(__name__)
log.addFilter(warning_filter)


class ProtobufDisplay(BasePlugin):
    """Insert Protobuf IDL into templated markdown."""

    config_scheme = (("proto_dir", Type(str, default=None)),)

    def __init__(self: "ProtobufDisplay") -> None:
        """Initialise self members."""
        self.messages: Dict = dict()

    def on_pre_build(self: "ProtobufDisplay", config: Config, **kwargs: Any) -> None:
        """Read protobuf director."""
        for root, _, files in os.walk(self.config["proto_dir"]):
            for proto in files:
                self.messages.update(read_proto(os.path.abspath(os.path.join(root, proto))))

    def on_page_markdown(self: "ProtobufDisplay", markdown: str, page: Page, **kwargs: Any) -> str:
        """Parse a page for any protobuf templates."""
        try:
            md_template = find_and_replace(markdown, self.messages)
            return md_template
        except jinja2.exceptions.TemplateSyntaxError as e:
            raise PluginError(f"Unable to render template for page {page.file}") from e


def find_and_replace(markdown: str, messages: dict) -> str:
    """Find all message templates in the markdown document and replace with actual protobuf message."""
    find_template = re.compile("{% (.*) %}")
    transforms = []
    for found in find_template.finditer(markdown):
        msg_name = find_template.split(markdown[found.start() : found.end()])[1]
        msg = messages[msg_name.split(".")[-1]]
        transforms.append((re.compile("{% " + msg_name + " %}"), msg))
    for transform in transforms:
        markdown = transform[0].sub(transform[1], markdown)
    return markdown


def read_proto(proto_file: str) -> dict:
    """Read a proto file and return a dict of its messages."""
    if not os.path.isfile(proto_file):
        log.warning(f"Proto file {proto_file} does not exist.")
    messages = dict()
    try:
        with open(proto_file) as f:
            data = f.read()
    except OSError:
        log.warning(f"Unable to read {proto_file}")

    # todo handle IO errors
    regex = re.compile("message .* {")
    regex_name = re.compile("message (.*) {")
    for found in regex.finditer(data):
        msg_name = regex_name.split(data[found.start() : found.end()])[1]
        msg_start = found.end()
        count = 1
        msg_end = None

        # find the end of the message
        for i, c in enumerate(data[msg_start:]):
            if c == "{":
                count += 1
            elif c == "}":
                if count > 1:
                    count -= 1
                else:
                    msg_end = i + msg_start
                    break
        if not msg_end:
            log.warning(f"Unable to parse proto file {proto_file}")

        msg_content = _strip_indent(data, found, msg_start, msg_end)
        msg = "\n".join([data[found.start() : found.end()], msg_content, "}"])
        messages[msg_name] = msg
    return messages


def _strip_indent(data: str, found: re.Match, msg_start: int, msg_end: Optional[int]) -> str:
    # remove indentation from sub messages
    # extract previous newline and determine the indentation of this message
    last_newline = [i for i, c in enumerate(data[: found.start()]) if c == "\n"][-1]
    indent = found.start() - (last_newline + 1)

    # add 1 to msg_start to avoid the first newline post message
    msg = []
    for i in data[msg_start + 1 : msg_end].split("\n"):
        if not i:
            msg.append(i)
        remove_indent = i[indent:]
        if remove_indent:
            msg.append(remove_indent)
    return "\n".join(msg)
