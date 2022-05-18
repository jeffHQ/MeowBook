# MeowBook
Collaborative platform-based development project
    <h1>MeowBook</h1>
    <h3>Integrantes:</h3>
    <ul>
        <li>Ruiz de Somocurcio Landa, Cristóbal</li>
        <li>Camacho Valencia, Aaron Arturo</li>
        <li>Vásquez de Velasco Gonzales Vigil, Rodrigo</li>
        <li>Hilario Quintana, Jeffry Arturo</li>
    </ul>
    <h3>Descripción del proyecto:</h3>
    <p>Meow Book es un repositorio de libros en el cual los usuarios (si lo desean) pueden agregar libros
        que les interesan y datos de este como autor, editorial sinopsis, etc. Otros usuarios pueden modificar
        la información libremente para finalemente encontrarlos con ayuda de una barra de busqueda.
    </p>
    <h3>Objetivos principales/Misión/Visión:</h3>
    <p><strong>Objetivo principal:</strong> Brindar un plataforma web en la cual las personas puedan compartir
        los libros que más les gusten, su reseñas y promover la lectura de una manera curiosa e innovadora
        dando la libertad a los usuarios de modificarlo todo :D.
    </p>
    <p><strong>Misión:</strong> Promo
        Promover la lectura y el respeto de opinión entre los lectores de nuestra página dando plena libertad a modificar las
        obras de los demás, esperando que se logre una convivencia adecuada por medio de los usuarios que entren a nuestra página.
    </p>
    <p><strong>Visión:</strong> Nuestra visión es desarrollar una comunidad de lectores que motivados por descubrir
        y compartir se retroalimenten dando recomendaciones entre ellos. Esperando finalmente que aun con la libertad
        de poder modificar o eliminar lo ageno, sean capaces no solo de respetar la opinión de toda la comunidad, sino
        que trabajen en conjunto para hacer tanto de la página web MeowBook como la comunidad que han formado mejoren
        tanto como ellos se lo permitan.
    </p>
    <h3>Información acerca de las librerías/frameworks/plugins utilizadas en Front-end, Back-end y Base de datos</h3>
    <ul>
        <li><strong>Front-end:</strong> Javascript</li>
        <li><strong>Back-end:</strong> 
            <ul>
                <li>-Flask-SQLAlchemy</li>
                <li>-Flask-Migrate</li>
                <li>-Flask</li>
            </ul>
        </li>
    </ul>
    <h3>Base de datos:</h3>
    La base de datos que usamos es PostgreSQL.
    <h3>Endpoints</h3>
        <ul>
            <li><strong>'/login':</strong></li> Lleva a la página de de inicio de sesión donde se puede ingresar al menú principal si la cuenta está previamente registrada.
            <li><strong>'/login/succesful':</strong></li> Con método POST recibe lo ingresado en inicio de sesión y verifica que la cuenta esté previamente registrada.
            <li><strong>'/registro':</strong></li> Carga la página donde se ingresa los valores para registrar un nuevo usuario.
            <li><strong>'/registro/succesful':</strong></li> Utiliza método POST para recibir los datos puestos en el registro y crear un nuevo usuario en la base de datos (tabla 'usuarios').
            <li><strong>'/libro':</strong></li> Muestra página donde se añaden datos para agregar un nuevo libro y muestra los libros ya creados.
            <li><strong>'/libro/registrar':</strong></li> A través de POST recibe datos para crear un nuevo libro en la base de datos (tabla 'libros').
            <li><strong>'/libros/<libro_name>/delete-libro':</strong></li> Con el método DELETE recibe el nombre de un libro, lo busca en la base de datos y lo elimina de esta (tabla 'libros').
            <li><strong>'/main_menu':</strong></li> Carga el menú principal donde se pueden ver los libros de la base de datos y filtrarlos.
            <li><strong>'/libro/busqueda':</strong></li> Permite filtrar los libros de la base de datos por su nombre o un fracmento de este a través del método POST.
            <li><strong>'/editarlibro':</strong></li> Carga página que permite editar los libros y modifcar la base de datos (tabla 'libros').
            <li><strong>'/libro/editar/final':</strong></li> Con POST recibe los datos a modificar de un libro y los actualiza en la base de datos (tabla 'libros').
            <li><strong>404:</strong></li> Al buscar cualquier path que no esté en la aplicación, te redirige a una página que te anuncia que lo buscado no existe.
        </ul>
        
    <h3>Manejo de errores</h3>
    
    

