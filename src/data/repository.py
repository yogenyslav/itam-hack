import abc
from pydantic import BaseModel


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, obj: BaseModel) -> BaseModel:
        raise NotImplementedError

    @abc.abstractclassmethod
    def get(self, **kwargs) -> BaseModel:
        raise NotImplementedError

    @abc.abstractclassmethod
    def delete(self, obj: BaseModel) -> None:
        raise NotImplementedError

    @abc.abstractclassmethod
    def update(self, obj: BaseModel) -> BaseModel:
        raise NotImplementedError

    @abc.abstractclassmethod
    def get_all(self, **kwargs) -> list:
        raise NotImplementedError
