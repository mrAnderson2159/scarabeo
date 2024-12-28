from src.database import Database
from src.exceptions import NotFoundErr

class BaseModel:
    @classmethod
    def _load_data(cls) -> dict:
        """Carica il database."""
        return Database.load()

    @classmethod
    def _save_data(cls, data: dict):
        """Salva il database."""
        Database.save(data)

    @classmethod
    def _get_entities(cls, key: str) -> list[dict]:
        """Restituisce la lista delle entità specificata."""
        data = cls._load_data()
        return data[key]

    @classmethod
    def _save_entities(cls, key: str, entities: list[dict]):
        """Salva le entità specificate nel database."""
        data = cls._load_data()
        data[key] = entities
        cls._save_data(data)

    @classmethod
    def get_entity(cls, key: str, entities_key: str, value):
        """Trova un'entità in base a una chiave."""
        entities = cls._get_entities(entities_key)
        for entity in entities:
            if entity[key] == value:
                return entity
        raise NotFoundErr(f"{cls.__name__} with {key}={value} not found")

    @classmethod
    def next_id(cls, entities_key: str) -> int:
        """Calcola il prossimo ID disponibile."""
        entities = cls._get_entities(entities_key)
        return max((e["id"] for e in entities), default=0) + 1

    @classmethod
    def all(cls, entities_key: str, model_class) -> list:
        """Restituisce tutte le istanze della classe specificata."""
        entities = cls._get_entities(entities_key)
        return [model_class(**entity) for entity in entities]

    @classmethod
    def create(cls, entities_key: str, model_class, **kwargs) -> object:
        """Crea una nuova istanza e la aggiunge al database."""
        entities = cls._get_entities(entities_key)
        new_id = cls.next_id(entities_key)
        entity = {"id": new_id, **kwargs}
        entities.append(entity)
        cls._save_entities(entities_key, entities)
        return model_class(**entity)

    @classmethod
    def update_entity(cls, entities_key: str, id_key: str, id_value, update_key: str, update_value):
        """Aggiorna un'entità specifica."""
        entities = cls._get_entities(entities_key)
        for entity in entities:
            if entity[id_key] == id_value:
                entity[update_key] = update_value
                break
        else:
            raise ValueError(f"Entity with {id_key}={id_value} not found")
        cls._save_entities(entities_key, entities)



class Player(BaseModel):
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    @classmethod
    def all(cls) -> list["Player"]:
        return cls.all("players", cls)

    @classmethod
    def get(cls, id: int) -> "Player":
        entity = cls.get_entity("id", "players", id)
        return cls(**entity)

    @classmethod
    def get_by_name(cls, name: str) -> "Player":
        entity = cls.get_entity("name", "players", name)
        return cls(**entity)


    @classmethod
    def create(cls, name: str) -> "Player":
        return cls.create("players", cls, name=name)

    @classmethod
    def rename(cls, id: int, new_name: str) -> "Player":
        cls.update_entity("players", "id", id, "name", new_name)
        return cls.get(id)

    @staticmethod
    def get_ids(players: list["Player"]) -> list[int]:
        return [player.id for player in players]

class PlayerSet(BaseModel):
    def __init__(self, id: int, player_ids: list[int]):
        self.id = id
        self.player_ids = player_ids

    @classmethod
    def all(cls) -> list["PlayerSet"]:
        return cls.all("player_sets", cls)

    @classmethod
    def get(cls, id: int) -> "PlayerSet":
        entity = cls.get_entity("id", "player_sets", id)
        return cls(**entity)

    @classmethod
    def create(cls, player_ids: list[int]) -> "PlayerSet":
        return cls.create("player_sets", cls, player_ids=player_ids)

    def get_players(self) -> list[Player]:
        return [Player.get(id) for id in self.player_ids]


class Game(BaseModel):
    def __init__(self, id: int, time: str, player_scores: list[dict[str, int]]):
        self.id = id
        self.time = time
        self.player_scores = player_scores

    @classmethod
    def all(cls) -> list["Game"]:
        return cls.all("games", cls)

    @classmethod
    def get(cls, game_id: int) -> "Game":
        entity = cls.get_entity("id", "games", game_id)
        return cls(**entity)

    @classmethod
    def create(cls, time: str, player_scores: list[dict[str, int]]) -> "Game":
        return cls.create("games", cls, time=time, player_scores=player_scores)

    def add_score(self, player_id: int, points: int):
        """Aggiorna i punteggi dei giocatori in una partita."""
        # Aggiorna i punteggi nella lista interna
        for score in self.player_scores:
            if score["player_id"] == player_id:
                score["points"] += points
                break
        else:
            self.player_scores.append({"player_id": player_id, "points": points})

        # Salva l'aggiornamento nel database
        entities_key = "games"
        id_key = "id"
        BaseModel.update_entity(
            entities_key,
            id_key,
            self.id,
            "player_scores",
            self.player_scores
        )
