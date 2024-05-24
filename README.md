# restaurant-information
Prueba técnica para vacante de BackEnd
Proyecto realizado en Python con Flask.
Parar poder ejecutar el Proyecto se necesita tener instalado Python 3.12.3 y realizar las siguientes instalaciones:
- pip install flask, mysql-connector-python, pandas

El proyecto es un CRUD básico el cual cuenta con las siguientes URL para las peticiones:
- /create_restaurant: Permite crear un nuevo restaurant.
- /read_restaurant: Permite leer toda la lista de restaurantes agregados en la BD.
- /update_restaurant/{id}: Permite actualizar la información de un restaurante por medio de la id.
- /delete_restaurant/{id}: Permite eliminar algún restaurante por meedio de la id.
- /import_restaurant: Permite importar desde un archivo con extensión .csv la información de los restaurantes.
- /restaurants/statistics?latitude=x&longitude=y&radius=z: Permite encontrar los restaurantes desde una geolocalización.
