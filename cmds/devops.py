import click
import subprocess
import sys
import os
import stat
import time
import json
from pathlib import Path

@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def g_devops(ctx, debug):
    """_summary_

    Args:
        ctx (_type_): _description_
        debug (_type_): _description_
    """
    pass

@g_devops.command()
@click.pass_context
def install(ctx):
    _build_installer()
    dist = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "dist/ztool") 
    source = Path(dist)
    destination = Path().home() / "bin/ztool"
    destination.write_bytes(source.read_bytes())
    current_permissions = os.stat(destination.absolute().as_posix()).st_mode
    new_permissions = current_permissions | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
    os.chmod(destination.absolute().as_posix(), new_permissions)
    click.secho(f"安装成功", fg="green")
# 修改文件权限
def _build_installer():
    try:
        import PyInstaller
    except ImportError:
        click.echo("开始安装PyInstaller")
        result = subprocess.run(["conda", "run", "-n", "ztool", "conda", "install", "PyInstaller"], capture_output=True)
        # 检查 returncode
        if result.returncode == 0:
            click.secho("PyInstaller安装成功", fg="green")
        else:
            click.secho(f"PyInstaller安装失败:{result.stderr}", fg="red")
            return
    click.echo("开始构建安装包")
    result = subprocess.run(["conda", "run", "-n", "ztool", "pyinstaller","ztool.py","--collect-binaries=rainbow_cpplib", "--onefile", "--noupx", "--strip", "--optimize=1"], 
                            capture_output=True, cwd=os.path.dirname(os.path.abspath(sys.argv[0])))
    if result.returncode == 0:
        click.secho("构建安装包成功", fg="green")
    else:
        click.secho(f"构建安装包失败:{result.stderr}", fg="red")
        return