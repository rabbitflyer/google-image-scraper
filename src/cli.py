import argparse, os, sys
from enum import Enum

# Should revisit this to look for xdg_downloads in env
def get_download_path():
    """Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'Downloads')


def get_default_dir(search_key: str):
    """Generate the default folder to store scraped images in"""
    search_key = search_key.replace(" ", ".")
    default_dir = get_download_path()
    default_dir = os.path.join(default_dir, "google-image-scraper")
    default_dir = os.path.join(default_dir, search_key)
    return default_dir

def check_pos_int(val: int):
    val = int(val)
    if ( val > 0 ):
        return val
    else:
        raise ValueError

def get_arguments(argv=sys.argv):
    """ 
    The cli front end for the scraper.

    Keyword arguments:
    argv -- An array of keywords expected to look like sys.argv
    
    Returns:
    parser.parse_args() -- A struct with all required info to run the scraper
    """
    parser = argparse.ArgumentParser(description="Scrape Google for images")
    parser.add_argument("keyword", 
                        help="the phrase used to find images",
                        type=str,
                        nargs=1)
    parser.add_argument("-c", "--count",
                        help="How many images to try to scrape",
                        type=check_pos_int,
                        nargs="?",
                        default=10)
    parser.add_argument("-d", "--directory",
                        help="where to save scraped images",
                        type=str,
                        nargs="?")
    parser.add_argument("-t", "--threads",
                        help="How many threads to spawn and download from",
                        type=check_pos_int,
                        nargs="?",
                        default=1)
    parser.add_argument("-s", "--size",
                        help="Restrict your search to a certain size of image. Can be 'large', 'medium', or 'icon'.",
                        type=str,
                        nargs="?",
                        choices=['large','medium','icon'],
                        default='')
    parser.add_argument("--color",
                        help="Search for a certain color of image. Can be 'red', 'orange', 'yellow', 'green', 'teal', 'blue', 'purple', 'pink', 'white', 'gray', 'black', 'brown', 'grayscale', or 'transparent'.",
                        type=str,
                        nargs="?",
                        choices=['red', 'orange', 'yellow', 'green', 'teal', 'blue', 'purple', 'pink', 'white', 'gray', 'black', 'brown', 'grayscale', 'transparent'],
                        default='')
    parser.add_argument("-k", "--type",
                        help="The type of image to search for. Can be 'clipart', 'lineart', or 'animated'.",
                        type=str,
                        nargs="?",
                        choices=['clipart', 'lineart', 'animated'],
                        dest="imgtype",
                        default='')
    parser.add_argument("-p", "--safesearch",
                        help="Force the use of a specific safesearch setting. Can be 'on' or 'off'.",
                        type=str,
                        nargs="?",
                        choices=['on', 'off'],
                        default='')
    args = parser.parse_args(argv[1:])
    # Set default directory
    if args.directory is None:
        print(args.keyword[0])
        args.directory = get_default_dir(args.keyword[0])
    return args
