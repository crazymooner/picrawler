from optparse import OptionParser
from datetime import datetime, timedelta, date
from subprocess import call

def get_options():
    parser = OptionParser()
    parser.add_option('-p', '--path', dest='path', action='store',
                      help='store path')
    parser.add_option('-d', '--date', dest='date', action='store',
                      default=date.today().strftime("%Y-%m-%d") ,help='crawl date')
    opts, args = parser.parse_args()
    return opts

def newsETL(options):
    if options.path == None:
        print "path is needed, use -p option"
        return
    call("mkdir " + options.path + options.date, shell=True)
    call("cd /home/pi314/workspace/picrawler && /home/pi314/anaconda/bin/scrapy crawl pimain -a path=" + options.path  + options.date + 
         "/ -a crawlDate=" + options.date, shell=True)
if __name__ == '__main__':
    newsETL(get_options())