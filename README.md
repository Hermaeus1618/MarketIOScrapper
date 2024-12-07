# MARKETINOUT PATTERN SCRAPPER

A simple scrapper to get stock patterns from MARKETINOUT https://www.marketinout.com.
Scrapper is made using asyncio to get most speed possible from server.
Number of concurrent requests is limited by `Semaphore`, one can change its value to own needs but higher values are susceptible to timeout errors.
