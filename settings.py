CURRENCY_STRING = '£$'
CRAWLER_SETTINGS = {
    # 1. Identify your bot responsibly (Change this to your project name/email)
    'USER_AGENT': 'ecommerce-price-monitor/1.0',
    
    # 2. Obey the site's robots.txt rules implicitly
    'ROBOTSTXT_OBEY': True,
    
    # 3. Configure a polite delay (2 seconds between requests to the same domain)
    'DOWNLOAD_DELAY': 10.0,
    
    # 4. Enable Scrapy's AutoThrottle extension
    # Dynamically adjusts crawling speed based on the target server's load
    'AUTOTHROTTLE_ENABLED': True,
    'AUTOTHROTTLE_START_DELAY': 5.0,  # Initial download delay
    'AUTOTHROTTLE_MAX_DELAY': 60.0,   # Maximum download delay in case of high latencies
    'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,  # Average number of requests Scrapy sends in parallel
    'REMOTE_CONTROL_ENABLED': False,

    # 5. Disable cookies to avoid tracking or session overhead
    'COOKIES_ENABLED': False,
    "ITEM_PIPELINES": {
        "pipelines.PostgreSQLPipeline": 300,
    },
}

