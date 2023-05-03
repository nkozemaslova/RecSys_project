from pydantic import BaseModel
from typing import Optional, List

# Users
class CreateAndUpdateUser(BaseModel):
    USER_ID : int
    UserName : str

class User(CreateAndUpdateUser):
    USER_ID: int

    class Config:
        orm_mode = True

class PaginatedUserInfo(BaseModel):
    limit: int
    offset: int
    data: List


# Songs
class CreateAndUpdateSong(BaseModel):
    SONG_ID : int
    Title : str
    ARTIST_ID : int
    GANRE_ID : int

class Song(CreateAndUpdateSong):
    SONG_ID: int

    class Config:
        orm_mode = True 

class PaginatedSongInfo(BaseModel):
    limit: int
    offset: int
    data: List

# Artists
class CreateAndUpdateArtist(BaseModel):
    ARTIST_ID : int
    ArtistName : str
    GANRE_ID : int

class Artist(CreateAndUpdateArtist):
    ARTIST_ID: int

    class Config:
        orm_mode = True 

class PaginatedArtistInfo(BaseModel):
    limit: int
    offset: int
    data: List


# Ganres
class CreateAndUpdateGanre(BaseModel):
    GANRE_ID : int
    GanreName : str

class Ganre(CreateAndUpdateGanre):
    GANRE_ID: int

    class Config:
        orm_mode = True 

class PaginatedGanreInfo(BaseModel):
    limit: int
    offset: int
    data: List

# Interactions
class CreateAndUpdateInteraction(BaseModel):
    INTERACTION_ID : int
    USER_ID : int
    SONG_ID : int
    Score : int

class Interaction(CreateAndUpdateInteraction):
    INTERACTION_ID : int

    class Config:
        orm_mode = True 

class PaginatedInteractionInfo(BaseModel):
    limit: int
    offset: int
    data: List
