# TOP 3 posiciones Super Smash Bros Melee RD / LATAM
### Visualización
- https://lookerstudio.google.com/s/teR-2kyYej4

Se puede observar la siguiente información:
- Nombre del torneo
- Fecha del torneo
- Primeros 3 lugares
- Enlace del torneo

## Herramientas
- Acceso a API de [start.gg](https://www.start.gg/)
- Servidor Linux (Raspberry Pi 4 en este caso)
- Python
- Google Sheets
- Google Looker Studio

## Detalles
Proyecto automatizado que refresca los datos todos los lunes a través del API de [start.gg](https://www.start.gg/), Raspberry Pi 4, Google Sheets y Google Looker Studio.

Archivo Python [my_modules](/modules/my_modules.py) en [modules](/modules) contiene módulos a utilizar en el script principal como queries y credenciales en las clases _Melee_ y _Sheets_.

La clase _General_ contiene función para eliminar logs automáticamente de la carpeta [logs](/logs).

La carpeta [src](/src) contiene el [código fuente](/src/dr_tournaments.py) del proyecto, el [script para eliminar logs](/src/del_logs.py) automáticamente y el [shell script](/src/dr_tournaments.sh) para configurar el [crontab](/src/crontab.txt).

## Recursos adicionales
- [API de start.gg](https://developer.start.gg/docs/intro/)
- [Conexión de Python a Google Sheets](https://developers.google.com/sheets/api/quickstart/python)

## Anexo
![image](https://github.com/user-attachments/assets/87476384-b37a-4544-b174-558dd49e2492)

![image](https://github.com/user-attachments/assets/6bae1888-d1f6-47ff-aee0-330516cccc15)
