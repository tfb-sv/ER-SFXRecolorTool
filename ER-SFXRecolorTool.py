#####################################################################################
import warnings
warnings.filterwarnings("ignore")   # for matplotlib related

# TODOs

# readme
# checkbox ve progressbar pad ust alt kontrol et
# nexus ve git release

# several iterations due to toning? > readme
# i have identified degistir > readme
# ?? Launch the game using > readme
# birkaç düzine denendi ama baþarýlý siyah vs problem > readme
# update için simply sil ve yenisini koy > readme
# f str > os > readme
# after recolor pencere checkbox > readme
# extensive tests > readme
#####################################################################################

def main():
    try: 
        from utils import recolor_gui
        
        recolor_gui.setup_ui()
    except Exception as e:
        print(f"An error occurred while program is running: {e}")
        input("Press Enter to exit...")

#####################################################################################

if __name__ == '__main__': main()

#####################################################################################
