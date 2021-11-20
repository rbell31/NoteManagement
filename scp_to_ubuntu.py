import subprocess


def input_script(filename):
    script = ['scp', filename, 'post:/mnt/HDD/DATA_LAKE/raw_note/']
    return script


def process_file(filepath):
    proc = subprocess.run(input_script(filepath))



# testing = process_file('testingscp.txt')