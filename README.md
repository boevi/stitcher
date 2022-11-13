# stitcher
Tiny quick image stitcher. For now the alignment is only top/left.

## Usage
```stitcher.py [-n output_file_name] [-o h/v] file1 file2 ...```
- `-n`/`--name` - the name of the output file; will be saved in PNG format
- `-o`/`--orientation` - \'h\' for horizontal stitch or \'v\' for vertical stitch
- `file1 file2 ...` - the input files

Example: ```stitcher.py -n output.png -o h input1.png input2.jpg input3.png```

## Requirements
- Python 3.10+
- [Pillow](https://python-pillow.org/)
