
import os
import glob

from tqdm import tqdm

from common import load_config, check_output_dirs
from audioslicer import AudioSlicer

def get_file_list(dir_path, ext='.wav'):
    '''
    get list of files from a given directory

    :param dir_path: path to the dir
    :param ext: file extension. defaults to .wav
    :return: list of file paths
    '''

    wav_path = os.path.join(dir_path, '*' + ext)
    fns = glob.glob(wav_path)

    # return the file list in lexicographic order
    fns.sort()

    return fns


def main():
    # load configuration
    cfg = load_config()

    # create output directories if needed
    check_output_dirs(cfg)

    # worker
    slicer = AudioSlicer(output_dir=cfg['output_dir'],
                         audio_len=cfg['length'],
                         use_hashing=cfg['use_hashing'])

    # get file list
    filenames = get_file_list(cfg['audio_dir'])

    # process
    for fn in tqdm(filenames):
        slicer.slice(filename=fn,
                     interval=cfg['interval'],
                     normalize_input=cfg['normalize_input'],
                     normalize_output=cfg['normalize_output'])

    # summary
    slicer.write_report(cfg['output_csv'])

if __name__ == '__main__':
    main()
