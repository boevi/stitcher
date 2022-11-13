import argparse
from PIL import Image

def arg_parsing():
    parser = argparse.ArgumentParser(usage = '%(prog)s [-n output_file_name] [-o h/v] file1 file2 ...', description = 'Stitch images together.')
    parser.add_argument('-n', '--name', action = 'store', help = 'the name of the output file; will be saved in PNG format')
    parser.add_argument('-o', '--orientation', action = 'store', help = '\'h\' for horizontal or \'v\' for vertical')
    parser.add_argument('files', nargs = '*')
    return parser

def merge_images(files, vertical):
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
        y = 0
        result = Image.new('RGBA', (result_width, result_height))
        for i in range(len(images)):
            result.paste(images[i],(0, y))
            y += heights[i]
        return result
    else:
        result_width = sum(widths)
        result_height = max(heights)
        x = 0
        result = Image.new('RGBA', (result_width, result_height))
        for i in range(len(images)):
            result.paste(images[i],(x, 0))
            x += widths[i]
        return result

if __name__ == '__main__':
    parser = arg_parsing()
    args = parser.parse_args()
    vertical = -1
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
            stitch = merge_images(args.files, vertical)
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
            stitch.save(fname)
            print("Saved as", fname)
