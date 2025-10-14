import json
import os
from datetime import datetime
from typing import List, Dict, Any
import httpx
from dotenv import load_dotenv
import webbrowser
from pathlib import Path
from html import escape
from call4API.catalog.polygon_catalog import polygon_catalog
from call4API.scripts.date_utils import date_to_iso, _fmt_date
from call4API.scripts.utils import _pct

geometry = {
    "type": "Polygon",
    "coordinates": [[[12.4924, 41.8902], [12.4925, 41.8902],
                     [12.4925, 41.8903], [12.4924, 41.8903],
                     [12.4924, 41.8902]]]
}

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
        self.aoi = polygon_catalog().get_polygon_catalog(self.countryname)

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
                "aoi": self.aoi,
                "fromDate": self.fromdate,
                "toDate": self.todate,
                "maxCloudCoveragePercent": self.maxCloudCoveragePercent,
                "maxOffNadirAngle": 50,
                "resolutions": self.resolutions,
                "productTypes": self.productTypes,
                "providers": self.providers,
                "openData": self.openData == 'True',
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
        # Genera una galleria HTML (static) con selezione multipla e azioni (copia/scarica)
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

        html = f"""<!doctype html>
    <html>
    <head>
    <meta charset="utf-8">
    <title>{escape(title)}</title>
    <style>
      body {{ margin:20px;background:#fafafa;font-family:Inter,Arial,Helvetica,sans-serif }}
      h2 {{ margin:0 0 12px 0 }}
      .wrap {{ display:flex;flex-wrap:wrap;gap:12px }}
      .card {{
        position:relative; border:1px solid #ddd; border-radius:14px; padding:12px; width:230px;
        background:#fff; box-shadow:0 1px 2px rgba(0,0,0,.04);
      }}
      .thumb {{ text-align:center; margin-bottom:8px }}
      .meta {{ font-size:12px; line-height:1.25 }}
      .chk {{ position:absolute; top:10px; left:10px; cursor:pointer }}
      .chk input {{ display:none }}
      .chk span {{
        display:inline-block; width:20px; height:20px; border-radius:6px; border:2px solid #666;
        background:#fff; box-shadow:inset 0 0 0 3px #fff;
      }}
      .chk input:checked + span {{ background:#1e88e5; border-color:#1e88e5 }}
      .bar {{
        position:fixed; left:50%; transform:translateX(-50%); bottom:16px;
        background:#fff; border:1px solid #ddd; border-radius:12px; padding:8px 12px;
        box-shadow:0 6px 20px rgba(0,0,0,.12); display:flex; gap:8px; align-items:center; z-index:9999;
      }}
      .btn {{
        border:1px solid #ccc; border-radius:10px; padding:6px 10px; background:#f7f7f7;
        cursor:pointer; font-size:13px;
      }}
      .btn:hover {{ background:#eee }}
      .idsbox {{
        min-width:220px; max-width:520px; font-family:ui-monospace,Menlo,Consolas,monospace;
        font-size:12px; border:1px dashed #ccc; border-radius:8px; padding:6px; background:#fcfcfc;
        white-space:nowrap; overflow:auto;
      }}
      .tip {{
        color:#666; font-size:12px; margin-top:10px
      }}
    </style>
    </head>
    <body>
      <h2>{escape(title)}</h2>
      <div class="wrap">{''.join(cards)}</div>

      <div class="tip">Suggerimento: clicca sulle miniature per aprirle in un nuovo tab. Spunta più immagini per creare la lista di <code>archiveId</code>.</div>

      <div class="bar">
        <div id="count"><b>0</b> selezionati</div>
        <button class="btn" id="copy">Copia</button>
        <button class="btn" id="csv">Scarica CSV</button>
        <button class="btn" id="json">Scarica JSON</button>
        <div class="idsbox" id="ids">[]</div>
      </div>

    <script>
    function getSelected() {{
      return Array.from(document.querySelectorAll('.sel:checked')).map(el => el.value);
    }}
    function updateUI() {{
      const ids = getSelected();
      document.getElementById('count').innerHTML = '<b>' + ids.length + '</b> selezionati';
      document.getElementById('ids').textContent = JSON.stringify(ids);
    }}
    document.addEventListener('change', e => {{
      if (e.target.classList.contains('sel')) updateUI();
    }});
    function download(filename, text, type='text/plain') {{
      const blob = new Blob([text], {{type}});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url; a.download = filename; document.body.appendChild(a); a.click();
      setTimeout(() => {{ URL.revokeObjectURL(url); a.remove(); }}, 0);
    }}
    document.getElementById('copy').onclick = async () => {{
      const ids = getSelected();
      await navigator.clipboard.writeText(ids.join('\\n'));
      document.getElementById('copy').textContent = 'Copiato ✓';
      setTimeout(()=> document.getElementById('copy').textContent='Copia', 1000);
    }};
    document.getElementById('csv').onclick = () => {{
      const ids = getSelected();
      const lines = ['archiveId']; ids.forEach(id => lines.push(id));
      download('skyfi_selected_{stamp}.csv', lines.join('\\n'), 'text/csv');
    }};
    document.getElementById('json').onclick = () => {{
      const ids = getSelected();
      download('skyfi_selected_{stamp}.json', JSON.stringify({{archiveIds: ids}}, null, 2), 'application/json');
    }};
    </script>
    </body>
    </html>"""
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
                order_id = item.get("id")
                created_at = item.get("createdAt", datetime.now().isoformat())
                filename = f"order_{order_id}_{created_at}.json"
                out_path = out_dir / filename

                with open(out_path, "w", encoding="utf-8") as f:
                    json.dump(item, f, indent=2, ensure_ascii=False)

                print(f"Orderine salvato in {out_path.name} (OrderId: {order_id})")
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
