import sqlite3
from sqlite3 import Error
from sqlite3.dbapi2 import Connection

class DbInterface:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        print("SQLite {} connection estalished".format(sqlite3.version))

    def inititialize_database(self):
        #popularity no yet implemented, but refers to how often this URL is cited in other pages
        #quality isn yet implemented and might never be
        create_url_table = """CREATE TABLE IF NOT EXISTS urls (
            url text PRIMARY KEY,
            popularity integer NOT NULL,
            quality real NOT NULL
        )"""
        #popularity still isn't implemented but might be interesting, as less common words should tend to be more important for the search engine
        #for example "python" and "OCR" are likely way less common than "and", but in a search for "learning python and ocr" the "and" is pretty meaningless
        create_word_table = """CREATE TABLE IF NOT EXISTS words (
            word text PRIMARY KEY,
            popularity integer NOT NULL
        )"""
        #importance does nothing for now, the idea is that maybe sometimes a word coming up in keywords might be more important
        #than being in description (just example) and this could be expressed by raising and lowering importance
        create_content_table = """CREATE TABLE IF NOT EXISTS contents (
            url text NOT NULL,
            word text NOT NULL,
            importance integer NOT NULL,
            PRIMARY KEY (url, word)
        )"""

        c = self.connection.cursor()
        c.execute(create_url_table)
        c.execute(create_word_table)
        c.execute(create_content_table)

    def insert_data(self, words, url, links):
        insert_url = """INSERT OR IGNORE INTO urls(url, popularity, quality) VALUES (?, 0, 1.0)"""
        insert_word = """INSERT OR IGNORE INTO words(word, popularity) VALUES (?, 1)"""
        insert_content = """INSERT INTO contents(url, word, importance) VALUES (?, ?, 1)"""
        update_url_popularity = """UPDATE urls SET popularity = popularity + 1 WHERE url = ?"""

        c = self.connection.cursor()
        c.execute(insert_url, [url])
        for word in words:
            c.execute(insert_word, [word])
            c.execute(insert_content, (url, word))
        for link_url in links:
            c.execute(insert_url, [link_url])
            c.execute(update_url_popularity, [link_url])
        self.connection.commit()

    #TODO figure out how to do this shit without violating threads
    #def __del__(self):
    #    if self.connection.:
    #        self.connection.close()