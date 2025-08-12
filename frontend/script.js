document.addEventListener('DOMContentLoaded', () => {
    // Definimos la URL base de tu API
    const API_BASE_URL = 'https://back-pass-3v90.onrender.com'; // ¡Esta es la URL correcta para tu backend desplegado!
    const FORM = document.getElementById('passwordForm');
    const STATUS_MESSAGE_DIV = document.getElementById('statusMessage');
    const PASSWORD_LIST_UL = document.getElementById('passwordList');
    
    // Función para mostrar mensajes de estado
    function showStatusMessage(message, type) {
        STATUS_MESSAGE_DIV.textContent = message;
        STATUS_MESSAGE_DIV.className = `status-message ${type}`;
        STATUS_MESSAGE_DIV.style.display = 'block';
    }

    // Oculta el mensaje de estado después de un tiempo
    function hideStatusMessage() {
        setTimeout(() => {
            STATUS_MESSAGE_DIV.style.display = 'none';
        }, 5000); // 5 segundos
    }

    // Función para manejar el envío del formulario
    FORM.addEventListener('submit', async (event) => {
        event.preventDefault(); // Evita que el formulario se envíe de la forma tradicional

        // 1. Ocultamos mensajes anteriores y limpiamos la lista
        showStatusMessage('Generando contraseñas...', 'success');
        PASSWORD_LIST_UL.innerHTML = '';
        
        // 2. Recolectamos los datos del formulario
        const formData = {
            length: parseInt(document.getElementById('length').value),
            count: parseInt(document.getElementById('count').value),
            duration: parseFloat(document.getElementById('duration').value),
            charset: document.getElementById('charset').value,
            use_video: document.getElementById('use_video').checked,
            use_audio: document.getElementById('use_audio').checked
        };
        
        try {
            // 3. Hacemos la solicitud POST a la API
            const response = await fetch(`${API_BASE_URL}/api/v1/generate`, { // ¡Nota: "/api" aquí si tu router está prefijado!
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            // 4. Manejamos la respuesta de la API
            if (response.ok) {
                const data = await response.json();
                
                // Limpiamos la lista y agregamos las nuevas contraseñas
                data.passwords.forEach(password => {
                    const li = document.createElement('li');
                    li.textContent = password;
                    PASSWORD_LIST_UL.appendChild(li);
                });

                showStatusMessage('Contraseñas generadas con éxito.', 'success');

            } else {
                // Si la respuesta no es exitosa (ej. 400, 500, etc.)
                const errorData = await response.json();
                showStatusMessage(`Error: ${errorData.detail}`, 'error');
            }
        } catch (error) {
            // 5. Manejamos errores de red o del servidor
            console.error('Error de red o de la solicitud:', error);
            showStatusMessage('Error de conexión con la API. Asegúrate de que el servidor esté corriendo.', 'error');
        }

        hideStatusMessage();
    });
});