import json
import os
from datetime import datetime
from typing import List, Dict, Any
import httpx
from dotenv import load_dotenv
import webbrowser
from pathlib import Path
from html import escape

from call4API.catalog.coordinates_catalog import coordinates_catalog
from call4API.catalog.polygon_catalog import polygon_catalog
from call4API.scripts.date_utils import date_to_iso, _fmt_date
from call4API.scripts.utils import _pct, extract_feature_from_configuration
from call4API.template.skyfi_template_html import skyfi_template_html


class Skyfi:
    def __init__(self, conf):
        load_dotenv()
        self.api_key = os.environ.get("API_KEY_SKYFI")
        self.base_url = "https://app.skyfi.com/platform-api"
        self.base_url_auth = "https://app.skyfi.com/platform-api/auth/"
        lat, lon, fromdate, todate, _, countryname = extract_feature_from_configuration(conf)
        self.lat = lat
        self.lon = lon
        self.countryname = self._countryname()
        self.aoi = polygon_catalog().create_polygon(self.lat, self.lon)
        self.resolutions = [p.upper() for p in conf.get("resolutions")]
        self.productTypes = [p.upper() for p in conf.get("productTypes")]
        self.providers = [p.upper() for p in conf.get("providers")]
        self.openData = self.openData = str(conf.get("openData")).strip().lower() == "true"
        self.fromdate = date_to_iso(fromdate)
        self.todate = date_to_iso(todate)
        self.maxCloudCoveragePercent = conf.get("maxCloudCoveragePercent")

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
        # prova a recuperare lo spec OpenAPI.
        r = httpx.get(f"{self.base_url}/openapi.json", headers=self._auth_headers(), follow_redirects=True)
        r.raise_for_status()
        response = r.json()
        return print(response["info"]["title"], response["openapi"])

    def get_current_user(self, verbose: bool = True):
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
                "email": whoami.get("email"),
                "budget_formatted": f"{budget_eur:.2f} €",
                "usage_formatted": f"{usage_eur:.2f} €"
            }

            if verbose:
                print(f"Email: {user_info['email']}")
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

    def catalog_gallery(self, title="SkyFi Catalog"):
        # Genera una galleria HTML (static) con selezione multipla e azioni (copia/scarica)
        catalog_response = self.get_catalog()
        archives = catalog_response['archives']

        from datetime import datetime
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        cards = []
        for a in archives:
            thumb = (a.get("thumbnailUrls") or {}).get("300x300")
            archiveId = a.get("archiveId", "-")
            provider = a.get("provider", "-")
            date = _fmt_date(a.get("captureTimestamp", "-"))
            cloud = _pct(a.get("cloudCoveragePercent", "-"))
            res = a.get("resolution", "-")
            gsd = a.get("gsd", "-")
            priceFullScene = a.get("priceFullScene", "-")

            img_html = (
                f'<a href="{escape(thumb)}" target="_blank"><img src="{escape(thumb)}" '
                f'alt="thumb" style="width:150px;height:150px;object-fit:cover;border-radius:12px;"></a>'
                if thumb else
                "<div style='width:150px;height:150px;background:#eee;border-radius:12px;"
                "display:flex;align-items:center;justify-content:center;'>no thumb</div>"
            )

            cards.append(f"""
            <div class="card">
              <label class="chk">
                <input type="checkbox" class="sel" value="{escape(archiveId)}">
                <span></span>
              </label>
              <div class="thumb">{img_html}</div>
              <div class="meta">
                <div><b>ID</b>: <code>{escape(archiveId)}</code></div>
                <div><b>Prov</b>: {escape(str(provider))}</div>
                <div><b>Date</b>: {escape(date)}</div>
                <div><b>Cloud</b>: {escape(cloud)}</div>
                <div><b>Res</b>: {escape(str(res))}</div>
                <div><b>GSD</b>: {escape(str(gsd))}</div>
                <div><b>Image Price</b>: {escape(str(priceFullScene))}</div>
              </div>
            </div>""")

        html = skyfi_template_html(title, cards, stamp).get_template()
        out_dir = Path("skyfiCatalog")
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = f"{out_dir}/catalog_gallery_{self.countryname}_{self.fromdate}_{self.todate}_openData{self.openData}.html"
        Path(out_path).write_text(html, encoding="utf-8")
        return print("Catalogo salvato in:" + str(Path(out_path).resolve()))

    def save_order_response(self, response_data):
        #Salva la/e response JSON degli ordini nella cartella 'skyfiJSON_response'.
        out_dir = Path("skyfiJSON_response")
        out_dir.mkdir(parents=True, exist_ok=True)

        saved_files = []

        # Se è una singola risposta, la metto in lista
        if isinstance(response_data, dict):
            response_data = [response_data]

        for item in response_data:
            filename = ""
            try:
                #order_id = item.get("id")
                order_code = item['response']['orderCode']
                created_at = item.get("createdAt", datetime.now().isoformat())
                filename = f"order_{order_code}_{created_at}.json"
                out_path = out_dir / filename

                with open(out_path, "w", encoding="utf-8") as f:
                    json.dump(item, f, indent=2, ensure_ascii=False)

                print(f"Orderine salvato in {out_path.name}")
                saved_files.append(str(out_path.resolve()))

            except Exception as e:
                print(f"Errore nel salvataggio ordine {filename}: {e}")

        return saved_files

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


    def order_from_json(self, path_json):
        with open(path_json, "r", encoding="utf-8") as f:
            data = json.load(f)
        archive_ids = data.get("archiveIds", [])
        if not archive_ids:
            print("Nessun archiveId nel file JSON.")
            return []
        response_data = self.place_orders(
            archive_ids=archive_ids,
            delivery_driver="NONE",
            delivery_params=None
        )
        return self.save_order_response(response_data)


    def get_order_status(self, order_id: str):
        try:
            url = f"{self.base_url}/orders/{order_id}"
            response = httpx.get(url, headers=self._auth_headers(), timeout=15.0)
            response.raise_for_status()
            data = response.json()

            status = data.get("status")
            download_url = data.get("downloadImageUrl")
            payload_url = data.get("downloadPayloadUrl")

            print(f"Order: {order_id} - Status: {status}")
            if download_url:
                print(f"Image ready: {download_url}")
            if payload_url:
                print(f"Payload: {payload_url}")

            return data

        except httpx.HTTPStatusError as e:
            print(f"Errore HTTP: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            print(f"Errore generale: {e}")

