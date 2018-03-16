# MediaScrub

## Description

CLI web page media scrubber/downloader with some url level filtering options.

## Installation

From the repo directory:

`sudo pip install -e .`

## Removal

`sudo pip uninstall mediascrub`

## Usage

Run mediascrub in the target directory where the files are to be stored in.

    usage: mediascrub [-h] [-d DEPTH] [-e N [N ...]] [-l] [-m N [N ...]] [-n]
                  [-o OUTPUT_PATH] [-p {domain,url}] [-t TIMEOUT]
                  [-u N [N ...]]
                  URL

    Download files from a website

    positional arguments:
           URL                   Root URL for searching

    optional arguments:
          -h, --help            show this help message and exit
          -d DEPTH, --depth DEPTH
                                Exploration link depth (default: 0)
          -e N [N ...], --ext-filter N [N ...]
                                Media extension filter (default: ['png', 'jpg',
                                'gif'])
          -l, --list            Create a list file (media-list.txt) with all media
                                urls (default: False)
          -m N [N ...], --media-filter N [N ...]
                                Media URL case-sensitive filter (default: None)
          -n, --no-dwl          Downloading disabled and creates a media link file
                                (--list) automatically (default: False)
          -p {domain,url}, --prefix {domain,url}
                                Relative URL prefix type (default: domain)
          -t TIMEOUT, --timeout TIMEOUT
                                Link exploration timeout in seconds (default: 5)
          -u N [N ...], --url-filter N [N ...]
                                URL case-sensitive filter (default: None)


#### Example

Scrub from "http://somesite.com/tgp/index.html":
* Media with extension 'jpg' or 'jpeg' and 'car' in the full path name.
* Link depth of 1 where the URL has 'Photo' or 'photo'.

`$ mediascrub http://somesite.com/tgp/ --depth 1 -media-filter cars -url-filter Photo photo -ext-filter jpg jpeg` 

# Requirements

Linux, Python3 and wget installed.

Python libraries:
* urllib3
* colorama
* bs4

## License

Released under the GNU General Public Licence 2 (GPL2).