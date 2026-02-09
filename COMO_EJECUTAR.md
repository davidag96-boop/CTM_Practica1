# Cómo Ejecutar la Aplicación Streamlit

## 1. Descargar el Repositorio
Para comenzar, primero necesitas clonar el repositorio en tu máquina local. Abre una terminal y ejecuta el siguiente comando:

```bash
git clone https://github.com/davidag96-boop/CTM_Practica1.git
```

## 2. Instalar Python
Asegúrate de tener Python instalado en tu sistema. Puedes descargarlo desde la [página oficial de Python](https://www.python.org/downloads/). Sigue las instrucciones según tu sistema operativo para completar la instalación.

## 3. Configurar el Entorno Virtual
Es recomendable crear un entorno virtual para manejar las dependencias del proyecto. Navega al directorio del repositorio que acabas de clonar:

```bash
cd CTM_Practica1
```

Luego, crea un entorno virtual ejecutando:

```bash
python -m venv env
```

Para activar el entorno virtual, utiliza el siguiente comando:
- En Windows:
```bash
.
\env\Scripts\activate
```
- En macOS y Linux:
```bash
source env/bin/activate
```

## 4. Instalar Dependencias
Una vez que el entorno virtual esté activado, puedes instalar las dependencias necesarias. Ejecuta:

```bash
pip install -r requirements.txt
```

## 5. Ejecutar la Aplicación Streamlit
Después de instalar las dependencias, puedes ejecutar la aplicación Streamlit con el siguiente comando:

```bash
streamlit run app.py
```

Esto abrirá una nueva pestaña en tu navegador con la aplicación ejecutándose. ¡Disfruta de tu aplicación!