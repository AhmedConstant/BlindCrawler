# Parser for command-line options & arguments [see here for more info: https://docs.python.org/3/library/argparse.html]
import argparse
from argparse import RawTextHelpFormatter
# regular Expretion [see here for more info: https://docs.python.org/2/library/re.htm]
import re
# Requests Module [see here for more info: https://requests.readthedocs.io/en/master/]
import requests

class Bootstrap():

    '''
        [Class Name]
            Bootstrap
        [Class Objectives]
            Script Initialization
        [The Algorithm]
            
        >> handle the user inputs arguments with argparse
        >> return data that ready to process by thr crawler
    '''
    
    def __init__(self):

        # Construct the argument parser
        ap = argparse.ArgumentParser(
            prog='BlindCrawler',
            description='>> Take a moment to read the usage, it doesn\'t bite!.',
            usage='BlindCrawler [-s https://sub.domain.tld/path-to-hell]',
            epilog='>> The Author: https://twitter.com/a_Constant_',
            # This formater just for inserting newline in the help string!
            # This is a very silly reason to consume resources! bad me! 
            formatter_class=RawTextHelpFormatter
        )

        # --start-point
        ap.add_argument(
            "-s",
            "--start-point",
            metavar=('\b'), # thats what make no space after the s [-s, --start-points]
            required=True,
            type=self.validate_start_point, # Method to check if the url is working
            help="\nThe URL to start crawling with [http://sub.domain.tld/path-to-hell]."
        )
        # --cookies
        ap.add_argument(
            "-c",
            "--cookies",
            metavar=('\b'),
            default=' ',
            required=False,
            help="\nA user supplied cookie."
        )
        # --random-agents
        ap.add_argument(
            "--random-agents",
            required=False,
            action='store_true', # set the value to true
            help="\nUse random user-agents when crawling."
        )

        # parse_args() returns an object
        # vars convert the object to a dictionary
        # usage of self.arguments:> self.arguments('key') >> value 
        self.arguments = vars(ap.parse_args())

    def validate_start_point(self, start_point: str):
        '''
            [Method Name]
                >> validate_start_point
            [Method Fuction]
                >> take the start point 'URL' from user input
                >> make a HEAD request to the URL to make sute it's up
        '''
        try:
            # send a head request  to check the server is up
            requests.head(start_point)
        except:
            # rise an error if there a problem
            msg = f"\n\nThe url: {start_point} doesn't seem to work!\n"
            raise argparse.ArgumentTypeError(msg)
        else:
            return start_point        

    def get_target_domain(self)-> str:
        # extract the domain from the start point URL
        domain = re.findall(r'(http|https)(:\/\/)([A-z0-9\.\-]+)', self.arguments['start_point'])
        
        # the regex return a list[] with 3 groups 'indexs'
        ## domain[0] = https
        ## domain[1] = :// 
        ## domain[2] = domain.tld
        self.domain = domain[0][2] 

    def get_sanitized_target_domain(self)-> str:
        '''
            the Method return sanitized domain without the subdomain or the TLD
            sub.dom-ain.com >> domain
        '''
        # this is an inefficient way to find out whether the domain has a subdomain or not 
        domain_to_escape = re.findall(r'([a-z0-9\-]+\.)?([a-z0-9\-]+)(\.[A-z]{2,})', self.domain)
        
        # if the length is 3
        # then it has a subdomain na the domain is in the scoend index
        if len(domain_to_escape[0]) == 3:
            # scape the special chrs like -
            # from the domain 
            self.sanitized_domain = re.escape(domain_to_escape[0][1]) # this sanitaized value will be used in the Crawler regex
        
        # else it has not
        # and the domain is in the first index
        else:
            # scape the special chrs like -
            # from the domain 
            self.sanitized_domain = re.escape(domain_to_escape[0][0]) # this sanitaized value will be used in the Crawler regex

    def crawling_setup(self):

        # The method already documented above
        self.get_target_domain()
        # The method already documented above
        self.get_sanitized_target_domain()
