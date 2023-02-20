import argparse
from PIL import Image

def arg_parsing():
    parser = argparse.ArgumentParser(usage = '%(prog)s [-n output_file_name] [-o h/v] [-a 1/2/3] file1 file2 ...', description = 'Stitch images together.')
    parser.add_argument('-n', '--name', action = 'store', help = 'the name of the output file; will be saved in PNG format')
    parser.add_argument('-o', '--orientation', action = 'store', help = '\'h\' for horizontal or \'v\' for vertical')
    parser.add_argument('-a', '--alignment', action = 'store', help = '\'1\' for top/left, \'2\' for center, \'3\' for bottom/right')
    parser.add_argument('files', nargs = '*')
    return parser

def merge_images(files, vertical, alignment):
    images = []
    widths = []
    heights = []
    for i in range(len(files)):
        print('Opening file:', files[i])
        try:
            images.append(Image.open(files[i]))
        except (FileNotFoundError, IsADirectoryError, PermissionError) as err:
            print(f"{files[i]}: {err.strerror}")
            exit()
        widths.append(images[i].width)
        heights.append(images[i].height)
    print('Stitching...')
    if vertical:
        result_width = max(widths)
        result_height = sum(heights)
        x = 0
        y = 0
        result = Image.new('RGBA', (result_width, result_height))
        for i in range(len(images)):
            match alignment:
                case 2:
                    x = int(result_width/2 - widths[i]/2)
                case 3:
                    x = result_width - widths[i]
            result.paste(images[i],(x, y))
            y += heights[i]
        return result
    else:
        result_width = sum(widths)
        result_height = max(heights)
        x = 0
        y = 0
        result = Image.new('RGBA', (result_width, result_height))
        for i in range(len(images)):
            match alignment:
                case 2:
                    y = int(result_height/2 - heights[i]/2)
                case 3:
                    y = result_height - heights[i]
            result.paste(images[i],(x, y))
            x += widths[i]
        return result

if __name__ == '__main__':
    parser = arg_parsing()
    args = parser.parse_args()
    vertical = -1
    align = 0
    fname = ''
    if (args.orientation):
        match args.orientation:
            case 'h':
                vertical = 0
            case 'v':
                vertical = 1
            case _:
                print('Incorrect orientation. \nRun with -h for help.')
                exit()
    if (args.alignment):
        if (args.alignment not in ['1','2','3']):
            print('Incorrect alignment. \nRun with -h for help.')
            exit()
        align = int(args.alignment)
    match len(args.files):
        case 0:
            print('No files specified. \nRun with -h for help.')
        case 1:
            print('Only one file was specified. Use two or more. \nRun with -h for help.')
        case _:
            if (vertical == -1):
                print('Choose the orientation of the stitch.\nType \'h\' for horizontal or \'v\' for vertical:')
                o = input()
                match o:
                    case 'h':
                        vertical = 0
                    case 'v':
                        vertical = 1
                    case _:
                        print('Incorrect orientation. \nRun with -h for help.')
                        exit()
            if (align == 0):
                match vertical:
                    case 0:
                        print('Choose the alignment of the images.\nType 1 for top, 2 for center, or 3 for bottom:')
                    case 1:
                        print('Choose the alignment of the images.\nType 1 for left, 2 for center, or 3 for right:')
                a = input()
                if (a not in ['1','2','3']):
                    print('Incorrect alignment. \nRun with -h for help.')
                    exit()
                align = int(a)
            if (args.name):
                fname = args.name
            else:
                print('Enter the name of the output file (will be saved in PNG format automatically):')
                fname = input()
            if (fname == ''):
                print('Empty file name. \nRun with -h for help.')
                exit()
            if not (fname.casefold().endswith('.png')):
                fname += '.png'
            stitch = merge_images(args.files, vertical, align)
            stitch.save(fname)
            print("Saved as", fname)
