# stitcher
Tiny quick image stitcher.

## Usage
```stitcher.py [-n output_file_name] [-o h/v] [-a 1/2/3] file1 file2 ...```
- `-n`/`--name` - the name of the output file; will be saved in PNG format
- `-o`/`--orientation` - \'h\' for horizontal stitch or \'v\' for vertical stitch
- `-a`/`--alignment` - \'1\' for top/left, \'2\' for center, \'3\' for bottom/right
- `file1 file2 ...` - the input files

Example: ```stitcher.py -n output.png -o h -a 2 input1.png input2.jpg input3.png```

## Requirements
- Python 3.10+
- [Pillow](https://python-pillow.org/)
