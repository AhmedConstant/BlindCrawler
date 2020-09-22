import os

class TheOutput():
    '''
        [Class Name]
            Output
        [Class Objectives]
            Handle the program output
        [The Algorithm]  
        >> Make a directory with the name of the target's domian
        >> store the collected data from TheCrawler into a files 
    '''
    
    def __init__(self, domain: str, crawled: list, schemes: list, subdomains: list, paths: list, emails: list, comments: list):
        # The Target Domain : will be used in the Directory name
        self.domain = domain
        # The Path of the current working directory : will change after the make_dir() method
        self.O_path = os.getcwd()

        # Make the output directory
        self.make_dir()
        
        # Store collected data into the files 
        self.write_file(crawled, 'crawled')
        self.write_file(schemes, 'schemes')
        self.write_file(subdomains, 'subdomains')
        self.write_file(paths, 'paths')
        self.write_file(emails, 'emails')
        self.write_file(comments, 'comments')



    def make_dir(self):
        # Output irectory : with the name of the target's domain
        directory = f"{self.domain}"
        # Parent directory path : the current working directory
        parent_dir = self.O_path
        # final Path 
        path = os.path.join(parent_dir, directory)
        # Make the dir if it's not already exists
        if not os.path.exists(path):
            os.mkdir(path)
        # it's now the output directory
        self.O_path = path

    def write_file(self, data, title):
        # create the file in append mode 
        file = open(os.path.join(self.O_path, f"{title}.txt"), 'a+')
        # Loop through data
        for d in data:
            # check if it is a dictionary
            # the program uses the dict type to store coments
            # because it store both comment & and the URL contain that comment
            if type(data) == dict:
                # the output in the file will be like:
                # http://c.com --> credentials
                file.write(d + ' --> ' + str(data[d]) + '\n')
            else:
                file.write(d + '\n')
        # from the name of the method
        # obviously it used to close the file
        file.close()