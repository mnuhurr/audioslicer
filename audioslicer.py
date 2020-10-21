
import hashlib
import os
import csv

import numpy as np
import soundfile as sf

class AudioSlicer:
    '''
    class to perform slicing of individual files. keeps track of generated segments. allows writing a summary csv
    after file splitting.
    '''

    def __init__(self, output_dir, audio_len, use_hashing=False):
        '''
        initialize slicer.

        :param output_dir: directory for output files. assume this exists
        :param interval: interval of slices in seconds
        :param audio_len: length of slices in seconds
        :param use_hashing: boolean value if the filenames should be encoded instead of numbering
        :param output_sr: output sample rate. use 0 to use the input sample rate
        '''

        self.output_dir = output_dir
        self.use_hashing = use_hashing

        self.audio_len = audio_len

        # counter
        self.out_count = 0

        self.csv_header = ['id', 'filename', 'source', 'offset', 'peak', 'rms']
        self.csv_rows = []

    def slice(self, filename, interval, normalize=False):
        '''
        process a single file. keeps track of the number of written files and updates the counter accordingly.

        :param filename:
        :return: None
        '''

        y, sr = sf.read(filename)

        num_slice_samples = int(self.audio_len * sr)
        interval_samples = int(interval * sr)

        for offset_samples in range(0, len(y), interval_samples):
            # output filename
            slice_fn = self.__out_fn__(hash_seed=filename)

            # output data
            slice_y = y[offset_samples:offset_samples + num_slice_samples]

            # for the last round: check if the slice length is full
            if len(slice_y) < num_slice_samples:
                continue

            # normalization
            if normalize:
                y = self.normalize(y)

            # write file
            sf.write(file=slice_fn, data=slice_y, samplerate=sr)

            # file info
            offset = offset_samples / sr
            rms = np.sqrt(np.mean(np.square(y)))
            peak = np.max(np.abs(y))
            row = [self.out_count, slice_fn, filename, offset, peak, rms]
            self.csv_rows.append(row)

            self.out_count += 1


    def normalize(self, x):
        '''
        normalize signal using the infinity norm (i.e. absolute maximum). if the absolute maximum is zero
        don't do anything. for multi channel signal normalization is done with the same maximum value.

        :param x: signal to normalize
        :return: normalized signal
        '''
        m = np.max(np.abs(x))

        if m > 0:
            return x / m

        return x

    def __out_fn__(self, hash_seed=''):
        '''
        construct a filename for the next slice file. the filename is based on the number of written files.

        :param hash_seed: something to add beside the index for the hashing, e.g. the original filename
        :return: str
        '''

        fn_base = '{:06d}'.format(self.out_count)

        if self.use_hashing:
            # to avoid having every time the same filename for the same numbers use the input as seed
            fn_base = hash_seed + fn_base
            fn_base = hashlib.md5(fn_base.encode('ascii')).hexdigest()

        fn_base = fn_base + '.wav'

        # construct full path
        fn = os.path.join(self.output_dir, fn_base)

        return fn


    def write_report(self, csv_filename):
        '''
        write the summary csv

        :param csv_filename: path to the csv file. suppose the directory exists as there is no error checking
        :return: None
        '''
        with open(csv_filename, 'wt') as f:
            csv_writer = csv.writer(f, delimiter=',')

            csv_writer.writerow(self.csv_header)
            csv_writer.writerows(self.csv_rows)
