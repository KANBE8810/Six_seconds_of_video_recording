import os
import shutil

# ファイルが入っているディレクトリパス
directory = 'ogawa'

# ディレクトリ内のファイルを取得し、50音順に並び替える
files = sorted(os.listdir(directory))

# 変更後のファイル名に使う数字
counter = 0

# ファイルをリネームする
for file in files:
    # 元のファイルのフルパス
    old_path = os.path.join(directory, file)
    
    # 新しいファイル名（数字）
    new_name = str(counter) + os.path.splitext(file)[1]
    
    # 新しいファイルのフルパス
    new_path = os.path.join(directory, new_name)
    
    # ファイルを移動＆リネーム
    shutil.move(old_path, new_path)
    
    # カウンターをインクリメント
    counter += 1

