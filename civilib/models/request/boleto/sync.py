from pydantic import BaseModel


class SyncBoletoModel(BaseModel):
    nossoNumero: int
