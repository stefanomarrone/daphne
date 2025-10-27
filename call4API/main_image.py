from call4API.Image.skyfiOrder import Order
from call4API.catalog.polygon_catalog import polygon_catalog
from call4API.catalog.coordinates_catalog import coordinates_catalog
from call4API.Image.GeeAPI import GeeAPI
import sys
from src.configuration import Configuration
from call4API.Image.skyfiApi import Skyfi


def skyfi(conf: Configuration):
    sky = Skyfi(conf)
    print("----User Info----")
    sky.get_current_user()
    print("----List Orders----")
    sky.get_user_orders(info_print=True)

def catalog(conf: Configuration):
    sky = Skyfi(conf)
    sky.catalog_gallery()

def order_request(conf: Configuration):
    sky = Skyfi(conf)
    txt_path = "/Users/stella/programming/repo4pat/skyfi_document/order_request/order_request_20251020.txt"
    order = Order(conf)
    order.order_txt_to_csv(txt_path)
    archive_ids = order.get_achiveId_toplace()
    response_data = sky.place_orders(archive_ids=archive_ids, delivery_driver="NONE",delivery_params=None)
    order.save_order_response(response_data)


def order_status(conf: Configuration):
    sky = Skyfi(conf)
    orderId = "2bcf71c0-2723-467c-80ec-9129c08fc857"
    sky.get_order_status(orderId, print_info=True)

def update_orders(conf: Configuration):
    sky = Skyfi(conf)
    order = Order(conf)
    try:
        orders = sky.get_user_orders()
        order.update_order_response(orders["orders"])
    except Exception as e_detail:
        print(f"Impossibile aggiornare gli ordini: {e_detail}")


def download(conf: Configuration):
    sky = Skyfi(conf)
    orderId = "2bcf71c0-2723-467c-80ec-9129c08fc857"
    sky.download_deliverable(orderId)
    #todo update csv dopo aver scaricato l'immagine

functions = {
    'skyfi': skyfi,
    'catalog': catalog,
    'order_request': order_request,
    'order_status': order_status,
    'update_orders': update_orders,
    'download': download
}

if __name__ == '__main__':
    configuration = Configuration(sys.argv[1])
    command = functions[sys.argv[2]]
    command(configuration)

'''
if __name__ == '__main__':

   lat = -16.949631
   lon = 12.332528
   #lat = None
   #lon = None
   start_date = "2023-01-01 12:00:00"
   end_date = "2023-01-02 12:00:00"
   image_catalog_name = "MODIS"
   #country_name = "Saudi_Arabia"
   country_name = ''


   geeAPI = GeeAPI()
   geeAPI.authenticate()
   geeAPI.download_satellite_image(country_name, lat, lon, start_date, end_date, image_catalog_name)
'''