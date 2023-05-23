# Google_Maps_scrapper
Scrapping google maps using selenium to extract all adresses, longitudes, latitudes of a place

# Requirements:
Python 3.10.11
selenium

# Example:
def main():
    
    mScraper = MapsScraper()
    print(mScraper.get_address())

if __name__ == "__main__":
    main()
