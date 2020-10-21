# audioslicer

A small tool for splitting audio files into short segments. The behavior is controlled by the settings file.
The file audioslicer.py contains an implementation of the `AudioSlicer` class, which is used to do the slicing. An 
instance of the class keeps track of written files and their information so that a summary csv can be written after 
slicing. 

### Settings
The configuration is placed in a YAML file. By default the filename is `settings.yaml`. 

#### audio_dir
Directory of files to be sliced.

#### output_dir
Directory of sliced audio segments. If the directory does not exists, it is created. The directory is not emptied, but 
the existing files with the same filenames will be overwritten.  

#### output_csv
Filename for the summary csv file. The file contains a list of generated audio slices. 

#### use_hashing
If `use_hashing` is false, then the output filename is a running index. If `use_hashing` is true, then the output 
filename is a md5 hash generated from the original filename and the running index. 

#### normalize_input
If `normalize_input` is set to true, the source audio is normalized before slicing. After the normalization the absolute
maximum of the input signal is equal to one.

#### normalize_output
If `normalize_output` is set to true, the audio slices are normalized before writing. After the normalization the absolute
maximum of every sound clip is equal to one. The normalization method processes the audio with several channels at
once, i.e. the channels linked.

#### interval
Interval of slices in seconds.

#### length
Length of slices in seconds. 

#### Example configuration
```
audio_dir: ../audio
output_dir: output
output_csv: files.csv

use_hashing: true
normalize_input: true
normalize_output: false

interval: 10.0
length: 1.0
```