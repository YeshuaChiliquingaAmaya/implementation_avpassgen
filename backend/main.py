# ----------------------------------------------------
# Archivo: main.py
# ----------------------------------------------------
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router as api_router

# Crea la instancia de la aplicación FastAPI
app = FastAPI(
    title="avpassgen API",
    description="Una API web para generar contraseñas usando entropía de audio/video.",
    version="1.0.0"
)

# Configuración de CORS (Cross-Origin Resource Sharing)
# Esto permite que tu frontend (que se ejecuta en un dominio diferente)
# pueda comunicarse con este backend.
# Para producción, es más seguro restringir los orígenes.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todas las cabeceras
)

# Incluye el router de la API que definimos en app/api.py
app.include_router(api_router, prefix="/api")

# Un endpoint raíz simple para verificar que la API está funcionando
@app.get("/", tags=["Root"])
def read_root():
    """Endpoint raíz para verificar el estado de la API."""
    return {"message": "Bienvenido a la API de avpassgen. Visita /docs para la documentación."}
