# main.py

import sys
import os

# 将项目根目录添加到 sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.ui_manager import UIManager

def main():
    ui_manager = UIManager()
    ui_manager.run()

if __name__ == "__main__":
    main()
