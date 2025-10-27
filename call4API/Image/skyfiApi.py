import os
from typing import List, Dict, Any
import httpx
from dotenv import load_dotenv
import webbrowser
from pathlib import Path
from datetime import datetime
from call4API.catalog.coordinates_catalog import coordinates_catalog
from call4API.catalog.polygon_catalog import polygon_catalog
from call4API.scripts.date_utils import date_to_iso, _fmt_date, from_iso_format, replace_str_with_date
from call4API.scripts.utils import _pct, extract_feature_from_configuration
from call4API.template.skyfi_template_html import skyfi_template_html

class Skyfi:
    def __init__(self, conf):
        load_dotenv()
        self.api_key = os.environ.get("API_KEY_SKYFI")
        self.base_url = "https://app.skyfi.com/platform-api"
        self.base_url_auth = "https://app.skyfi.com/platform-api/auth/"
        self.catalog_title = "SkyFi Catalog"
        self.order_request_file = "order_request.txt"

        lat, lon, fromdate, todate, _, countryname = extract_feature_from_configuration(conf)
        self.lat = lat
        self.lon = lon
        self.countryname = self._countryname()
        self.aoi = polygon_catalog().create_polygon(self.lat, self.lon)
        self.resolutions = [p.upper() for p in (conf.get("resolutions") or [])]
        self.productTypes = [p.upper() for p in (conf.get("productTypes") or [])]
        self.providers = [p.upper() for p in (conf.get("providers") or [])]
        self.openData = str(conf.get("openData")).strip().lower() == "true"
        self.fromdate = date_to_iso(fromdate)
        self.todate = date_to_iso(todate)
        self.maxCloudCoveragePercent = conf.get("maxCloudCoveragePercent")

        self.catalog_folder = Path(conf.get("catalogfolder"))
        self.order_request_folder =  Path(conf.get("orderrequestfolder"))
        self.order_response_folder = Path(conf.get("orderresponsefolder"))
        self.download_image_folder = Path(conf.get("downloadimagefolder"))
        self.deliverable_type = conf.get("deliverabletype")

    def _countryname(self):
        if self.lat != None and self.lon != None:
            return coordinates_catalog().get_countryname(self.lat, self.lon)

    def _aoi(self):
        if self.countryname != '':
            return polygon_catalog().get_polygon_catalog(self.countryname)
        elif self.lat != None and self.lon != None:
            return polygon_catalog().create_polygon(self.lat, self.lon)
        else:
            return None

    def _auth_headers(self):
        return {"X-Skyfi-Api-Key": self.api_key} if self.api_key else {}

    def ping(self):
        ping_response = httpx.get(f"{self.base_url}/ping", headers=self._auth_headers())
        ping = ping_response.json()
        return ping['message']

    def check_status(self):
        health_check_response = httpx.get(f"{self.base_url}/health_check", headers=self._auth_headers())
        health_check = health_check_response.json()
        return health_check['status']

    def rapid_doc_status(self):
        rapid_doc_response = httpx.get(f"{self.base_url}/rapidoc", headers=self._auth_headers(), follow_redirects=True)
        return rapid_doc_response.status_code

    def open_docs_in_browser(self, kind: str = "rapidoc"):
        routes = {
            "rapidoc": f"{self.base_url}/rapidoc",
            "redoc":   f"{self.base_url}/redoc",   # ReDoc ufficiale
            "swagger": f"{self.base_url}/docs",    # Swagger UI
        }
        url = routes.get(kind.lower(), routes["rapidoc"])
        webbrowser.open(url)

    def get_openapi_spec(self):
        r = httpx.get(f"{self.base_url}/openapi.json", headers=self._auth_headers(), follow_redirects=True)
        r.raise_for_status()
        info = r.json()
        print(info["info"]["title"], info["openapi"])
        return info

    def get_current_user(self):
        try:
            response = httpx.get(
                f"{self.base_url_auth}/whoami",
                headers=self._auth_headers(),
                timeout=10.0
            )
            response.raise_for_status()
            whoami = response.json()

            budget_eur = whoami.get("budgetAmount", 0) / 100
            usage_eur = whoami.get("currentBudgetUsage", 0) / 100

            user_info = {
                "id": whoami.get("id"),
                "organizationId": whoami.get("organizationId"),
                "isDemoAccount": whoami.get("isDemoAccount"),
                "hasValidSharedCard": whoami.get("hasValidSharedCard"),
                "email": whoami.get("email"),
                "user_firstName": whoami.get("firstName"),
                "user_lastName": whoami.get("lastName"),
                "budget_formatted": f"{budget_eur:.2f} €",
                "usage_formatted": f"{usage_eur:.2f} €"
            }

            print(f"Email: {user_info['email']}")
            print(f"Current User: {user_info['user_firstName']} {user_info['user_lastName']}")
            print(f"Budget: {user_info['budget_formatted']}")
            print(f"Utilizzato: {user_info['usage_formatted']}")

            return user_info

        except httpx.HTTPStatusError as e:
            return {"status": "error", "code": e.response.status_code, "message": e.response.text}
        except httpx.RequestError as e:
            return {"status": "error", "message": f"Errore: {e}"}

    def get_catalog(self) -> Dict[str, Any]:
        try:
            request = {
                "aoi": self.aoi,
                "fromDate": self.fromdate,
                "toDate": self.todate,
                "maxCloudCoveragePercent": self.maxCloudCoveragePercent,
                "maxOffNadirAngle": 50,
                "resolutions": self.resolutions,
                "productTypes": self.productTypes,
                "providers": self.providers,
                "openData": self.openData,
                "minOverlapRatio": 0.1,
                "pageSize": 100
            }
            archives_response = httpx.post( f"{self.base_url}/archives", json=request, headers=self._auth_headers(), follow_redirects=True, timeout=30.0)
            archives_response.raise_for_status()
            data = archives_response.json()
            result = {
                #"request": data.get("request", request),
                "archives": data.get("archives", []),
                "nextPage": data.get("nextPage"),
                "total": data.get("total", len(data.get("archives", []))),
            }
            return result

        except httpx.HTTPStatusError as e:
            return {"status": "error", "code": e.response.status_code, "message": e.response.text}
        except httpx.RequestError as e:
            return {"status": "error", "message": f"Errore: {e}"}


    def catalog_gallery(self):
        catalog_response = self.get_catalog()
        archives = catalog_response['archives']

        cards = []
        for a in archives:
            thumb = (a.get("thumbnailUrls") or {}).get("300x300")
            archiveId = a.get("archiveId", "-")
            provider = a.get("provider", "-")
            date = from_iso_format(_fmt_date(a.get("captureTimestamp", "-")))
            cloud = _pct(a.get("cloudCoveragePercent", "-"))
            res = a.get("resolution", "-")
            priceFullScene = str(a.get("priceFullScene", "-"))

            t = skyfi_template_html.card_block(
                thumb=thumb, archiveId=archiveId, provider=provider, date=date,
                cloud=cloud, res=res, priceFullScene=priceFullScene
            )
            cards.append(t)
        stamp = datetime.now().strftime("%Y%m%d")
        html_template = skyfi_template_html(title=self.catalog_title, cards=cards, stamp=stamp)
        html = html_template.get_template()

        out_dir = self.catalog_folder
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = Path(f"{out_dir}/catalog_{self.countryname}_{self.fromdate}_{self.todate}_openData{self.openData}_{stamp}.html")
        out_path.write_text(html, encoding="utf-8")
        return print("Catalogo salvato in:" + str(out_path.resolve()))


    def place_orders(self, delivery_params,
                     archive_ids: List[str],
                     delivery_driver: str = "NONE",
                     ) -> List[Dict[str, Any]]:
        #Crea un ordine per ciascun archiveId. Ritorna la lista delle risposte.
        results = []
        for aid in archive_ids:
            payload = {
                "aoi": self.aoi,
                "archiveId": aid,
                "deliveryDriver": delivery_driver,
                "deliveryParams": delivery_params,
                "metadata": {}
            }
            try:
                r = httpx.post(
                    f"{self.base_url}/order-archive",
                    headers={**self._auth_headers(), "Content-Type": "application/json"},
                    json=payload,
                    timeout=30.0,
                    follow_redirects=True
                )
                r.raise_for_status()
                results.append({"archiveId": aid, "status": "ok", "response": r.json()})
            except httpx.HTTPStatusError as e:
                results.append({"archiveId": aid, "status": "error", "code": e.response.status_code, "message": e.response.text})
            except httpx.RequestError as e:
                results.append({"archiveId": aid, "status": "error", "message": f"Errore rete: {e}"})
        return results


    def get_order_status(self, order_id: str, print_info=False):
        try:
            url = f"{self.base_url}/orders/{order_id}"
            response = httpx.get(url, headers=self._auth_headers(), timeout=30.0)
            response.raise_for_status()
            data = response.json()

            status = data.get("status")
            created_at = replace_str_with_date(data.get("createdAt"))
            download_url = data.get("downloadImageUrl")
            payload_url = data.get("downloadPayloadUrl")

            if print_info:
                print(f"Order: {order_id} - Created at: {created_at} - Status: {status}")
                if download_url:
                    print(f"Image ready: {download_url}")
                if payload_url:
                    print(f"Payload: {payload_url}")

            return data

        except httpx.HTTPStatusError as e:
            print(f"Errore HTTP: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            print(f"Errore generale: {e}")

    def get_user_orders(self, info_print=False):
        try:
            url = f"{self.base_url}/orders"
            response = httpx.get(url, headers=self._auth_headers(), timeout=30.0)
            response.raise_for_status()
            orders = response.json()

            for order in orders["orders"]:
                order_id = order.get("orderId")
                created_at = replace_str_with_date(order.get("createdAt"))
                status = order.get("status")
                if info_print:
                    print(f"Order: {order_id} - Created at: {created_at} - Status: {status}")
            return orders

        except httpx.HTTPStatusError as e:
            print(f"Errore HTTP: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            print(f"Errore generale: {e}")

    def download_deliverable(self, order_id) -> str:
        url = f"{self.base_url}/orders/{order_id}/image"
        out_dir = self.download_image_folder
        out_dir.mkdir(parents=True, exist_ok=True)

        # seguiamo i redirect e salviamo lo stream
        with httpx.stream("GET", url, headers=self._auth_headers(), follow_redirects=True, timeout=60.0) as r:
            r.raise_for_status()
            # prova a ricavare un nome sensato
            fname = f"{self.countryname}_{self.deliverable_type}.png"
            out_path = out_dir / fname
            with open(out_path, "wb") as f:
                for chunk in r.iter_bytes():
                    f.write(chunk)

        print(f"Scaricato: {out_path}")
        return str(out_path)