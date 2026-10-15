# Guía de Nimbus Weather API

Documento ficticio para pruebas RAG.

## 1. Autenticación
Todas las solicitudes, excepto GET /status, requieren el encabezado X-API-Key. No envíes claves en la URL.

## 2. Pronóstico diario
Endpoint: GET /v1/forecast/daily?city={city}&days={days}
El parámetro days acepta valores entre 1 y 7. El valor predeterminado es 3. Un valor inválido devuelve 400 INVALID_DAYS.

## 3. Límites de uso
El plan de demostración admite 60 solicitudes por minuto por clave y 10.000 solicitudes por día. Si se excede el límite, devuelve 429 RATE_LIMIT_EXCEEDED. Respeta Retry-After si está presente.

## 4. Estado del servicio
GET /status no requiere autenticación. Los estados posibles son operational, degraded y unavailable.

## 5. Errores
- 400 INVALID_PARAMETER: parámetro ausente o incorrecto.
- 401 INVALID_API_KEY: clave ausente o inválida.
- 403 INSUFFICIENT_SCOPE: permisos insuficientes.
- 404 LOCATION_NOT_FOUND: ciudad no encontrada.
- 429 RATE_LIMIT_EXCEEDED: límite de solicitudes superado.
- 503 FORECAST_TEMPORARILY_UNAVAILABLE: pronóstico temporalmente no disponible.

## 6. Preguntas para evaluar el RAG
1. ¿Cuántos días permite el pronóstico?
2. ¿Qué encabezado se utiliza para autenticar?
3. ¿Qué significa el error 429?
4. ¿Qué endpoint no requiere autenticación?
5. ¿Cuál es el límite diario de solicitudes?
6. ¿Qué ocurre si se consulta una ciudad inexistente?

## 7. Preguntas sin respuesta
- ¿Cuál es el precio del plan empresarial?
- ¿Quién fundó NimbusLab?
- ¿Qué algoritmo utiliza el sistema?

La información de esta guía es ficticia y no describe un servicio real.