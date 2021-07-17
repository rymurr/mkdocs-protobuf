# -*- coding: utf-8 -*-
"""Protobuf plugin for mkdocs."""
import logging
import os
import re
from typing import Any, Dict

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

    config_scheme = (("proto_dir", Type(str, default=None)), ("jinja_options", Type(dict, default={})))

    def __init__(self: "ProtobufDisplay") -> None:
        """Initialise self members."""
        self.messages: Dict = {"proto": {"message": dict()}}

    def on_pre_build(self: "ProtobufDisplay", config: Config, **kwargs: Any) -> None:
        """Set up Jinja and read protobuf director."""
        jinja_options: Dict[str, Any] = self.config["jinja_options"]
        self.env = jinja2.Environment(undefined=jinja2.DebugUndefined, autoescape=True, **jinja_options)
        for root, _, files in os.walk(self.config["proto_dir"]):
            for proto in files:
                self.messages["proto"]["message"].update(read_proto(os.path.abspath(os.path.join(root, proto))))

    def on_page_markdown(self: "ProtobufDisplay", markdown: str, page: Page, **kwargs: Any) -> str:
        """Parse a page for any protobuf templates."""
        try:
            md_template = self.env.from_string(markdown)
            return md_template.render(self.messages)
        except jinja2.exceptions.TemplateSyntaxError as e:
            raise PluginError(f"Unable to render template for page {page.file}") from e


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
        count = 0
        msg_end = None
        for i, c in enumerate(data[msg_start:]):
            if c == "{":
                count += 1
            elif count > 0 and c == "}":
                count -= 1
            elif count == 0 and c == "}":
                msg_end = i + msg_start
        if not msg_end:
            log.warning(f"Unable to parse proto file {proto_file}")
        msg_content = data[msg_start:msg_end]
        msg = "\n".join([data[found.start() : found.end()], msg_content, "}"])
        messages[msg_name] = msg
    return messages
