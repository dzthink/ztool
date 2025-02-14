import subprocess
import json

def get_blame(repo_root_dir, file_path,commit=None):
    """
    获取指定文件的 Git Blame 信息。

    :param file_path: 文件路径
    :param commit: 可选的特定提交哈希
    :return: 包含每行信息的列表，每个元素是一个字典，包含 'commit', 'author', 'date', 'line'
    """
    cmd = ['git', 'blame']
    cmd.append('-w')  # 忽略空白变化
    if commit:
        cmd.append(f'-e {commit}')
    cmd.append(file_path)
    
    result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True, check=True, cwd=repo_root_dir)
    lines = result.stdout.splitlines()
    
    blame_info = {}
    for line in lines:
        try:
            parts = line.split(maxsplit=6)
            if len(parts) not in (6,7):
                print(line)
                continue
            if len(parts) == 6:
                parts.append('')
            commit_hash, author, date,time_h, time_z, line_num, content = parts
            line_num = int(line_num.rstrip(')'))
            blame_info[line_num] = {
                'commit': commit_hash,
                'author': author.lstrip('('),
                'date': f"{date} {time_h} {time_z}",
                'line': line_num,
                'content': content
            }
        except Exception as e:
            print(f"{line} exception: {e}")
    return blame_info