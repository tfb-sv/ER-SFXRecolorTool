#####################################################################################
import warnings
warnings.filterwarnings("ignore")   # for matplotlib related

# TODOs

# before palet yanl��

# readme hint'e sfx'leri nerden bulabilece�i > readme
# siyah ekran kapat�lacak
# di�er sfx'lere destek > readme
#####################################################################################

def main():
    try: 
        import recolor_gui
        
        recolor_gui.setup_ui()
    except Exception as e:
        print(f"An error occurred while program is running: {e}")
        input("Press Enter to exit...")

#####################################################################################

if __name__ == '__main__': main()

#####################################################################################
