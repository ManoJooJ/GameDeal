import json, os, itertools

BASE = os.path.join(os.path.dirname(__file__), "data")
GAMES_FILE = os.path.join(BASE, "games.json")
USERS_FILE = os.path.join(BASE, "users.json")

os.makedirs(BASE, exist_ok=True)

DEFAULT_GAMES = [
    {"id":1,"nome":"Resident Evil Requiem","genero":"Terror","score":9.4,"ano":2026,"plat":"PC · PS5 · Xbox",
     "descricao":"O nono capítulo da saga Resident Evil. Uma nova protagonista enfrenta o terror em cenários devastados por um novo vírus.",
     "imagem":"https://cdn.cloudflare.steamstatic.com/steam/apps/3764200/header.jpg","destaque":True,
     "precos":{"steam":249.90,"nuuvem":219.90,"epic":None}},
    {"id":2,"nome":"Elden Ring","genero":"RPG","score":9.8,"ano":2022,"plat":"PC · PS · Xbox",
     "descricao":"Explore um vasto mundo aberto em um RPG de ação desafiador criado por FromSoftware.",
     "imagem":"https://cdn.cloudflare.steamstatic.com/steam/apps/1245620/header.jpg","destaque":True,
     "precos":{"steam":249.90,"nuuvem":134.90,"epic":None}},
    {"id":3,"nome":"Hollow Knight","genero":"Indie","score":9.5,"ano":2017,"plat":"PC · Switch",
     "descricao":"Explore um reino subterrâneo de insetos e heróis neste metroidvania desafiador.",
     "imagem":"https://cdn.cloudflare.steamstatic.com/steam/apps/367520/header.jpg","destaque":False,
     "precos":{"steam":15.99,"nuuvem":None,"epic":None}},
    {"id":4,"nome":"The Witcher 3","genero":"RPG","score":9.7,"ano":2015,"plat":"PC · PS · Xbox",
     "descricao":"Um RPG de mundo aberto épico com escolhas morais e uma história envolvente.",
     "imagem":"https://cdn.cloudflare.steamstatic.com/steam/apps/292030/header.jpg","destaque":False,
     "precos":{"steam":None,"nuuvem":29.99,"epic":29.99}},
    {"id":5,"nome":"Hades","genero":"Indie","score":9.6,"ano":2020,"plat":"PC · Switch",
     "descricao":"Um roguelike de ação frenético onde você escapa do submundo grego.",
     "imagem":"https://cdn.cloudflare.steamstatic.com/steam/apps/1145360/header.jpg","destaque":True,
     "precos":{"steam":37.99,"nuuvem":29.90,"epic":None}},
    {"id":6,"nome":"GTA V","genero":"Ação","score":9.0,"ano":2013,"plat":"PC · PS · Xbox",
     "descricao":"O crime organizado de Los Santos com modo online massivo.",
     "imagem":"https://cdn.cloudflare.steamstatic.com/steam/apps/271590/header.jpg","destaque":False,
     "precos":{"steam":39.99,"nuuvem":None,"epic":None}},
]

def _load_games():
    if not os.path.exists(GAMES_FILE):
        _save_games(DEFAULT_GAMES)
        return DEFAULT_GAMES
    with open(GAMES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _save_games(games):
    with open(GAMES_FILE, "w", encoding="utf-8") as f:
        json.dump(games, f, ensure_ascii=False, indent=2)

def get_all():
    return _load_games()

def get_by_id(game_id):
    return next((g for g in _load_games() if g["id"] == game_id), None)

def get_destaques():
    return [g for g in _load_games() if g.get("destaque")]

def create(data):
    games = _load_games()
    data["id"] = max((g["id"] for g in games), default=0) + 1
    games.append(data)
    _save_games(games)
    return data

def update(game_id, data):
    games = _load_games()
    for i, g in enumerate(games):
        if g["id"] == game_id:
            games[i].update(data)
            _save_games(games)
            return games[i]
    return None

def delete(game_id):
    games = [g for g in _load_games() if g["id"] != game_id]
    _save_games(games)

def _load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def get_user(username):
    return _load_users().get(username)

def user_exists(username):
    return username in _load_users()

def create_user(username, email, password, is_admin=False):
    users = _load_users()
    users[username] = {"email": email, "password": password, "avatar": "", "is_admin": is_admin}
    _save_users(users)

def update_user(username, data):
    users = _load_users()
    if username in users:
        users[username].update(data)
        _save_users(users)