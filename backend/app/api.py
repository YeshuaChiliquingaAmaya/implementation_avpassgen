
# ----------------------------------------------------
# Archivo: app/api.py
# ----------------------------------------------------
from fastapi import APIRouter, HTTPException
from .schemas import GenerationRequest, GenerationResponse

# Importa las funciones y excepciones de la librería avpassgen INSTALADA
# Esto funcionará porque instalaste la versión 0.1.1 (o superior)
from avpassgen import generate_passwords, AvPassGenConfig, LowEntropyError, CaptureError

# Crea un 'router'. Esto ayuda a organizar los endpoints en aplicaciones grandes.
router = APIRouter(
    prefix="/v1",
    tags=["Password Generation"]
)

@router.post("/generate", response_model=GenerationResponse)
async def generate_password_endpoint(request: GenerationRequest):
    """
    Endpoint para generar contraseñas seguras.
    Recibe una configuración y devuelve una lista de contraseñas.
    """
    try:
        # 1. Convierte el modelo de la solicitud (Pydantic) a la configuración
        #    que espera la librería avpassgen.
        config = AvPassGenConfig(
            duration_s=request.duration,
            use_video=request.use_video,
            use_audio=request.use_audio,
        )

        # 2. Llama a la función principal de la librería con los parámetros.
        passwords = generate_passwords(
            length=request.length,
            count=request.count,
            charset=request.charset,
            cfg=config
        )
        
        # 3. Devuelve la respuesta exitosa.
        return {"passwords": passwords}

    # 4. Manejo de errores específicos de la librería.
    except LowEntropyError as e:
        # Si la librería detecta que no hay suficiente aleatoriedad.
        raise HTTPException(
            status_code=400, # Bad Request
            detail=f"Error de Entropía: {e}. Intenta moverte o hacer ruido durante la captura."
        )
    except CaptureError as e:
        # Si la librería no puede acceder a la cámara o al micrófono.
        raise HTTPException(
            status_code=503, # Service Unavailable
            detail=f"Error de Captura: {e}. Asegúrate de que la cámara/micrófono no estén en uso por otra aplicación."
        )
    except Exception as e:
        # Captura cualquier otro error inesperado.
        raise HTTPException(
            status_code=500, # Internal Server Error
            detail=f"Ha ocurrido un error interno inesperado: {e}"
        )
