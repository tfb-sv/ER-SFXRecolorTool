#####################################################################################
import warnings
warnings.filterwarnings("ignore")   # for matplotlib related

# TODOs

# info text update yaz�lar
# ignored yaz�s� ekrana gelsin
# checkbox ve progressbar pad �st alt kontrol et

# several iterations due to toning? > readme
# i have identified de�i�tir > readme
# ?? Launch the game using > readme

# console kapat�lacak > make exe py
# examples kopyalancak > make exe py

# cls eklenecek
# testler genel 
# nexus ve git release
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
