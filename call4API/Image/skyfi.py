import os
from typing import List, Dict, Any

import httpx
from dotenv import load_dotenv
import webbrowser

class Skyfi:
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ.get("API_KEY_SKYFI")
        self.base_url = "https://app.skyfi.com/platform-api"
        self.base_url_auth = "https://app.skyfi.com/platform-api/auth/"

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

    def get_catalog(self, aoi_wkt: str, fromDate: str,toDate: str,resolutions: List[str],productTypes: List[str],providers: List[str],
        maxCloudCoveragePercent: int = 10, maxOffNadirAngle: int = 4,openData: bool = True,) -> Dict[str, Any]:
        try:
            request = {
                "aoi": aoi_wkt,
                "fromDate": "2000-01-01T00:00:00",
                "toDate": "2024-12-31T00:00:00",
                "maxCloudCoveragePercent": maxCloudCoveragePercent,
                "maxOffNadirAngle": maxOffNadirAngle,
                "resolutions": ["VERY HIGH"],
                "productTypes": ["DAY", "MULTISPECTRAL"],
                "providers": ["SATELLOGIC", "SENTINEL2_CREODIAS"],
                "openData": openData,
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
