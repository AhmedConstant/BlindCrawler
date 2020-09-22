# Import the class Bootstrap
from Bootstrap import Bootstrap
# Import the class crawler
from TheCrawler import TheCrawler
# Import the class O
from Output import TheOutput
#
import datetime
#
import pyfiglet

def main():
    # Set the program start time 
    program_start_time = datetime.datetime.now()

    # some unnecessary decorated text
    # i am bored, and i really need some shapes and colors
    print('\033[1;31;40m' + pyfiglet.figlet_format("Blind Crawler", font = "slant"), end='')
    print("\033[1;31;40m #" * 60)

    ########>> Stage 1: Boostrabing the Program
    # crate the instance
    bootstrap = Bootstrap()
    # set-up the data to be ready for crawling
    bootstrap.crawling_setup()

    ########>> Stage 2: Start the crawling process
    # Prepare the Crawler
    crawler = TheCrawler(
        bootstrap.domain, # str: domain.com
        bootstrap.arguments['start_point'], # str: http://sub.domain.tld/path
        bootstrap.sanitized_domain # str: domain
    )
    # # Fire the Crawler
    crawler.crawl(
        bootstrap.arguments['random_agents'], # bool: True|False
        bootstrap.arguments['cookies'] # str: if the user provide cookies
    )

    ########>> Stage 3: The Prize!
    # crate the instance
    TheOutput(
        bootstrap.domain,
        crawler.crawled,
        crawler.schemes,
        crawler.subdomains,
        crawler.paths,
        crawler.emails,
        crawler.comments
    )

    ########>> Stage 4: runtime report:
    print("\033[1;31;40m #" * 60)
    print("\033[1;37;40m Number of crawled pages: \033[1;31;40m" + str(len(crawler.crawled)))
    print("\033[1;37;40m Number of schemes: \033[1;31;40m" + str(len(crawler.schemes)))
    print("\033[1;37;40m Number of Subdomains: \033[1;31;40m" + str(len(crawler.subdomains)))
    print("\033[1;37;40m Number of Paths: \033[1;31;40m" + str(len(crawler.paths)))
    print("\033[1;37;40m Number of emails: \033[1;31;40m" + str(len(crawler.emails)))
    print("\033[1;37;40m Number of comments: \033[1;31;40m" + str(len(crawler.comments)))
    print('\n', end='')
    print("\033[1;35;40m Program Runtime: " + str(datetime.datetime.now() - program_start_time))
    print("\033[1;31;40m #" * 60, end='')

########>> Program Entry Point ->
if __name__ == '__main__':
    try:
      # The Program!
      main()
    # If the user interrupt the run, curse them!
    except KeyboardInterrupt:
      print('\033[1;31;40m KeyboardInterrupt: As You Like :(')
      print("\033[1;31;40m #" * 60, end='')
