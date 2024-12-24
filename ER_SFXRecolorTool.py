import warnings
warnings.filterwarnings("ignore")

def main():
    try: 
        from utils.utils_common import handle_exception, setup_logger
        from utils import recolor_gui
        
        setup_logger("log.txt")
        recolor_gui.setup_ui()
    except Exception as e:
        try: handle_exception(e, "Main Thread")   # , on_closing
        except Exception as e2: print(f"Critical error:\n\n{e2}\n")
        input("Press Enter to exit...")

if __name__ == '__main__': main()
