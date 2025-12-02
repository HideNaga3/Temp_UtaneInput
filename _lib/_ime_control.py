import subprocess
import traceback
import os
import sys
from ._create_logger import create_logger

def set_ime_mode_jp_or_en(mode: str = 'en'):
    try:
        error_log_path = './data/error.log'
        log_ = create_logger(error_log_path)

        try:
            if getattr(sys, 'frozen', False): # 実行ファイルの場合
                application_path = sys._MEIPASS # 実行ファイルのパス
                ahk_script_path = os.path.join(application_path, '_ime_control.ahk')
                ahk_executable = os.path.join(application_path, 'AutoHotkey64_2.0.18.exe')
            else: # スクリプトファイルの場合
                # _libフォルダの親ディレクトリ（プロジェクトルート）を取得
                application_path = os.path.dirname(os.path.dirname(__file__))
                ahk_script_path = os.path.join(application_path, '_ime_control.ahk')
                ahk_executable = os.path.join(application_path, 'AutoHotkey64_2.0.18.exe')
        except Exception as e:
            print('_ime_control.pyのset_ime_mode_jp_or_en関数でエラーが発生しました。 002')
            print(e)

        # IMEのモードに応じてAutoHotkeyの関数を呼び出す
        if mode == 'jp':
            subprocess.run([ahk_executable, ahk_script_path, 'IME_On'], check=True)
        elif mode == 'en':
            subprocess.run([ahk_executable, ahk_script_path, 'IME_Off'], check=True)

    except Exception as e:
        print('_ime_control.pyのset_ime_mode_jp_or_en関数でエラーが発生しました。 002')
        print(e)
        log_.error(traceback.format_exc())

if __name__ == '__main__':
    set_ime_mode_jp_or_en('jp')  # 日本語IMEをオンにする
    # set_ime_mode_jp_or_en('en')  # 日本語IMEをオフにする
