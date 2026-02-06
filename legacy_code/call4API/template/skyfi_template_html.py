from html import escape

class skyfi_template_html:
    def __init__(self, title, cards, stamp):
        self.title = title
        self.cards_html = ''.join(cards)
        self.stamp = stamp
        self.html = f"""<!doctype html>
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
  .tip {{ color:#666; font-size:12px; margin-top:10px }}
  #save-msg {{ font-size:12px; color:#0a7; margin-left:6px; }}
</style>
</head>
<body>
  <h2>{escape(title)}</h2>
  <div class="wrap">{self.cards_html}</div>

  <div class="tip">Suggerimento: clicca sulle miniature per aprirle in un nuovo tab. Spunta più immagini per creare la lista di <code>archiveId</code>.</div>

  <!-- Barra fissa -->
  <div class="bar">
    <div id="count"><b>0</b> selezionati</div>
    <button class="btn" id="copy">Copia</button>
    <button class="btn" id="csv">Scarica CSV</button>
    <button class="btn" id="json">Scarica JSON</button>
    <button class="btn" id="save">Salva TXT</button>
    <div class="idsbox" id="ids">[]</div>
    <span id="save-msg"></span>
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

// Bottoni
document.getElementById('copy').onclick = async () => {{
  const ids = getSelected();
  await navigator.clipboard.writeText(ids.join('\\n'));
  document.getElementById('copy').textContent = 'Copiato ✓';
  setTimeout(()=> document.getElementById('copy').textContent='Copia', 1000);
}};
document.getElementById('csv').onclick = () => {{
  const ids = getSelected();
  const lines = ['archiveId']; ids.forEach(id => lines.push(id));
  download('skyfi_selected_{self.stamp}.csv', lines.join('\\n'), 'text/csv');
}};
document.getElementById('json').onclick = () => {{
  const ids = getSelected();
  download('skyfi_selected_{self.stamp}.json', JSON.stringify({{archiveIds: ids}}, null, 2), 'application/json');
}};

// ===== Salva TXT (File System Access API se disponibile; fallback download) =====
async function saveSelectedTXT() {{
  const ids = getSelected();
  const content = ids.join('\\n');

  // File System Access API?
  if (window.showSaveFilePicker) {{
    try {{
      const handle = await window.showSaveFilePicker({{
        suggestedName: 'order_request_{self.stamp}.txt',
        types: [{{ description: 'Text', accept: {{ 'text/plain': ['.txt'] }} }}]
      }});
      const writable = await handle.createWritable();
      await writable.write(content);
      await writable.close();
      document.getElementById('save-msg').textContent = 'Salvato ✔';
      return;
    }} catch (err) {{
      // se l'utente annulla, cado nel fallback
    }}
  }}

  // Fallback: normale download in Download/
  download('order_request_{self.stamp}.txt', content, 'text/plain');
  document.getElementById('save-msg').textContent = 'Scaricato ✔';
}}

document.getElementById('save').addEventListener('click', saveSelectedTXT);
</script>
</body>
</html>"""

    @staticmethod
    def card_block(thumb, archiveId, provider, date, cloud, res, priceFullScene):
        img_html = (
            f'<a href="{escape(thumb)}" target="_blank"><img src="{escape(thumb)}" '
            f'alt="thumb" style="width:150px;height:150px;object-fit:cover;border-radius:12px;"></a>'
            if thumb else
            "<div style='width:150px;height:150px;background:#eee;border-radius:12px;"
            "display:flex;align-items:center;justify-content:center;'>no thumb</div>"
        )
        return f"""
        <div class="card">
          <label class="chk">
            <input type="checkbox" class="sel" value="{escape(archiveId)}">
            <span></span>
          </label>
          <div class="thumb">{img_html}</div>
          <div class="meta">
            <div><b>Prov</b>: {escape(str(provider))}</div>
            <div><b>Date</b>: {escape(date)}</div>
            <div><b>Cloud</b>: {escape(cloud)}</div>
            <div><b>Res</b>: {escape(str(res))}</div>
            <div><b>Image Price</b>: {escape(str(priceFullScene))}</div>
          </div>
        </div>"""

    def get_template(self):
        return self.html
