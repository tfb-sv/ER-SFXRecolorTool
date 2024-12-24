import threading
import subprocess
import logging as log

def handle_global_thread_exception(args):
    thread_name = args.thread.name
    exc_value = args.exc_value
    handle_exception(exc_value, thread_name=thread_name)

def handle_exception(e, thread_name):   # , closing_function
    print(f"Error in {thread_name}:\n\n{e}\n")
    log.error(f"Error in {thread_name}:\n\n{e}\n", exc_info=True)
    # showinfo("ERROR", str(e))
    # closing_function()

def setup_logger(log_fp):
    logger = log.getLogger()
    logger.setLevel(log.DEBUG)
    log_format = '%(message)s'
    # log_format = '\n%(asctime)s - %(levelname)s - %(message)s\n'
    file_handler = log.FileHandler(log_fp, mode='w')
    file_handler.setLevel(log.DEBUG)
    file_formatter = log.Formatter(log_format)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    console_handler = log.StreamHandler()
    console_handler.setLevel(log.INFO)
    console_formatter = log.Formatter(log_format)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    log.getLogger('matplotlib').setLevel(log.WARNING)
    log.getLogger('PIL').setLevel(log.WARNING)
    threading.excepthook = handle_global_thread_exception 
    
def witchy_subprocess(command):
    witchy_silent_argument = "-s"   # previously it was "-p"
    command.append(witchy_silent_argument)
    _ = subprocess.run(command)

def custom_json_dumper(data, fp, indent=4):
    with open(fp, 'w', encoding='utf8') as f:
        f.write('{\n')
        key_text1 = f'{" " * indent}"sfx_ids": ['
        f.write(key_text1)
        for i, item in enumerate(data['sfx_ids']):
            if i != 0: f.write(" " * len(key_text1))
            f.write(f'{item}')
            if i < len(data['sfx_ids']) - 1: f.write(',\n')
            else: f.write('],\n')
        key_text2 = f'{" " * indent}"target_colors": {{'
        f.write(key_text2)
        for i, (key, value) in enumerate(data['target_colors'].items()):
            if i != 0: f.write(" " * len(key_text2))
            f.write(f'"{key}": {value}')
            if i < len(data['target_colors']) - 1: f.write(',\n')
            else: f.write('}\n')
        f.write('}')
