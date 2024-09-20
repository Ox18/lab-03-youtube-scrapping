import requests
import re
import json
import streamlit as st

def obtener_datos_youtube(query):
    url_youtube = f"https://www.youtube.com/results?search_query={query}"

    response = requests.get(url_youtube)

    pattern = r"var ytInitialData = ({.*?});"
    match = re.search(pattern, response.text)

    if match:
        data = match.group(1)
        data = json.loads(data)

        try:
            contents = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]
        except KeyError:
            st.error("No se encontraron resultados.")
            return []

        items_list = []

        for content in contents:
            if "videoRenderer" not in content:
                continue

            data = content["videoRenderer"]
            title = data["title"]["runs"][0]["text"]
            image_url = data["thumbnail"]["thumbnails"][-1]["url"]
            video_url = "https://www.youtube.com/watch?v=" + data["videoId"]
            channel_name = data["ownerText"]["runs"][0]["text"]
            channel_name_id = data["ownerText"]["runs"][0]["navigationEndpoint"]["browseEndpoint"]["browseId"]
            vistas = data.get("viewCountText", {}).get("simpleText", "No disponible")
            tiempo = data.get("lengthText", {}).get("simpleText", "No disponible")

            items_list.append({
                "title": title,
                "image_url": image_url,
                "video_url": video_url,
                "channel_name": channel_name,
                "channel_name_id": channel_name_id,
                "vistas": vistas,
                "tiempo": tiempo
            })

        return items_list

    else:
        st.error("No se pudo extraer la información.")
        return []


# Interfaz de Streamlit
st.title("Scraping de YouTube")

# Entrada de texto para la búsqueda
search_query = st.text_input("Introduce el texto de búsqueda")

# Botón para ejecutar el scraping
if st.button("Buscar"):
    if search_query:
        st.write(f"Buscando: {search_query}")
        resultados = obtener_datos_youtube(search_query)
        
        # Mostrar resultados
        if resultados:
            for item in resultados:
                st.image(item["image_url"], width=120)
                st.write(f"**Título**: {item['title']}")
                st.write(f"**Canal**: [{item['channel_name']}](https://www.youtube.com/channel/{item['channel_name_id']})")
                st.write(f"**Vistas**: {item['vistas']}")
                st.write(f"**Duración**: {item['tiempo']}")
                st.write(f"[Ver Video]({item['video_url']})")
                st.write("---")
        else:
            st.write("No se encontraron resultados para la búsqueda.")
    else:
        st.warning("Por favor, introduce un texto de búsqueda.")
