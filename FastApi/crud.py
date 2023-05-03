# crud.py
from typing import List
from exceptions import UserInfoInfoAlreadyExistError, UserInfoNotFoundError
from model import Users, Songs, Artists, Ganres, Interactions

import logging

#
# Logging initialization
#
logging.basicConfig(level=logging.DEBUG)

# Function to get list of user info
def get_all_users(session, limit: int, offset: int):
    logging.info(f"crud get_all_users requests")
    return session.query(Users).offset(offset).limit(limit).all()

def get_user_song_list_by_id(session, _id: int):
    user_song_list = session.query(Interactions, Users, Songs, Artists, Ganres) \
        .join(Users, Users.USER_ID == Interactions.USER_ID) \
        .join(Songs, Songs.SONG_ID == Interactions.SONG_ID) \
        .join(Artists, Artists.ARTIST_ID == Songs.ARTIST_ID) \
        .join(Ganres, Ganres.GANRE_ID == Songs.GANRE_ID) \
        .with_entities(Users.UserName, Songs.Title, Artists.ArtistName, Ganres.GanreName) \
        .filter(Users.USER_ID == _id).all()
    logging.info(f"crud get_user_song_list_by_id requests")

    return user_song_list

# Function to get list of user info
def get_all_users(session, limit: int, offset: int) -> List[Users]:
    return session.query(Users).offset(offset).limit(limit).all()

def get_all_songs(session, limit: int, offset: int):
    return session.query(Songs, Artists, Ganres) \
        .join(Artists, Artists.ARTIST_ID == Songs.ARTIST_ID) \
        .join(Ganres, Ganres.GANRE_ID == Songs.GANRE_ID) \
        .with_entities(Songs.Title, Artists.ArtistName, Ganres.GanreName) \
        .offset(offset).limit(limit).all()

def get_all_artists(session, limit: int, offset: int) -> List[Artists]:
    return session.query(Artists).offset(offset).limit(limit).all()

def get_all_ganres(session, limit: int, offset: int) -> List[Ganres]:
    return session.query(Ganres).offset(offset).limit(limit).all()

def get_all_interactions(session, limit: int, offset: int):
    return session.query(Interactions, Users, Songs, Artists, Ganres) \
        .join(Users, Users.USER_ID == Interactions.USER_ID) \
        .join(Songs, Songs.SONG_ID == Interactions.SONG_ID) \
        .join(Artists, Artists.ARTIST_ID == Songs.ARTIST_ID) \
        .join(Ganres, Ganres.GANRE_ID == Songs.GANRE_ID) \
        .with_entities(Users.UserName, Songs.Title, Artists.ArtistName, Ganres.GanreName) \
        .offset(offset).limit(limit).all()
