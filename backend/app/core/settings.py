from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AZURE_STORAGE_CONNECTION_STRING: str = ""
    CONTAINER_INPUTS: str = "cloudkit-inputs"
    ADMIN_BLOB_PATH: str = "kode_kloud/root/KodeKloud2025Admin.xlsx"
    ACTIVITY_BLOB_PATH: str = "kode_kloud/root/activity_leaderboard.xlsx"
    JSON_BLOB_PATH: str = "kode_kloud/root/kodekloud_data.json"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
