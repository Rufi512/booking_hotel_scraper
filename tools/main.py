




import  argparse
import logging
import threading


from scraper import scrapperHandler




def main(url:str):
    hotel = scrapperHandler.BookingScrapperHandler(url)

    hotel_id,response_rooms = hotel._scrapper_hotel()

    hotel._room_save(url=url, hotel_id=hotel_id, response_rooms=response_rooms)
    hotel._review_save(url=url,hotel_id=hotel_id)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description ='enter a URL to run the scraping. example: python scraper.py https://www.booking.com/hotel/cl/ibis-budget-providencia.en-gb.html?',
        usage='%(prog)s [options] URL',
        epilog='Enjoy the program! :)'
    )

    # Add the arguments
    parser.add_argument('URL',
                       metavar='URL',
                       type=str,
                       help='the url to list')

    args = parser.parse_args()

    input_path:str = args.URL

    main(input_path)