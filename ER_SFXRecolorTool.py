import warnings
warnings.filterwarnings("ignore")   # , module="matplotlib"

def main():
    try: 
        from utils.utils_recolor import handle_exception, setup_logger
        from utils import recolor_gui
        
        setup_logger("log.txt")
        recolor_gui.setup_ui()
    except Exception as e:
        print(f"An error occurred while program is running: {e}")
        try: handle_exception(e)   # , on_closing
        except Exception as e2: 
            print(f"Error: {e2}")
            input("Press Enter to exit...")

if __name__ == '__main__': main()
