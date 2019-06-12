from bs4 import BeautifulSoup
import requests
import re
import json
import timeit
import logging

actors = []
movies = []
actor_next_pages = []
movie_next_pages = []
scraped_actors = []
scraped_movies = []


def get_soup(url):
    """
    retrieves http-parsed web data from the specified url
    :param url: the specified url
    :return: http-parsed web data
    """
    response = requests.get("https://en.wikipedia.org"+url)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


def film_scape(start_url):
    """
    recursivee function that scrapes actor and movie pages
    :param start_url: url
    :return:
    """
    soup = get_soup(start_url)
    if soup.find("a", href="#Filmography"):
        actor_json = actor_scrape(soup)
        actor_name = json.loads(actor_json)["name"]
        if actor_name not in scraped_actors:
            actors.append(actor_json)
            scraped_actors.append(actor_name)
        else:
            film_scape(actor_next_pages.pop())

        if len(movie_next_pages) > 0 and len(actors) <= 250:
            print("movies", "actors", len(movies), len(actors))
            film_scape(movie_next_pages.pop())

    elif soup.find("a", href="#Cast"):
        movie_json = movie_scrape(soup)
        movie_name = json.loads(movie_json)["title"]
        if movie_name not in scraped_movies:
            movies.append(movie_json)
            scraped_movies.append(movie_name)
        else:
            film_scape(movie_next_pages.pop())
        if len(actor_next_pages) > 0 and len(actors) <= 250:
            print("movies", "actors", len(movies), len(actors))
            film_scape(actor_next_pages.pop())
    else:
        if len(movie_next_pages) > 0:
            film_scape(movie_next_pages.pop())
        elif len(actor_next_pages) > 0:
            film_scape(actor_next_pages.pop())
        else:
            print("fail")


def actor_scrape(soup):
    """
    scraps actor data from an actor page and jsonifies it
    :param soup: http-parsed web data
    :return: jsonified actor data
    """

    # Name
    name = soup.find("h1", {"id": "firstHeading"}).text

    # Age
    age = None
    infobox = soup.find("table", {"class": "infobox"})
    if infobox is not None:
        age_str = infobox.find("span", {"class": "noprint ForceAgeToShow"})
        if age_str is not None:
            age = int(age_str.text.split()[1].replace(")", ""))
    else:
        logging.warning("information box cannot be retrieved")
    # Films
    films = []
    filmography = soup.find_all("a", href=re.compile('\(film\)$'))
    for film in filmography:
        films.append(film['title'].replace(" (film)", ""))
        if film['href'] not in movie_next_pages:
            movie_next_pages.append(film['href'])
    if name is None:
        logging.warning("name cannot be retrieved")
    if age is None:
        logging.warning("age cannot be retrieved")
    if films is []:
        logging.warning("films cannot be retrieved")
    if name is not None and age is not None and films is not []:
        logging.info("Actor data is successfully retrieved")
    return json.dumps({"name": name, "age": age, "films": films})


def movie_scrape(soup):
    """
    scraps movie data from aa movie page and jsonifies it
    :param soup: http-parsed web data
    :return: jsonified movie data
    """

    # Title
    title = soup.find("h1", {"id": "firstHeading"}).text

    year = None
    grossing = None
    cast = []

    infobox = soup.find("table", {"class": "infobox"})
    if infobox is not None:
        # Year
        year_candidates = infobox.find_all("li")
        for c in year_candidates:
            if re.findall('\d{4}', c.text):
                year = c.text
        if year is None:
            year_candidate = infobox.find("td", text=re.compile('\d{4}'))
            if year_candidate is not None:
                year = year_candidate.text

        # Starring
        infobox_rows = infobox.find_all("tr")
        for infobox_row in infobox_rows:
            if infobox_row.find("th", text="Starring"):
                casts = infobox_row.find_all("a", attrs={"class": None})
                for c in casts:
                    cast.append(c.text)
                    actor_next_pages.append(c['href'])

        # Grossing
        for infobox_row in infobox_rows:
            if infobox_row.find("th", text="Box office"):
                grossing = infobox_row.find("td").text

    if title is None:
        logging.warning("title cannot be retrieved")
    if year is None:
        logging.warning("year cannot be retrieved")
    if cast is []:
        logging.warning("casts cannot be retrieved")
    if grossing is None:
        logging.warning("grossing cannot be retrieved")
    if title is not None and year is not None and cast is not [] and grossing is not None:
        logging.info("Movie data is successfully retrieved")

    return json.dumps({"title": title, "year": year, "cast": cast, "Grossing": grossing})


def main():
    start_time = timeit.default_timer()
    logging.basicConfig(filename='FilmScraper.log', level=logging.DEBUG, filemode='w')
    film_scape("/wiki/Morgan_Freeman")
    end_time = timeit.default_timer()
    print("Time taken to scrap data:", str(int(end_time - start_time)), "seconds")
    print("# of scraped actors", str(len(actors)))
    print("# of scraped movies", str(len(movies)))
    with open('movie_output.json', 'w') as filehandle:
        json.dump(movies, filehandle, indent=2)
    with open('actor_output.json', 'w') as filehandle:
        json.dump(actors, filehandle, indent=2)


if __name__ == "__main__":
    main()
