from fastapi import FastAPI

app = FastAPI()


class Soundtrack:
    def __init__(self, name: str, author: str, track_length: int,
                 listens: int, genres: list | tuple, album: str | None = None):
        self.name = name
        self.author = author
        self.track_length = track_length
        self.listens = listens
        self.genres = genres
        self.album = album


data = [Soundtrack('Aria 5', 'Joe Fofo', 121, 40175, ['rock']),
        Soundtrack('Cake Song', 'Untalanted baker', 307, 23, ['pop', 'rap'], 'Void'), ]


@app.get('/')
def index():
    return {'test': 'Hello World!'}


@app.get('/music/get')
def read():
    return data


@app.get('/music/get/{track_id}')
def read_all(track_id: int):
    return data[track_id]
