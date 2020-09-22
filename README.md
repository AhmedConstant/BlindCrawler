# BlindCrawler - Beta v1.0
![alt text](https://github.com/AhmedConstant/ImagesV/blob/master/blindcrawler-logo-github.png "BlindCrawler")<br/>
A tool for web crawling &amp; content discovery
# Installation
`git clone https://github.com/AhmedConstant/BlindCrawler.git`<br/>

`cd /BlindCrawler`<br/>

`sudo pip3 install requirements.txt`<br/>

# Usage
![Runtime](https://github.com/AhmedConstant/ImagesV/blob/master/blindcrawler-usges-github.png)
### domain
`python3 BlindCrawler.py -s https://domain.com`<br/>
### subdomain
`python3 BlindCrawler.py -s https://sub.domain.com/path`<br/>
### random agents
`python3 BlindCrawler.py -s https://sub.domain.com/path --random-agents`<br/>
### with cookies
`python3 BlindCrawler.py -s https://sub.domain.com/path -c "key: value; key:value"`<br/>
# Features
![Runtime](https://github.com/AhmedConstant/ImagesV/blob/master/blindcrawler-output.png)
* Process
 * Crawle the subdomains to expand the discovery surface.
 * Crawle /robot.txt for more URLs to crawle.
 * Crawle /sitemap.xml for more URLs to crawle.
 * Use web archive CDX API to get more URLs to crawle.
* Output
  * A file with all **crawled** URLs
  * A file with all **paths** crawled
  * A file with **subdomains** discovered.
  * A file with **schemes** discovered.
  * A file with **emails** discovered.
  * a file with **comments** discovered
* Performance
  * There will be a continuous process **to make performance as fast as possible** 
* Design
  * **OOP** Design
  * Good **Documentation**.
  * **Easy to edit** the script code
# To-Do List
- [x] ~~Relase beta version.~~
- [ ] Output in JSON, XML and CSV formats.
- [ ] Bruteforce for the sensitive files and directories.
- [ ] Extract **strings with high entropy** from crawled pages. [UUID, Key..etc]
- [ ] Recognize the **static/repetitive** Urls to avoid crawling it & reduce time and resources.
- [ ] Let the user provide its own **pattern** to extract from crawled pages.
- [ ] Create a **custom wordlist** for directory bruteforcing.
- [ ] Search for potential **DOM XSS** vulnerable functions.
- [ ] **Fuzzing** the GET Parameters.
- [ ] .....
# The Author
Ahmed Constant
[Twitter](https://twitter.com/a_Constant_)
