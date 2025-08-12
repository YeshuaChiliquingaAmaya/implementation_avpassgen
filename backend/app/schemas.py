
# ----------------------------------------------------
# Archivo: app/schemas.py
# ----------------------------------------------------
from pydantic import BaseModel, Field

class GenerationRequest(BaseModel):
    """
    Define la estructura y validación para las solicitudes de generación de contraseñas.
    Pydantic se encarga de validar que los datos entrantes cumplan con estas reglas.
    """
    length: int = Field(default=20, gt=7, le=128, description="Longitud de la contraseña (entre 8 y 128)")
    count: int = Field(default=1, gt=0, le=50, description="Cantidad de contraseñas a generar (entre 1 y 50)")
    duration: float = Field(default=2.0, gt=0.5, le=10.0, description="Segundos de captura de entropía (entre 0.5 y 10)")
    charset: str = Field(default="base64url", pattern="^(base64url|alnum|alnum\\+sym)$", description="Set de caracteres a usar")
    use_video: bool = Field(default=True, description="Indica si se debe usar la cámara para la entropía")
    use_audio: bool = Field(default=True, description="Indica si se debe usar el micrófono para la entropía")

class GenerationResponse(BaseModel):
    """
    Define la estructura de la respuesta exitosa.
    """
    passwords: list[str]
