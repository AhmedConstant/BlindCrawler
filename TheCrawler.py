# Requests Module [see here for more info: https://requests.readthedocs.io/en/master/]
import requests.exceptions
import requests
# regular Expretion [see here for more info: https://docs.python.org/2/library/re.htm]
import re
#
import random

class TheCrawler():
    '''
        [Class Name]
            TheCrawler
        [Class Objectives]
            Crawling wep pages
        [The Crawling Algorithm]
            
            its a just an iteration 
            and it works as follow:

            >> start_point: the url that the crawler start with it
            >> crawling_log: which save the visited & un-visitied pages
                > store the start_point in the crawled[] list
                > if the start_point is in the un_crawled[] list
                    > delete the start_point from the un_crawled[] list "to prevent visting it again"
            >> visit the start_point
            >> get the HTML source code from the start_point
            >> use regex to extract certian patterns from the HTML code
                > e.x: subdomains, endpoints, urls, emails, credentials, UUID...etc
            >> store the exctracted data in the class lists
                > emails[], schemes[], subdomains[] ...etc
            >> check the base condition [its the codition that end the loop!]
                > if the list named un_crawled[] is empty
                    > that means that there are no more URLs to visit
                        > end the Loop
                > if the list named un_crawled[] is not empty
                    > that means that there are URLs to visit
                        > start the Loop agian with start_point = un_crawled[-1] "last URL in the un_crawled[] list"    
    '''

    def __init__(self, target_domain: str, start_point: str, sanitized_domain: str)-> None:
        '''
            [Method Named]
                __init__
            [Method Descreption]
                initialized when the object been made
            [Method Function]
                >> set the
                    > start_point "the URL to start crawling with"
                    > required exctract list
                    > target domain
                    > regex_domain "excape any special characters in the domain -if any- string to use it later in the regex pattern"
                >> create the temporary databases "lists[] used to store the output crawling data"
        '''

        self.start_point = start_point
        self.sanitized_domain = sanitized_domain
        self.target_domain = target_domain
        self.user_agent = {'user-agent': 'BlindCrawler'}

        #### Start Databases section
        # List to store the crawled links
        self.crawled = []
        # List to store the un crawled links
        self.un_crawled = []
        # List to store schemes
        self.schemes = []
        # List to store subdomains
        self.subdomains = []
        # List to store paths
        self.paths = []
        # List to store emails
        self.emails = []
        # Dictionary to store URL:Comment
        self.comments = {}
        #### End Databases section

        #### Section
        # Regex pattern to use in ignoring any URL with theses extensions
        #   > images URLs
        #   > fonts URLs 
        #   > CSS URLs
        #   > flash files URLs
        self.excluded_urls_pattern = r'(\.esd|\.png|\.svg|\.jpg|\.jpeg|\.bmp|\.ico|\.gif|\.tiff|\.hdr|\.heif|\.bpg|\.webp|\.img|\.css|\.swf|\.ttf|\.oft|\.woff|\.woff2|\.eot)'
        ### End Section

        #### Start Pre-Crawling Section
        # The method is documented below
        self.pre_crawling()
        # set the start point in the uncrawled[] list
        self.un_crawled.append(self.start_point)
        #### End Pre-Crawling Section

    def pre_crawling(self)-> None:
        '''
            some endpoints to get more URLs
        '''

        # Web Archive CDX API; to Get more URLs
        self.un_crawled.append(f'http://web.archive.org/cdx/search/cdx?url={self.target_domain}&output=text&filter=statuscode:200&matchType=domain&fl=original&collapse=urlkey')
        
        # sitemap.xml file
        self.un_crawled.append(f'https://{self.target_domain}/sitemap.xml')

        # robots.txt file
        self.un_crawled.append(f'https://{self.target_domain}/robots.txt')

    def the_discoverer(self, html: str) -> bool:
        '''
            [Method Name]
                the_discoverer
            [Method Function]
                exctract data -that meets regex patterns- from the HTML source Code
                that returned from the request to the start_point web page
            [Method Algorithm]
                >> exctract data
                >> check it there is no data exctracted
                    > end the method & return false
                >> if there is data
                    > loop throw it & and insert data into the Class databases "the lists []" 
        '''

        # if the current crawled URL is /robot.txt
        if re.search('(\/robots.txt)$', self.un_crawled[-1]):

            robots_file = re.findall(r"\/([A-z0-9\/\-\_\&\=\?\#\%\.\+]+)$", html)
        
            if len(robots_file) == 0:
                # end the Method
                pass
            else:
                for path in range(0, len(robots_file)):

                    # cheack if the url is not empty
                    if robots_file[path][0] is not '':
                        rel_to_abs = f'https://{self.target_domain}{robots_file[path][0]}'

                        # cheack if the url is not in the crawled[] list
                        if rel_to_abs not in self.crawled:
                            # check if the url has one of the excluded extentions
                            if (re.search(self.excluded_urls_pattern, rel_to_abs)):
                                # just pass!
                                pass
                            else:
                                # Check if the url is already in the uncrawled[] list
                                if rel_to_abs not in self.un_crawled:
                                    # store the url in the un_crawled[] lists
                                    self.un_crawled.append(rel_to_abs)


        #### Start URLs 'absolute paths' exctraction Section
        absolute_paths = re.findall(r"((https?|[A-z]{3,10})://([A-z0-9]+)?\.?"+self.sanitized_domain+".[a-z]{2,6}([A-z0-9\/\-\_\&\=\?\#\%\.]+)?)", html)

        # if there is no URLs -that meets the regex pattern- in the HTML source code
        if len(absolute_paths) == 0:
            # end the Method
            pass
        # if there a URLs in the HTML source code "exctracted into the UTLs[] list"
        else:
            # loop thruogh the URLs[] list "witch contains URLs devided into 4 groups"
            #   0> The whole link e.x: scheme://sub.domain.tld/path/to/the/end/and/beyond
            #   1> The scheme
            #   2> The subdomains
            #   3> The Path
            for url in range(0, len(absolute_paths)):
                
                # cheack if the url is not empty
                if absolute_paths[url][0] is not '':
                    # cheack if the url is not in the crawled[] list
                    if absolute_paths[url][0] not in self.crawled:
                        # check if the url has one of the excluded extentions
                        if (re.search(self.excluded_urls_pattern, absolute_paths[url][0])):
                            # just pass!
                            pass
                        else:
                            # Check if the url is already in the uncrawled[] list
                            if absolute_paths[url][0] not in self.un_crawled:
                                # store the url in the un_crawled[] lists
                                self.un_crawled.append(absolute_paths[url][0])
                
                # cheack if the scheme is not empty
                if absolute_paths[url][1] is not '':
                    # cheack if the scheme is not already in the schemes[] list
                    if absolute_paths[url][1] not in self.schemes:
                        # store the scheme in the schemes[] lists
                        self.schemes.append(absolute_paths[url][1])

                # cheack if the subdomain is not empty
                if absolute_paths[url][2] is not '':
                    # cheack if the subdomain is not already in the subdomains[] list
                    if absolute_paths[url][2] not in self.subdomains:
                        # store the subdomain in the subdomains[] lists
                        self.subdomains.append(absolute_paths[url][2])
                
                # cheack if the path is not empty
                if absolute_paths[url][3] is not '':
                    # cheack if the path is not already in the pathes[] list
                    if absolute_paths[url][3] not in self.paths:
                        # store the path in the pathes[] lists
                        self.paths.append(absolute_paths[url][3])    
        #### End URLs exctraction Section


        #### Start URLs 'relative paths' exctraction Section
        ## <a>      href
        ## <img>    src
        ## JS Code? window.location
        ## <Meta> 
        relative_paths = re.findall(r"(href|src)(=[\'\"]?)\/([A-z0-9\/\=\?\&\_\-\.]+)([\'\"]?)", html)

        # if there is no URLs -that meets the regex pattern- in the HTML source code
        if len(relative_paths) == 0:
            pass      
        # if there a relative paths in the HTML source code
        else:
            # loop thruogh the relative_paths[] list "witch contains relative_paths devided into 4 groups"
            #   0> href | src
            #   1> " | '
            #   2> the relative path
            #   3> " | '
            for path in range(0, len(relative_paths)):

                # cheack if the url is not empty
                if relative_paths[path][2] is not '':

                    # Convert the relative path into an abolute path
                    # by adding the start point as a prefix
                    # the start_point variable at this point is
                    # the Curenttly crawled page
                    # so /path-to-hell >> http://sub.domain.com/path-to-hell
                    if relative_paths[path][2] not in self.paths:
                        self.paths.append(relative_paths[path][2])

                        if self.un_crawled[-1].endswith('/'):
                            abs_p = self.un_crawled[-1].rstrip('/')
                        if relative_paths[path][2].startswith('/'):
                            rel_p= relative_paths[path][2].lstrip('/')

                        rel_to_abs = f'{abs_p}/{rel_p}'

                        # cheack if the url is not in the crawled[] list
                        if rel_to_abs not in self.crawled:
                            # check if the url has one of the excluded extentions
                            if (re.search(self.excluded_urls_pattern, rel_to_abs)):
                                # just pass!
                                pass
                            else:
                                # Check if the url is already in the uncrawled[] list
                                if rel_to_abs not in self.un_crawled:
                                    # store the url in the un_crawled[] lists
                                    self.un_crawled.append(rel_to_abs)
        #### End URLs exctraction Section

        #### Start Data exctraction Section
        # Exctract emails from HTML Source Code
        exctracted_emails = re.findall(r"[A-z0-9\.\-\_]+@[A-z]+\.[A-z]{2,}", html)
        # If the pattern returns emails
        if len(exctracted_emails) != 0:
            # Loop throw the extracted emails[]
            for exctracted_email in exctracted_emails:
                # if the email not in the emails[] database list
                if exctracted_email not in self.emails:
                    # store the email in the Class Database "emails[] list"
                    self.emails.append(exctracted_email)

        # Exctract comments from HTML Source Code
        exctracted_comments = re.findall(r"<!--(.+?)-->", html) # HTML source comment
        exctracted_comments.append(re.findall(r"^\/\/(.+)$", html)) # JS single comment
        exctracted_comments.append(re.findall(r"\/\*(.)\*\/", html, flags=re.DOTALL)) # JS multiable comment
        # If the pattern returns comments
        if len(exctracted_comments) != 0:
            # Loop throw the extracted comments{}
            for exctracted_comment in exctracted_comments:
                # if the comment not in the comments{} database
                if exctracted_comment not in self.comments.values():
                    # store the URL & the comment in the Database "comments{} Dict"
                    self.comments.update({f'{self.un_crawled[-1]}' : exctracted_comment})
        #### End Data exctraction Section

        return True

    def crawling_log(self)-> None:
        '''
            [Method Name]
                crawling_log
            [Method Function]
                Store the crawled & uncrawled links
        '''
        # store the start_point "curently crawling link" in the crawled[] list
        self.crawled.append(self.un_crawled[-1])

        # remove the last element in the un_crawled[] list "curently crawling link"
        self.un_crawled.pop()

    def get_agent(self)-> str:
        user_agents = [
            'Mozilla/5.0 CK={} (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
            'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; KTXN)',
            'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko)',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko; googleweblight) Chrome/38.0.1025.166 Mobile Safari/535.19',
            'Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.18',
            'Opera/9.80 (Linux armv7l) Presto/2.12.407 Version/12.51 , D50u-D1-UHD/V1.5.16-UHD (Vizio, D50u-D1, Wireless)',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36 OPR/36.0.2130.32',
            'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 YaBrowser/17.6.1.749 Yowser/2.5 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 YaBrowser/18.3.1.1232 Yowser/2.5 Safari/537.36',
            'Mozilla/5.0 (Linux; U; Android 4.4.2; zh-CN; HUAWEI MT7-TL00 Build/HuaweiMT7-TL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.3.8.909 Mobile Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 [FBAN/FBIOS;FBDV/iPhone11,8;FBMD/iPhone;FBSN/iOS;FBSV/13.3.1;FBSS/2;FBID/phone;FBLC/en_US;FBOP/5;FBCR/]',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 [FBAN/FBIOS;FBDV/iPhone9,2;FBMD/iPhone;FBSN/iOS;FBSV/13.3.1;FBSS/3;FBID/phone;FBLC/en_US;FBOP/5;FBCR/]'
        ]
        
        random_index = random.randint(0,len(user_agents) - 1)

        return user_agents[random_index]

    def crawl(self, random_agents: bool, cookies_values: str)-> None:
        
        # Understand 404 Pages
        response_404 = requests.get(f'{self.start_point}/ConstantWouldBeSurprisedIfThereIsAnUrlWithThisName-404Response')
        # store the length of the 404 page
        response_404_length = len(response_404.content)

        # start the crawling loop
        # and stop only when there is no more links to crawle
        while len(self.un_crawled) != 0:
            
            # Print The Currenly crawling URL
            # The below ANSI escape code will set the text colour. The format is:
            # \033[  Escape code, this is always the same
            # 1 = Style, 1 for normal.
            # 32 = Text colour, 32 for bright green, 37 for white.
            # 40m = Background colour, 40 is for black.
            print('\033[1;32;40m Crawled: \033[1;37;40m' + str(self.un_crawled[-1]))

            try:
                # if the random agents option is true
                if random_agents:
                    # the method already documented above
                    agent = self.get_agent()
                    # set the user agent
                    self.user_agent = {'user-agent': f'{agent}'}

                # set the user's supplied cookies
                if cookies_values:
                    cookies = {'Cookie': f'{cookies_values}'}    

                # initiate the request to the taget URL
                the_request = requests.get(self.un_crawled[-1], headers=self.user_agent, cookies=cookies, timeout=1)

            # catch the base-class exception, which will handle all HTTP error cases
            # this is an exeption for any Request error
            # [see here for more info https://requests.readthedocs.io/en/master/_modules/requests/exceptions/]
            except(requests.exceptions.RequestException):
                # When there is an HTTP error with the link
                # skip the extracting data step
                
                # The Method already documented above
                self.crawling_log()
            else:
                # if the program get here
                # that means the request completed successfully
                # shall we continue?
                # like you have an opinion in this! :')

                # if the length of the page is equal to the length of the 404 page
                # pass the content discovery phase
                if len(the_request.content) == response_404_length:
                    # The Method already documented above
                    self.crawling_log()
                else:
                    try:
                        # Get the HTML source -from the request- in text
                        html = the_request.text

                        # The Method already documented above
                        self.the_discoverer(html)

                        # The Method already documented above
                        self.crawling_log()
                    except:
                        # The Method already documented above
                        self.crawling_log()