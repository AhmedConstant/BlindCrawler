# BlindCrawler
A tool for web crawling &amp; content discovery
# Installation
`git clone https://github.com/AhmedConstant/BlindCrawler.git`<br/>

`cd /BlindCrawler`<br/>

`pip install requirements.txt`<br/>

# Usage
![Runtime](https://github.com/AhmedConstant/Images/blob/master/blindcrawler-github.png)
![Runtime](https://github.com/AhmedConstant/Images/blob/master/Snap%202020-09-22%20at%2014.54.34.png)
### domain
`BlindCrawler.py -s https://domain.com`<br/>
### subdomain
`BlindCrawler.py -s https://sub.domain.com/path`<br/>
### random agents
`BlindCrawler.py -s https://sub.domain.com/path --random-agents`<br/>
### with cookies
`BlindCrawler.py -s https://sub.domain.com/path -c "key: value; key:value"`<br/>
# Features
# To-Do List
- [x] Relase beta version.
- [ ] Extract strings with high entropy from crawled pages. [UUID, Key..etc]
- [ ] Recognize the static/repetitive Urls to avoid crawling it & reduce time and resources.
- [ ] Let the user provide its own pattern to extract from crawled pages.
- [ ] Create a custom wordlist for directory bruteforcing.
- [ ] Search for potential DOM XSS vulnerable functions.
- [ ] Fuzzing the GET Parameters.
- [ ] .....
# The Author
Ahmed Constant<br/>
[Twitter](https://twitter.com/a_Constant_)
