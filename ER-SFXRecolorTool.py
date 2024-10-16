#####################################################################################

def main():
    try: 
        import recolor_gui
        
        # recolor_gui.check_admin()
        recolor_gui.setup_ui()
    except Exception as e:
        print(f"An error occurred while program is running: {e}")
        input("Press Enter to exit...")


#####################################################################################

if __name__ == '__main__': main()

#####################################################################################