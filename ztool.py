#!/usr/bin/env python
from cmds import devops
from infra import config
import click

rb_config = {}
def init_conf():
    config.merge_rb_config(rb_config)
@click.group()
@click.pass_context
def main(ctx):
    pass

command_list = [
    devops.g_devops
]
cli = click.CommandCollection(sources=command_list)
if __name__ == '__main__':
    init_conf()
    cli(obj={})