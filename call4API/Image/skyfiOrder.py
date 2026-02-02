import json
from datetime import datetime
from pathlib import Path
import csv

from call4API.scripts.date_utils import replace_str_with_date


class Order:
    def __init__(self, conf):
        self.catalog_folder = Path(conf.get("catalogfolder"))
        self.order_request_folder =  Path(conf.get("orderrequestfolder"))
        self.order_response_folder = Path(conf.get("orderresponsefolder"))
        self.download_image_folder = Path(conf.get("downloadimagefolder"))
        self.deliverable_type = conf.get("deliverabletype")
        self.order_request_file = "order_request.txt"
        self.csv_filename = "orders.csv"
        self.status_for_download = "PROCESSING_COMPLETE"

    def order_txt_to_csv(self, txt_path: str = None):
        """
        Legge gli archiveId da un file TXT (uno per riga) e li inserisce in un CSV
        con colonne: archiveId, order_name, status, isImageDownloaded.
        """
        # 1) Sorgente TXT
        if txt_path is None:
            # usa il TXT di default salvato nella cartella degli order request
            txt_path = self.order_request_folder / self.order_request_file
        src = Path(txt_path).expanduser().resolve()
        if not src.exists():
            raise FileNotFoundError(f"File TXT non trovato: {src}")

        # 2) Destinazione CSV (registro)
        dst_dir = self.order_request_folder
        dst_dir.mkdir(parents=True, exist_ok=True)
        csv_path = dst_dir / self.csv_filename

        # 3) Leggi gli ID dal TXT
        raw_lines = src.read_text(encoding="utf-8").splitlines()
        ids = [line.strip() for line in raw_lines if line.strip()]
        if not ids:
            print("Nessun archiveId nel TXT; nessun aggiornamento al CSV.")
            return str(csv_path), {"added": 0, "skipped": 0, "total": 0}

        # 4) Carica eventuali righe esistenti dal CSV
        existing_rows = []
        existing_index = {}
        if csv_path.exists():
            with open(csv_path, "r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    row.setdefault("orderId", "")
                    row.setdefault("archiveId", "")
                    row.setdefault("order_name", "")
                    row.setdefault("status", "")
                    row.setdefault("isImageDownloaded", "false")
                    existing_rows.append(row)
                    if row["archiveId"]:
                        existing_index[row["archiveId"]] = row

        # 5) Aggiungi nuovi ID evitando duplicati
        added = 0
        for aid in ids:
            if aid not in existing_index:
                new_row = {
                    "orderId": "",
                    "archiveId": aid,
                    "order_name": "",
                    "status": "",
                    "isImageDownloaded": "false",
                }
                existing_rows.append(new_row)
                existing_index[aid] = new_row
                added += 1

        skipped = len(ids) - added
        total = len(existing_rows)

        # 6) Scrivi (o riscrivi) il CSV con header ordinato
        fieldnames = ["orderId", "archiveId", "order_name", "status", "isImageDownloaded"]
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(existing_rows)

        print(f"Registro aggiornato: {csv_path} (+{added} nuovi, {skipped} duplicati, tot={total})")
        return str(csv_path), {"added": added, "skipped": skipped, "total": total}

    def get_achiveId_toplace(self):
        csv_path = self.order_request_folder / self.csv_filename
        if not csv_path.exists():
            print(f"CSV non trovato: {csv_path}")
            return {"to_order": 0, "ordered": 0, "errors": 0}

        # 1) carica righe esistenti
        with open(csv_path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # normalizza colonne minime richieste
        for r in rows:
            r.setdefault("archiveId", "")
            r.setdefault("order_name", "")
            r.setdefault("status", "")
            r.setdefault("isImageDownloaded", "false")

        # 2) seleziona le righe vuote
        candidates_idx = [
            i for i, r in enumerate(rows)
            if r.get("archiveId") and not r.get("order_name") and not r.get("status")
        ]
        if not candidates_idx:
            print("Nessuna riga 'vuota' nel CSV da ordinare.")
            return {"to_order": 0, "ordered": 0, "errors": 0}

        archive_ids = [rows[i]["archiveId"] for i in candidates_idx]
        return archive_ids

    def save_order_response(self, response_data):
        #Salva la/e response JSON degli ordini nella cartella 'order_response_folder'.
        out_dir = self.order_response_folder
        out_dir.mkdir(parents=True, exist_ok=True)

        saved_files = []
        # Se è una singola risposta, la metto in lista
        if isinstance(response_data, dict):
            response_data = [response_data]

        for item in response_data:
            filename = ""
            try:
                order_id = item['response']['id']
                order_code = item['response']['orderCode']
                created_at = replace_str_with_date(item['response']['createdAt'])
                filename = f"order_ID_{order_id}_{created_at}.json"
                out_path = out_dir / filename

                with open(out_path, "w", encoding="utf-8") as f:
                    json.dump(item, f, indent=2, ensure_ascii=False)

                print(f"Ordine salvato in {out_path.name}")
                saved_files.append(str(out_path.resolve()))

            except Exception as e:
                print(f"Errore nel salvataggio ordine {filename}: {e}")
        self.update_orders_csv_from_responses(response_data, saved_files)

        return saved_files

    def update_order_response(self, orders_list):
        out_dir = self.order_response_folder
        out_dir.mkdir(parents=True, exist_ok=True)

        saved_files = []
        for item in orders_list:
            filename = ""
            try:
                order_id = item['id']
                created_at = replace_str_with_date(item['createdAt'])
                filename = f"order_ID_{order_id}_{created_at}.json"
                out_path = out_dir / filename

                with open(out_path, "w", encoding="utf-8") as f:
                    json.dump(item, f, indent=2, ensure_ascii=False)

                print(f"Ordine aggiornato in {out_path.name}")
                saved_files.append(str(out_path.resolve()))

            except Exception as e:
                print(f"Errore nel'aggiornamento ordine {filename}: {e}")
        self.update_orders_csv_from_orders_list(orders_list, saved_files)

        return saved_files

    def update_orders_csv_from_orders_list(self, orders_list, saved_files):
        if orders_list is None:
            print("Nessun ordine da aggiornare (orders_list=None).")
            return {"updated": 0, "inserted": 0, "errors": 0}

        csv_path = self.order_request_folder / self.csv_filename
        if not csv_path.exists():
            # Se il CSV non esiste, crealo con header standard
            fieldnames = ["orderId", "archiveId", "order_name", "status", "isImageDownloaded"]
            with open(csv_path, "w", encoding="utf-8", newline="") as f:
                w = csv.DictWriter(f, fieldnames=fieldnames)
                w.writeheader()

        # Carica CSV
        with open(csv_path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            fieldnames = reader.fieldnames or []

        idx_by_order = {}
        idx_by_archive = {}
        for i, r in enumerate(rows):
            r.setdefault("archiveId", "")
            r.setdefault("order_name", "")
            r.setdefault("status", "")
            r.setdefault("isImageDownloaded", "False")
            r.setdefault("orderId", "")

            if r["orderId"]:
                idx_by_order[r["orderId"]] = i
            if r["archiveId"]:
                idx_by_archive[r["archiveId"]] = i

        updated = 0
        inserted = 0
        errors = 0

        for i, item in enumerate(orders_list):
            try:
                order_id = item.get("orderId") or item.get("id", "")
                status = item.get("status", "") or ""
                arch = item.get("archive") or {}
                archive_id = arch.get("archiveId") or item.get("archiveId", "")

                order_filename = ""
                if i < len(saved_files) and saved_files[i]:
                    order_filename = Path(saved_files[i]).name


                # 1) match per orderId
                if order_id and order_id in idx_by_order:
                    row = rows[idx_by_order[order_id]]
                    row["status"] = status or row.get("status", "")
                    if archive_id and not row.get("archiveId"):
                        row["archiveId"] = archive_id
                    updated += 1
                    continue

                # 2) fallback: match per archiveId
                if archive_id and archive_id in idx_by_archive:
                    row = rows[idx_by_archive[archive_id]]
                    row["status"] = status or row.get("status", "")
                    if order_id and not row.get("orderId"):
                        row["orderId"] = order_id
                    updated += 1
                    continue

                # 3) altrimenti, aggiungi nuova riga
                new_row = {
                    "archiveId": archive_id,
                    "order_name": order_filename,
                    "status": status,
                    "isImageDownloaded": "False",
                    "orderId": order_id,
                }
                rows.append(new_row)
                # aggiorna indici
                if order_id:
                    idx_by_order[order_id] = len(rows) - 1
                if archive_id:
                    idx_by_archive[archive_id] = len(rows) - 1
                inserted += 1

            except Exception as e:
                print(f"[WARN] Errore processando ordine: {e}")
                errors += 1

        # Riscrivi CSV
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(rows)

        print(f"CSV aggiornato: {csv_path} (updated={updated}, inserted={inserted}, errors={errors})")
        return {"updated": updated, "inserted": inserted, "errors": errors}


    def update_orders_csv_from_responses(self, response_data, saved_files):
        """
        Aggiorna orders.csv usando le risposte dell'API (response_data) e i file JSON salvati (saved_files).
        - Match su 'archiveId' (chiave nel CSV).
        - Compila 'order_name' con il filename JSON salvato.
        - Compila 'status' con lo stato ordine restituito dall'API (o 'ERROR[...]').
        """
        if isinstance(response_data, dict):
            response_data = [response_data]
        if saved_files is None:
            saved_files = []

        csv_path = self.order_request_folder / self.csv_filename
        if not csv_path.exists():
            print(f"CSV non trovato: {csv_path}")
            return {"updated": 0, "errors": len(response_data)}

        # Carica CSV
        with open(csv_path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # Indice archiveId -> idx riga
        index = {}
        for i, r in enumerate(rows):
            r.setdefault("orderId", "")
            r.setdefault("archiveId", "")
            r.setdefault("order_name", "")
            r.setdefault("status", "")
            r.setdefault("isImageDownloaded", "False")
            if r["archiveId"]:
                index[r["archiveId"]] = i

        updated = 0
        errors = 0

        for i, item in enumerate(response_data):
            archive_id = item.get("archiveId")
            if not archive_id or archive_id not in index:
                errors += 1
                continue

            row = rows[index[archive_id]]

            if item.get("status") == "ok":
                api_resp = item.get("response", {}) or {}
                # status dell'ordine restituito dall'API (es. CREATED/PROCESSING/PROCESSING_COMPLETE)
                api_status = api_resp.get("status", "") or "UNKNOWN"

                # Filename del JSON salvato (se disponibile)
                order_filename = ""
                if i < len(saved_files) and saved_files[i]:
                    order_filename = Path(saved_files[i]).name

                row["order_name"] = order_filename
                row["status"] = api_status
                row["orderId"] = item["response"]["id"]
                updated += 1
            else:
                code = item.get("code")
                row["status"] = f"ERROR{f'[{code}]' if code else ''}"
                errors += 1

        # Riscrivi CSV
        fieldnames = ["orderId", "archiveId", "order_name", "status", "isImageDownloaded"]
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(rows)

        print(f"CSV aggiornato: {csv_path} (updated={updated}, errors={errors})")
        return {"updated": updated, "errors": errors}

    def update_orders_csv_after_download(self, orderIds_to_download):
        csv_path = self.order_request_folder / self.csv_filename
        if not csv_path.exists():
            print(f"CSV non trovato: {csv_path}")

        updated = 0
        errors = 0
        with open(csv_path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            fieldnames = reader.fieldnames or []

        for r in rows:
            if r.get("orderId") in orderIds_to_download:
                r["isImageDownloaded"] = "True"
                updated += 1
            else:
                if not r.get("isImageDownloaded"):
                    r["isImageDownloaded"] = "False"

        try:
            with open(csv_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

        except Exception as e:
            print(f"Errore nel salvataggio del CSV: {e}")
            errors += 1

        print(f"CSV aggiornato: {csv_path} (updated={updated}, errors={errors})")
        return {"updated": updated, "errors": errors}

    def get_order_to_download(self, all=True) -> list:
        orderIds_to_download = []
        csv_path = self.order_request_folder / self.csv_filename
        if not csv_path.exists():
            print(f"CSV non trovato: {csv_path}")

        # Carica CSV
        with open(csv_path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        for r in rows:
            status = r.get("status", "")
            isImageDownloaded = r.get("isImageDownloaded", "False").strip().lower() == "true"

            if all:
                if status==self.status_for_download:
                    orderIds_to_download.append(r["orderId"])
            else:
                if status == self.status_for_download and not isImageDownloaded:
                    orderIds_to_download.append(r["orderId"])

        return orderIds_to_download