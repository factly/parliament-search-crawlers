from scrapy.cmdline import execute

try:
    execute(
        [
            'scrapy',
            'crawl',
            'ls_members_details'
        ]
    )
except SystemExit:
    pass