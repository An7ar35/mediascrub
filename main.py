import argparse
import sys

from colorama import Fore, Style

import explorer
from flags import PrefixType
from writer import TextWriter


def main(argv):
    list_file_name = 'media-list.txt'

    parser = argparse.ArgumentParser(prog='mediascrub', description='Download files from a website')
    parser.add_argument('URL', help='Root URL for searching')
    parser.add_argument('-d', '--depth', default=0, type=int, help='Exploration link depth (default: %(default)s)')
    parser.add_argument('-e', '--ext-filter', metavar='N', nargs='+', default=['png', 'jpg', 'gif'],
                        help='Media extension filter (default: %(default)s)')
    parser.add_argument('-l', '--list', action='store_true',
                        help='Create a list file (media-list.txt) with all media urls (default: %(default)s)')
    parser.add_argument('-m', '--media-filter', metavar='N', nargs='+',
                        help='Media URL case-sensitive filter (default: %(default)s)')
    parser.add_argument('-o', '--output-path', default='.', help='Output path for the download')
    parser.add_argument('-p', '--prefix', default='domain', choices=['domain', 'url'],
                        help='Relative URL prefix type (default: %(default)s)')
    parser.add_argument('-t', '--timeout', default=5, help='Link exploration timeout in seconds (default: %(default)s)')
    parser.add_argument('-u', '--url-filter', metavar='N', nargs='+',
                        help='URL case-sensitive filter (default: %(default)s)')

    args = parser.parse_args(argv)
    print("Print media links to file .....: ", Fore.GREEN if args.list else Fore.RED, list_file_name if args.list else 'None', Style.RESET_ALL)
    # print(args)
    scrubber = explorer.LinkExplorer(args.ext_filter,
                                     args.url_filter,
                                     args.media_filter,
                                     PrefixType.translate(args.prefix),
                                     args.depth,
                                     args.timeout)
    urls = scrubber.grabLinks(args.URL)

    if args.list is True:
        writer = TextWriter()
        writer.open(list_file_name)
        for url in urls:
            writer.writeLine(url)


if __name__ == "__main__":
    main(sys.argv[1:])
