from logging import getLogger, StreamHandler, FileHandler, DEBUG, Formatter, ERROR, INFO
from pathlib import Path
import sys

def create_logger(log_path: str):
    # 標準出力・標準エラー出力をUTF-8に設定（VSCodeデバッグコンソール文字化け対策）
    if not hasattr(sys, 'frozen'):
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')

    log_pobj = Path(log_path).resolve()
    if not log_pobj.exists():
        with open(log_pobj, 'w', encoding='utf-8') as f:
            pass # 空のログファイルを作成
    log_ = getLogger(__name__)
    formatter = Formatter('%(asctime)s [%(levelname)s] %(message)s [%(name)s]')
    stream_handler = StreamHandler()
    stream_handler.setLevel(DEBUG)
    stream_handler.setFormatter(formatter)
    file_handler = FileHandler(log_path, encoding='utf-8')
    file_handler.setLevel(INFO)
    file_handler.setFormatter(formatter)
    log_.addHandler(stream_handler)
    log_.addHandler(file_handler)
    log_.setLevel(DEBUG)
    return log_

if __name__ == '__main__':
    log_ = create_logger('error_text.log')
    log_.debug('debug')
    log_.error('error')