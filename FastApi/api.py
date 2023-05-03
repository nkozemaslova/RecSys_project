from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv
from crud import get_all_users, get_all_songs, get_all_artists, get_all_ganres, get_all_interactions, get_user_song_list_by_id
from database import session
from exceptions import UserInfoException
from schema import PaginatedSongInfo, PaginatedUserInfo, PaginatedArtistInfo, PaginatedGanreInfo, PaginatedInteractionInfo

import logging

#
# Logging initialization
#
logging.basicConfig(level=logging.DEBUG)


router = APIRouter()


# Example of Class based view
@cbv(router)
class Users:

    # API to get the list of user info
    @router.get("/users", response_model=PaginatedUserInfo)
    def list_users(self, limit: int = 10, offset: int = 0):
        logging.info(f"list_users request")

        users_list = get_all_users(session, limit, offset)
        response = {"limit": limit, "offset": offset, "data": users_list}
        logging.info(f"list_users get {len(users_list)} records")

        return response
    
# API endpoint to get info of a particular car
@router.get("/users/{user_id}", response_model=PaginatedSongInfo)
def get_user_song_list(user_id, limit: int = 10, offset: int = 0):
    logging.info(f"get_user_song_list request")

    songs_list_info = get_user_song_list_by_id(session, user_id)
    response = {"limit": limit, "offset": offset, "data": songs_list_info}
    logging.info(f"get_user_song_list get {len(songs_list_info)} records")

    return response


@cbv(router)
class Songs:    

    # API to get the list of user info
    @router.get("/songs", response_model=PaginatedSongInfo)
    def list_songs(self, limit: int = 10, offset: int = 0):

        songs_list = get_all_songs(session, limit, offset)
        response = {"limit": limit, "offset": offset, "data": songs_list}

        return response
    
@cbv(router)
class Artists:    

    # API to get the list of user info
    @router.get("/artists", response_model=PaginatedArtistInfo)
    def list_artists(self, limit: int = 10, offset: int = 0):

        artists_list = get_all_artists(session, limit, offset)
        response = {"limit": limit, "offset": offset, "data": artists_list}

        return response
    
@cbv(router)
class Ganres:    

    # API to get the list of user info
    @router.get("/ganres", response_model=PaginatedGanreInfo)
    def list_ganres(self, limit: int = 10, offset: int = 0):

        ganres_list = get_all_ganres(session, limit, offset)
        response = {"limit": limit, "offset": offset, "data": ganres_list}

        return response
    
@cbv(router)
class Interations:    

    # API to get the list of user info
    @router.get("/interactions", response_model=PaginatedInteractionInfo)
    def list_interactions(self, limit: int = 10, offset: int = 0):

        interactions_list = get_all_interactions(session, limit, offset)
        response = {"limit": limit, "offset": offset, "data": interactions_list}

        return response