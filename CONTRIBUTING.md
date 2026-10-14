# Contribuir a Biblo

Gracias por tu interés en Biblo. Es un proyecto pequeño con un solo mantenedor, así que unas notas previas ahorran
tiempo a todos.

## Abre antes un issue

Abre un issue antes de escribir código, tanto para un arreglo como para una función nueva. Puede que ya esté en marcha
y aún no se haya subido, y así sabrás si encaja («sí», «ahora no» o «así debería encajar») antes de dedicarle una
tarde. Un pull request que llegue sin issue puede cerrarse con un enlace a esta página.

## Pull requests

Cuando el issue diga adelante:

- Un solo arreglo o una sola función, con el motivo en la descripción.
- `swift test` tiene que pasar.
- Si cambia lo que devuelve la búsqueda, pasa los evals de `evals/` antes y después (por ejemplo,
  `.build/release/biblo eval evals/synthetic.json --index <índice de ~/BibloTestbed>`) e incluye los dos resultados.
- Si cambia la velocidad o la memoria, mide antes y después en el mismo Mac.

Biblo lo guarda todo en el Mac, así que no encajan los cambios que envían datos fuera, como la telemetría o los
servicios en la nube.

## Qué esperar

Biblo se mantiene junto a un trabajo y otros proyectos, así que las respuestas pueden tardar unos días. Una semana sin
noticias significa mucho trabajo, no que se ignore: todos los issues reciben respuesta, aunque sea «ahora no».

No todos los pull requests se integran, ni siquiera los buenos. El proyecto tiene un rumbo y algunos cambios no
encajan en él; otros se rehacen para adaptarlos al trabajo en curso, y entonces se reconoce la autoría en las notas de
la versión.

## Informar de un error

Ayuda indicar tu Mac (chip y memoria), las versiones de macOS y de Biblo, qué hiciste o buscaste y qué esperabas. Los
registros están en `~/Library/Application Support/Biblo/index.noindex` (`app.log` e `indexer.log`). Pueden contener
nombres de archivo y tus búsquedas: revísalos antes de pegarlos.

Para un problema de seguridad, usa «Report a vulnerability» en la pestaña Security en lugar de abrir un issue público.
