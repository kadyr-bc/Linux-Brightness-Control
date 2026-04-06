Control de Brillo (Brightness Control)
Esta herramienta ofrece un control de hardware gráfico y sencillo para monitores externos directamente en tu escritorio Linux. Fue creada para ofrecer una forma fácil de cambiar el brillo del monitor en Linux, similar a como se hace en Windows con la aplicación Twinkle Tray.

Características
Interfaz sencilla: Ajusta el brillo del monitor externo a través de una interfaz GTK limpia.

Control de color avanzado: Incluye configuraciones expandibles para ajustar el contraste y los niveles de Rojo, Verde y Azul.

Detección de hardware: Escanea automáticamente los monitores que admiten comandos DDC/CI.

Ajustes persistentes: Guarda tus preferencias y las restaura la próxima vez que abras la aplicación.

Instalación
Opción 1: Instalación completa (Recomendado)
El script install.sh proporcionado está diseñado para facilitar el proceso al automatizar las comprobaciones de dependencias, la configuración del hardware y la integración en el menú.

Descarga tanto el script de Python como install.sh en la misma carpeta.

Haz que el script sea ejecutable:

Bash
chmod +x install.sh
Ejecuta el instalador como usuario normal (solicitará sudo solo cuando sea necesario):

Bash
./install.sh
CRÍTICO: Debes cerrar sesión y volver a entrar para que los nuevos permisos de hardware surtan efecto.

Nota: El instalador configura ddcutil, habilita el módulo i2c-dev, te añade al grupo i2c y crea un acceso directo en tu menú de aplicaciones.

Opción 2: Ejecución rápida (Portátil)
Si ya tienes las dependencias instaladas y tu usuario tiene los permisos correctos (es decir, perteneces al grupo i2c), puedes ejecutar el script directamente sin instalar nada en tu sistema:

Bash
python3 brightness-control.py
Uso
Una vez configurado y tras haber reiniciado sesión, busca Control de Brillo en tu lanzador de aplicaciones. La aplicación mostrará un indicador de carga mientras escanea monitores compatibles antes de mostrar los controles deslizantes.

⚠️ Nota sobre los valores predeterminados: Al abrir la aplicación por primera vez, los controles deslizantes se establecerán en un valor predeterminado de 50. Ten en cuenta que estos valores iniciales de la interfaz no reflejan los valores reales actuales del hardware de tu monitor. Una vez que ajustes los controles, tus nuevas preferencias se guardarán y se restaurarán en usos futuros.
