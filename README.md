# Instrucciones de instalación

Existen dos aplicaciones distintas:
1. El script importer.py que se lanza de forma habitual
1. La aplicación flask del API

Para la aplicación flask se incluye en el proyecto la configuración de lanzamiento desde Visual Studio Code.

# Uso

1. Importar datos desde csv a bbdd mediante el script independiente importer.py. Siempre se borrarán todos los registros que hubiera previamente.
2. Lanzar la aplicación flask
3. Pedir al API flask un token válido para nuestro usuario mediante el comando:

`curl -X POST -H "Content-Type: application/json" http://localhost:5000/auth -d '{ "username": "user1", "password": "qwerty" }'`
    
    Existen dos usuarios válidos:
        1. user1 / qwerty
        2. user2 / asdfgh
    
    La respuesta de esta llamada es similar a:
    
`{"access_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTQ0MDI0ODMsImlhdCI6MTU5NDQwMjE4MywibmJmIjoxNTk0NDAyMTgzLCJpZGVudGl0eSI6MX0.HUGH0MgdyQIdsx4AKYULiIjGxqFDLVEDYDliFgxuLwA"}`

4. Hacer las llamadas al api usando el Token generado en el paso anterior. Ejemplos de llamadas son:

`curl --location --request GET 'http://localhost:5000/customers/CMA-095-A/active_power/2019-08-01-00:00:00/2019-08-01-02:15:00' --header 'Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTQ0MDI0ODMsImlhdCI6MTU5NDQwMjE4MywibmJmIjoxNTk0NDAyMTgzLCJpZGVudGl0eSI6MX0.HUGH0MgdyQIdsx4AKYULiIjGxqFDLVEDYDliFgxuLwA'`

`curl --location --request GET 'http://localhost:5000/customers/CMA-095-A/energy_consumption/2019-08-01-00:00:00/2019-08-01-02:15:00' --header 'Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTQ0MDI0ODMsImlhdCI6MTU5NDQwMjE4MywibmJmIjoxNTk0NDAyMTgzLCJpZGVudGl0eSI6MX0.HUGH0MgdyQIdsx4AKYULiIjGxqFDLVEDYDliFgxuLwA'`

`curl --location --request GET 'http://localhost:5000/customers/CMA-095-A/current_month_status' --header 'Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTQ0MDI0ODMsImlhdCI6MTU5NDQwMjE4MywibmJmIjoxNTk0NDAyMTgzLCJpZGVudGl0eSI6MX0.HUGH0MgdyQIdsx4AKYULiIjGxqFDLVEDYDliFgxuLwA'`

5. Existen 3 endpoints que responden a las 3 zonas marcadas en la siguiente imagen:

![Dashboard with endpoints](dashboard.jpg)

# Decisiones técnicas

## General
- Creación de un entorno virtual para aislar el desarrollo de dependencias no deseadas.
- Creación de un módulo monitoring para separar el API de la utilidad de carga de csv.

## Carga de datos desde csv
- Se crean las clases CsvReader y Store para separar conceptos y respetar el principio SOLID de Responsaliddad Única.
- Se usa Pandas para leer csv
- Se usa sqlite3 para persistir los datos debido a que puede distribuirse sin problemas, es ligera y de un rendimiento decente para pequeños desarrollos.

## API
- Autenticación mediante JWT. Es un API, sin estado y es una manera segura de hacerlo.
- El token de autenticación JWT se encuentra en el header de cada petición. Importante: El prefijo de autorización es JWT.
- Al ser peticiones de lectura se obliga a usar siempre métodos GET a excepción del endpoint de autenticación que es POST (ver sección Uso).
- Se considera que el dashboard mostrado pertenece a un cliente con identificador CMA-095-A
- Se usa un decorador(@customer_exists) para validar si el cliente existe siguiendo el principio DRY. Si no existe, se aborta la ejecución devolviendo un 404 y mensaje de error en formato json
- Se considera que el formato de fechas puede ser distinto en la request y como está almacenada en base de datos. La fecha se almacena en base de datos tal cual aparece en el csv
- Se usa un decorador(@validate_date) para validar las fechas del request. Además, este decorador las transforma al formato de base de datos.
- Se usa como una extensión de flask como sistema de caché, Flask-Caching. Configurado en su versión simple que puede funcionar standalone. Cada endpoint tiene una caché de duración 10s. Si se hace la misma petición dentro de ese tiempo, el resultado sale de la caché, no de base de datos.

# Siguientes pasos de mejoras

- Una base de datos documental como MondoDB puede ser más adecuada para almacenar este tipo de datos.
- Almacenar los usuarios autorizados en base de datos (distinta de los datos de monitorización) La gestión de usuarios debería sacarse a un sistema/servicio diferente.
- Almacenar los clientes en base de datos y asociarle los datos del csv
- En estos momentos, se devuelven resultados directamente de la base de datos. Es importante crear nuevos modelos para hacerlo.


