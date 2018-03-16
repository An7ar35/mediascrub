import re
from enum import Enum, auto

import bs4
import urllib3
from colorama import Fore, Style


class PrefixType(Enum):
    DOMAIN = auto()
    URL = auto()

    def describe(self):
        return self.name, self.value

    def __str__(self):
        return self.name

    @staticmethod
    def translate(string):
        if string is 'domain':
            return PrefixType.DOMAIN
        elif string is 'url':
            return PrefixType.URL
        else:
            raise ValueError('Prefix type \'' + string + '\' is not valid.')

class LinkExplorer:
    def __init__(self, ext_list, link_filters, media_filters, prefix_types, depth, timeout):
        self.ext_pattern = self.__buildExtPattern(ext_list)
        self.link_filter_pattern = self.__buildFilterPattern(link_filters)
        self.media_filter_pattern = self.__buildFilterPattern(media_filters)
        self.prefix_type = prefix_types
        self.depth = depth
        self.timeout = timeout
        self.http = urllib3.PoolManager()
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.visited_urls = set()

        print("REGEX link URL filter .........: ",
              Fore.CYAN if self.link_filter_pattern is not '' else Fore.RED,
              self.link_filter_pattern if self.link_filter_pattern is not '' else 'None',
              Style.RESET_ALL)
        print("REGEX media extension pattern .: ",
              Fore.CYAN if self.ext_pattern is not '' else Fore.RED,
              self.ext_pattern if self.ext_pattern is not '' else 'None',
              Style.RESET_ALL)
        print("REGEX media URL filter ........: ",
              Fore.CYAN if self.media_filter_pattern is not '' else Fore.RED,
              self.media_filter_pattern if self.media_filter_pattern is not '' else 'None',
              Style.RESET_ALL)
        print("Relative URL prefix type ......: ", Fore.CYAN, str(self.prefix_type), Style.RESET_ALL)
        print("Link search depth .............: ", Fore.CYAN, str(self.depth), Style.RESET_ALL)
        print("Connection timeout ............: ", Fore.CYAN, str(self.timeout) + "s", Style.RESET_ALL)


    def grabLinks(self, url):
        '''
        Gets all the media links present in the page
        @param url: URL of the page
        @return: List of all the media links
        '''
        print("Root URL ......................: ", Fore.LIGHTBLUE_EX, url, Style.RESET_ALL)
        media_links = set()
        count = 0

        if self.depth >= 0:
            self.__grabLinks(media_links, url, self.depth)

        self.http.clear()
        media_links = list(set(media_links))
        return media_links

    def __grabLinks(self, media_links, url, depth):
        '''
        Gets all the media links present in a page
        @param media_links: Global set of unique media links found
        @param url: URL of the page
        @param depth: Current link depth
        @return: List of all the media links
        '''
        if depth >= 0:
            # Gets media from the page
            page_links = self.__grabMedia(media_links, url)
            # Recurse if there is still depth to explore
            if (depth > 0):
                for link in page_links:
                    if re.search(re.compile(self.link_filter_pattern), link) is not None:
                        if self.__addToSet(self.visited_urls, link):  # If never visited
                            self.__grabLinks(media_links, link, depth - 1)

    def __grabMedia(self, media_links, url):
        '''
        Grabs link to any media found
        @param media_links: Global set of unique media links found
        @param url: URL of page
        @return: List of all other std links found in page
        '''
        page_links = []
        try:
            request = self.http.request("GET", url, timeout=self.timeout)
        except urllib3.exceptions.MaxRetryError:
            print("|-", Fore.MAGENTA, "(!) Error:", Fore.RESET, "Max GET retries reached on " + url)
        except urllib3.exceptions.LocationParseError:
            print("|-", Fore.MAGENTA, "(!) Error:", Fore.RESET, "Failed to parse \"" + url + "\"")
        else:
            html = request.data  # .decode("utf-8")
            count = 0

            for tag in bs4.BeautifulSoup(html, "html.parser").find_all("a", href=True):
                link = tag.get('href')
                # print("ful URL A: "+ link)
                link = self.__createAbsoluteURL(url, link)
                # print("ful URL B: "+ link)
                if re.search(self.ext_pattern, link) is not None:
                    if re.search(re.compile(self.media_filter_pattern), link) is not None:
                        if self.__addToSet(media_links, link):
                            count += 1
                else:
                    page_links.append(link)

            print("|- Found " + str(count) + " new media targets in " + url)
        return page_links

    def __buildExtPattern(self, ext_list):
        '''
        Builds a regex pattern for all given extensions
        @param ext_list: Extension list
        @return: Pattern string
        '''
        pattern = ['.*\.(?i:']
        for i, ext in enumerate(ext_list):
            if i > 0:
                pattern.append('|' + ext)
            else:
                pattern.append(ext)
        pattern.append(')')
        return ''.join(pattern)

    def __buildFilterPattern(self, filter_list):
        '''
        Build a regex pattern for all given filters
        @param filter_list: Filter list
        @return: Pattern string
        '''
        if filter_list:
            pattern = ['.*']
            for i, filter in enumerate(filter_list):
                if i > 0:
                    pattern.append('|' + filter)
                else:
                    pattern.append('(' + filter)
            pattern.append(').*')
            return ''.join(pattern)
        else:
            return ''

    def __createAbsoluteURL(self, base_url, relative_link):
        '''
        Creates an absolute URL from a page url and a relative link from that page
        @param base_url: Origin page URL
        @param relative_link: Relative link from origin page
        @return: Absolute URL
        '''
        if self.prefix_type == PrefixType.DOMAIN:
            return self.__addUrlPrefix(self.__getDomain(base_url), relative_link)
        else:
            return self.__addUrlPrefix(base_url, relative_link)

    def __addUrlPrefix(self, url, link):
        '''
        Adds the url before the link if the link is relative
        @param url: URL
        @param link: Link to check
        @return: Full absolute link
        '''
        # REGEX URL detection
        # Group 1: string starting with 'http'
        # Group 2: string starting with '//'
        capture = re.search(re.compile('(http.*)|(//.*)'), link)
        if capture is None:
            if url.endswith('/'):
                return url[:-1] + link
            else:
                return url + link
        elif capture.group(2) is not None:  # missing "http:" needs to be added before "//"
            return "http:" + link
        else:
            return link

    def __getDomain(self, url):
        '''
        Extracts domain url from a url
        @param url: Url to extract from
        @return: Domain url
        '''
        # REGEX for domain extraction. Match first of any groups:
        # Group 1: string with '//' in the middle and up to first single '/',
        # Group 2: string with '//' in the middle and up to the first '?',
        # Group 3: string with '//' in the middle and up to the first '#'.
        domain = re.search(re.compile('(.*//.*?)/|(.*//.*?)\?|(.*//.*?)[#]'), url)
        if domain is not None:
            if domain.group(1) is not None:
                return str(domain.group(1)) + '/'
            elif domain.group(2) is not None:
                return str(domain.group(2)) + '/'
            elif domain.group(3) is not None:
                return str(domain.group(3)) + '/'
        return str(url) + '/'

    def __addToSet(self, set, x):
        '''
        Adds to a set
        @param set: Set to add to
        @param x: Item to add to set
        @return: Success
        '''
        length = len(set)
        set.add(x)
        return len(set) != length

