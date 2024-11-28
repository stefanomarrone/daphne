from IPython.core.display_functions import display

if __name__ == '__main__':
    wind= {'speed': 4.63, 'deg': 70}
    if 'speed' not in wind.keys():
        print('no')


if __name__ == '__main__':
    import ee
    import requests
    import os

    # Autenticazione a Earth Engine
    ee.Authenticate()
    ee.Initialize()

    # Caricamento della collezione di immagini MODIS
    dataset = ee.ImageCollection('MODIS/061/MOD13Q1').filter(ee.Filter.date('2018-01-01', '2019-01-01'))

    ndvi = dataset.select('NDVI').mean()  # Calcolo della media NDVI nel periodo

    # Definizione della regione di interesse (bounding box)
    region_of_interest = ee.Geometry.BBox(12.332528, -28.038970, 38.6245267, 29.6369064)

    # Get the first image in the collection
    image = ndvi.clip(region_of_interest)

    # Define the url
    # url = image.getDownloadUrl(
    #     {'region': region_of_interest.getInfo()['coordinates'], 'scale': 30})
    # os.makedirs('maggio', exist_ok=True)
    # response = requests.get(url)
    # image_zip_filepath = f"{'maggio'}/{'mod'}_{'2018'}_to_{'2019'}.{'zip'}"
    # with open(image_zip_filepath, 'wb') as f:
    #     f.write(response.content)

    # Configurazione dell'esportazione dell'immagine
    export_task = ee.batch.Export.image.toDrive(
        image=ndvi.clip(region_of_interest),
        description='NDVI_Image_Export',
        folder='EarthEngineImages_2',  # Assicurati di avere questa cartella nel tuo Google Drive
        fileNamePrefix='NDVI_2018_to_2019',
        region=region_of_interest.getInfo()['coordinates'],
        scale=500,  # Scala in metri (adatta secondo le tue necessità)
        crs='EPSG:4326',  # Sistema di riferimento delle coordinate
        maxPixels=1e13  # Numero massimo di pixel
    )

    # Avvio dell'esportazione
    export_task.start()

print('Esportazione avviata. Controlla il tuo Google Drive per il file esportato.')

if __name__ == '__main__':
    import ee
    import folium

    # Autenticazione a Earth Engine
    ee.Authenticate()
    ee.Initialize()

    # Caricamento della collezione di immagini MODIS
    dataset = ee.ImageCollection('MODIS/061/MOD13Q1').filter(ee.Filter.date('2018-01-01', '2018-05-01')).first()

    ndvi = dataset.select('NDVI')

    # Definizione delle visualizzazioni per NDVI
    ndvi_vis = {
        'min': 0,
        'max': 8000,
        'palette': [
            'ffffff', 'ce7e45', 'df923d', 'f1b555', 'fcd163', '99b718', '74a901',
            '66a000', '529400', '3e8601', '207401', '056201', '004c00', '023b01',
            '012e01', '011d01', '011301'
        ]
    }

    # Creazione di una lista di Feature
    features = [
        ee.Feature(ee.Geometry.Point([18.105889, -28.038970]), {'name': 'Namibia'}),
        ee.Feature(ee.Geometry.Point([12.332528, -16.949631]), {'name': 'Angola'}),
        ee.Feature(ee.Geometry.Point([38.6245267, 29.6369064]), {'name': 'Saudi Arabia'}),
        ee.Feature(ee.Geometry.Point([36.860099, -1.346889]), {'name': 'Kenya'})
    ]

    # Creazione di una FeatureCollection dalla lista
    from_list = ee.FeatureCollection(features)

    # Definizione del centro della mappa
    map_center = [0, 0]  # Puoi cambiare questa posizione per centrare la mappa sui tuoi punti
    zoom_level = 2  # Cambia il livello di zoom se necessario

    # Creazione della mappa Folium
    map_folium = folium.Map(location=map_center, zoom_start=zoom_level)


    # Aggiunta del layer NDVI alla mappa Folium
    def add_ee_layer(self, ee_image_object, vis_params, name):
        map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
        folium.TileLayer(
            tiles=map_id_dict['tile_fetcher'].url_format,
            attr='Google Earth Engine',
            name=name,
            overlay=True,
            control=True
        ).add_to(self)


    # Aggiunta del metodo add_ee_layer alla classe folium.Map
    folium.Map.add_ee_layer = add_ee_layer

    # Aggiunta del layer NDVI
    map_folium.add_ee_layer(ndvi, ndvi_vis, 'NDVI')

    # Aggiunta dei punti alla mappa
    for feature in features:
        coords = feature.geometry().coordinates().getInfo()
        name = feature.get('name').getInfo()
        folium.Marker(location=[coords[1], coords[0]], popup=name).add_to(map_folium)

    # Aggiunta del controllo layer alla mappa
    folium.LayerControl().add_to(map_folium)

    # Visualizzazione della mappa
    map_folium
