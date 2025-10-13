import os
from typing import List, Dict, Any
import httpx
from dotenv import load_dotenv
import webbrowser
from pathlib import Path
from html import escape
from call4API.catalog.polygon_catalog import polygon_catalog
from call4API.scripts.date_utils import date_to_iso, _fmt_date
from call4API.scripts.utils import _pct


class Skyfi:
    def __init__(self, conf):
        load_dotenv()
        self.api_key = os.environ.get("API_KEY_SKYFI")
        self.base_url = "https://app.skyfi.com/platform-api"
        self.base_url_auth = "https://app.skyfi.com/platform-api/auth/"
        self.countryname = conf.get("countryname")
        self.resolutions = [p.upper() for p in conf.get("resolutions")]
        self.productTypes = [p.upper() for p in conf.get("productTypes")]
        self.providers = [p.upper() for p in conf.get("providers")]
        self.openData = conf.get("openData")
        self.fromdate = date_to_iso(conf.get("fromdate"))
        self.todate = date_to_iso(conf.get("todate"))
        self.maxCloudCoveragePercent = conf.get("maxCloudCoveragePercent")

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

    def demo_delivery(self, geometry, product_type="optical", resolution=0.5, start_date=None, end_date=None, driver="GS"):
        # simula un acquisto
        geometry = {
            "type": "Polygon",
            "coordinates": [[[12.4924, 41.8902], [12.4925, 41.8902],
                             [12.4925, 41.8903], [12.4924, 41.8903],
                             [12.4924, 41.8902]]]
        }
        deliveryParams = {
            "geometry": geometry,
            "product_type": product_type,
            "resolution": resolution,
            "time_range": {
                "start": start_date or "2024-01-01",
                "end": end_date or "2024-02-01"
            }
        }

        payload = {
            "deliveryDriver": driver,
            "deliveryParams": deliveryParams
        }

        response = httpx.post(
            f"{self.base_url}/demo-delivery",
            headers={**self._auth_headers(), "Content-Type": "application/json"},
            json=payload,
            timeout=30.0,
        )

        if response.status_code == 200:
            return response.json()
        else:
            return {
                "status": "error",
                "code": response.status_code,
                "message": response.text
            }

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
                "aoi": polygon_catalog().get_polygon_catalog(self.countryname),
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



    def save_catalog_gallery(self, archives, title="SkyFi Catalog"):
        #Genera una galleria HTML (static) con miniature e info chiave.
        cards = []
        for a in archives:
            thumb = (a.get("thumbnailUrls") or {}).get("300x300")
            archiveId = a.get("archiveId", "-")
            provider = a.get("provider", "-")
            date = _fmt_date(a.get("captureTimestamp", "-"))
            cloud = _pct(a.get("cloudCoveragePercent", "-"))
            res = a.get("resolution", "-")
            gsd = a.get("gsd", "-")
            # Se la thumb esiste, rendila cliccabile per vederla full-size
            img_html = f'<a href="{escape(thumb)}" target="_blank"><img src="{escape(thumb)}" alt="thumb" style="width:150px;height:150px;object-fit:cover;border-radius:12px;"></a>' if thumb else "<div style='width:150px;height:150px;background:#eee;border-radius:12px;display:flex;align-items:center;justify-content:center;'>no thumb</div>"
            cards.append(f"""
            <div style="border:1px solid #ddd;border-radius:14px;padding:12px;margin:10px;width:220px;font-family:Arial">
              <div style="text-align:center">{img_html}</div>
              <div style="margin-top:8px;font-size:12px;line-height:1.2">
                <div><b>ID</b>: {escape(archiveId)}</div>
                <div><b>Prov</b>: {escape(str(provider))}</div>
                <div><b>Date</b>: {escape(date)}</div>
                <div><b>Cloud</b>: {escape(cloud)}</div>
                <div><b>Res</b>: {escape(str(res))}</div>
                <div><b>GSD</b>: {escape(str(gsd))}</div>
              </div>
            </div>""")

        html = f"""<!doctype html>
    <html>
    <head><meta charset="utf-8"><title>{escape(title)}</title></head>
    <body style="margin:20px;background:#fafafa">
      <h2 style="font-family:Arial;margin-bottom:10px">{escape(title)}</h2>
      <div style="display:flex;flex-wrap:wrap">{''.join(cards)}</div>
      <p style="font-family:Arial;color:#666">Suggerimento: clicca sulle miniature per aprirle in un nuovo tab, poi copia l'<code>archiveId</code> che ti interessa.</p>
    </body>
    </html>"""
        out_dir = Path("skyfiCatalog")
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = f"{out_dir}/catalog_gallery_{self.countryname}_{self.fromdate}_{self.todate}_openData{self.openData}.html"
        Path(out_path).write_text(html, encoding="utf-8")
        return print("Catalogo salvato in:" + str(Path(out_path).resolve()))

