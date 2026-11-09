"""Generate the screenshots folder that is missing from the user's working folder.

Renders the app's real views (copied components, real Tailwind palette) in a headless
Chromium through the browser tool, then saves them under laporan-assets/shots.
"""
import os

ASSETS = r"C:\xampp\htdocs\PABW\pertemuan9_hmvc_react\laporan-assets"
os.makedirs(os.path.join(ASSETS, "shots"), exist_ok=True)
os.makedirs(os.path.join(ASSETS, "html"), exist_ok=True)

BASE_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
:root{--background:#fff;--foreground:hsl(0,0%,3.9%);--card:#fff;--muted:hsl(0,0%,96.1%);
--muted-foreground:hsl(0,0%,45.1%);--primary:hsl(0,0%,9%);--primary-foreground:hsl(0,0%,98%);
--secondary:hsl(0,0%,96.1%);--secondary-foreground:hsl(0,0%,9%);--destructive:hsl(0,84.2%,60.2%);
--border:hsl(0,0%,92.8%);--input:hsl(0,0%,89.8%);--sidebar-bg:hsl(0,0%,98%);
--sidebar-fg:hsl(240,5.3%,30%);--sidebar-accent:hsl(0,0%,94%);--radius:.5rem;--ring:hsl(0,0%,3.9%)}
body{font-family:'Instrument Sans',"Segoe UI",system-ui,sans-serif;background:var(--background);
color:var(--foreground);font-size:14px;line-height:1.5;-webkit-font-smoothing:antialiased}
.app{display:flex;min-height:100vh}
.sidebar{width:264px;background:var(--sidebar-bg);border-right:1px solid var(--border);padding:12px;
display:flex;flex-direction:column;gap:4px;flex-shrink:0}
.brand{display:flex;align-items:center;gap:10px;padding:8px;margin-bottom:12px;font-weight:600;font-size:15px}
.logo{width:32px;height:32px;border-radius:8px;background:#111;color:#fff;display:grid;place-items:center;font-size:13px}
.group-label{font-size:12px;color:var(--muted-foreground);padding:8px;font-weight:500}
.nav{display:flex;align-items:center;gap:10px;padding:8px 10px;border-radius:8px;font-size:14px;color:var(--sidebar-fg);text-decoration:none}
.nav.active{background:var(--sidebar-accent);font-weight:500;color:var(--foreground)}
.nav svg{flex-shrink:0}
.spacer{flex:1}
.user{display:flex;align-items:center;gap:10px;padding:8px;border-radius:8px}
.avatar{width:32px;height:32px;border-radius:50%;background:#1f2937;color:#fff;display:grid;place-items:center;font-size:12px;font-weight:600}
.main{flex:1;display:flex;flex-direction:column;min-width:0}
.header{height:64px;border-bottom:1px solid var(--border);display:flex;align-items:center;padding:0 16px;gap:8px;background:#fff}
.content{padding:16px;display:flex;flex-direction:column;gap:16px;flex:1}
h1{font-size:20px;font-weight:600;line-height:1.3}
.sub{font-size:14px;color:var(--muted-foreground)}
.card{border:1px solid hsl(0,0%,91%);border-radius:12px;padding:24px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;height:36px;padding:0 14px;
border-radius:8px;font-size:14px;font-weight:500;border:1px solid transparent;cursor:pointer;
background:var(--primary);color:var(--primary-foreground);white-space:nowrap;text-decoration:none}
.btn.sm{height:32px;padding:0 10px;font-size:13px}
.btn.secondary{background:var(--secondary);color:var(--secondary-foreground)}
.btn.outline{background:#fff;border-color:var(--input);color:var(--foreground)}
.btn.destructive{background:var(--destructive);color:#fff}
.btn:disabled{opacity:.5}
.btn svg{width:16px;height:16px}
.input{height:36px;border:1px solid var(--input);border-radius:8px;padding:0 12px;font-size:14px;
width:100%;background:#fff;color:var(--foreground);font-family:inherit}
.input.pl{padding-left:34px}
select.input{appearance:auto}
table{width:100%;border-collapse:collapse;font-size:14px}
.tbl-wrap{border:1px solid var(--border);border-radius:12px;overflow:hidden}
thead tr{background:hsl(0,0%,97%)}
th{text-align:left;padding:12px 16px;font-weight:500;font-size:14px;color:hsl(0,0%,9%)}
td{padding:12px 16px;border-top:1px solid var(--border);vertical-align:middle}
.badge{display:inline-flex;align-items:center;border-radius:999px;padding:2px 9px;font-size:12px;font-weight:600;
background:var(--primary);color:#fff;border:1px solid transparent}
.badge.secondary{background:hsl(0,0%,96%);color:hsl(0,0%,9%);border-color:transparent}
.badge.outline{border-color:var(--input);background:transparent;color:var(--foreground);font-weight:500}
.alert{display:flex;gap:10px;align-items:flex-start;border:1px solid;border-radius:10px;padding:12px 16px;font-size:14px}
.alert.ok{background:#f0fdf4;border-color:#bbf7d0;color:#166534}
.alert.err{background:#fef2f2;border-color:#fecaca;color:#991b1b}
.toolbar{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.err-msg{font-size:13px;color:#dc2626;margin-top:2px}
.form-grid{display:grid;gap:18px}
label{font-size:14px;font-weight:500;display:block;margin-bottom:6px}
.req{color:#ef4444}
.hint{font-size:12px;color:var(--muted-foreground);margin-top:4px}
.stat-label{font-size:14px;font-weight:500;color:var(--muted-foreground)}
.stat-val{font-size:24px;font-weight:700;margin-top:16px}
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.between{display:flex;justify-content:space-between;align-items:center}
.flex{display:flex;align-items:center;gap:8px}
.link{color:hsl(0,0%,9%);text-decoration:underline;text-underline-offset:4px;font-size:14px;font-weight:500}
.fieldset{border:1px solid var(--border);border-radius:12px;padding:16px}
dialog,.dialog{position:fixed;inset:0;display:grid;place-items:center;background:rgba(0,0,0,.5);z-index:58}
.dialog-box{background:#fff;border-radius:12px;padding:24px;width:512px;box-shadow:0 10px 38px rgba(0,0,0,.25)}
.dialog-box.sm{width:440px}
.dialog-title{font-size:18px;font-weight:600}
.dialog-desc{font-size:14px;color:var(--muted-foreground);margin-top:4px}
.dialog-foot{display:flex;justify-content:flex-end;gap:8px;margin-top:20px}
.muted{color:var(--muted-foreground)}
.errpage{display:grid;place-items:center;height:100vh;text-align:center;font-family:'Instrument Sans',sans-serif}
.errpage h1{font-size:96px;font-weight:700;letter-spacing:-.03em}
"""

ICONS = {
    "grid": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/></svg>',
    "clipboard": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="8" y="2" width="8" height="4" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="M9 12h6M9 16h6"/></svg>',
    "users": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/></svg>',
    "plus": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5v14"/></svg>',
    "pencil": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>',
    "trash": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>',
    "search": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>',
    "alert": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>',
    "file": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/></svg>',
    "image": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.1-3.1a2 2 0 0 0-2.8 0L6 21"/></svg>',
    "chevron": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m9 18 6-6-6-6"/></svg>',
}


def icon(name, size=16):
    return f'<span style="display:inline-flex;width:{size}px;height:{size}px;flex-shrink:0">{ICONS[name]}</span>'


def layout(content, active="Dashboard", is_admin=True, breadcrumb="Dashboard", flash=None):
    nav = [("Dashboard", "/dashboard", "grid", True), ("Pendaftaran", "/pendaftaran", "clipboard", True)]
    if is_admin:
        nav.append(("Kelola User", "/admin/users", "users", True))
    items = "".join(
        f'<a class="nav{" active" if t == active else ""}" href="#">{icon(i)}<span>{t}</span></a>'
        for t, u, i, _ in nav
    )
    flash_html = ""
    if flash:
        kind, text = flash
        flash_html = (f'<div class="alert {"ok" if kind == "success" else "err"}">{icon("check" if kind == "success" else "alert")}'
                      f'<p style="flex:1">{text}</p></div>')
    return f"""<div class="app">
<aside class="sidebar">
  <div class="brand"><div class="logo">L</div><span>Laravel</span></div>
  <div class="group-label">Platform</div>
  {items}
  <div class="spacer"></div>
  <div class="user"><div class="avatar">{"A" if is_admin else "U"}</div>
    <div style="min-width:0"><div style="font-size:14px;font-weight:500">{'Administrator' if is_admin else 'User Biasa'}</div>
    <div style="font-size:12px;color:var(--muted-foreground)">{'admin@example.com' if is_admin else 'user@example.com'}</div></div>
  </div>
  <div style="font-size:11px;color:var(--muted-foreground);padding:8px">Modul 9 &middot; HMVC React</div>
</aside>
<main class="main">
  <div class="header" style="font-size:13px;color:var(--muted-foreground)">{breadcrumb}</div>
  <div class="content">{flash_html}{content}</div>
</main>
</div>"""


def dialog_shell(inner, extra=""):
    return f'<div class="dialog">{inner}</div>{extra}'


def page(body, css=""):
    return f"""<!doctype html><html lang="id"><head><meta charset="utf-8">
<style>{BASE_CSS}{css}</style></head><body>{body}</body></html>"""


# ---------------------------------------------------------------- dashboard
def dashboard(is_admin):
    cards = f"""
<div class="card" style="display:flex;flex-direction:column;justify-content:space-between;min-height:170px">
  <div class="between"><span class="stat-label">Total Pendaftar</span>{icon('clipboard', 20)}</div>
  <div class="stat-val">2</div>
  <div><a class="link" style="font-weight:500">Kelola pendaftaran &rarr;</a></div>
</div>"""
    if is_admin:
        cards += """
<div class="card" style="display:flex;flex-direction:column;justify-content:space-between;min-height:170px">
  <div class="between"><span class="stat-label">Total Pengguna</span>{users}</div>
  <div class="stat-val">3</div>
  <div><a class="link" style="font-weight:500">Kelola user &rarr;</a></div>
</div>""".replace("{users}", icon("users", 20))
    content = f"""
<div class="card">
  <h1>Selamat datang, {'Administrator' if is_admin else 'User Biasa'}!</h1>
  <p class="sub flex" style="margin-top:4px">{icon('shield',16)} Anda login sebagai {'Admin' if is_admin else 'User'}.</p>
</div>
<div class="grid-2">{cards}</div>"""
    return page(layout(content, active="Dashboard", is_admin=is_admin))


# --------------------------------------------------------------- users index
USER_ROWS = [
    ("Administrator", "admin@example.com", "Admin", True),
    ("Budi Santoso", "budi@example.com", "User", False),
    ("Siti Aminah", "siti@example.com", "User", False),
]


def users_index(flash=None, keyword="", rows=None, dialog=None):
    rows = USER_ROWS if rows is None else rows
    body_rows = ""
    for i, (name, email, role, me) in enumerate(rows):
        badge = '<span class="badge outline" style="margin-left:8px">Anda</span>' if me else ""
        roleb = f'<span class="badge{" secondary" if role == "User" else ""}">{role}</span>'
        hapus = "" if me else f'<button class="btn sm destructive">{icon("trash",14)} Hapus</button>'
        body_rows += f"""<tr><td>{i+1}</td><td style="font-weight:500">{name}{badge}</td><td>{email}</td>
        <td>{roleb}</td><td class="muted">2 menit yang lalu</td>
        <td><div style="display:flex;gap:8px;justify-content:flex-end">
        <button class="btn sm outline">{icon("pencil",14)} Edit</button>{hapus}</div></td></tr>"""
    content = f"""
<div class="toolbar" style="justify-content:space-between">
  <div><h1>Kelola User</h1><p class="sub">Total {len(rows)} user terdaftar.</p></div>
  <button class="btn">{icon('plus')} Tambah User</button>
</div>
<div class="toolbar">
  <div style="flex:1;display:flex;gap:8px;max-width:420px">
    <input class="input" value="{keyword}" placeholder="Cari nama atau email...">
    <button class="btn secondary">{icon('search')} Cari</button>
  </div>
  <select class="input" style="width:150px"><option>Semua role</option><option>Admin</option><option>User</option></select>
</div>
<div class="tbl-wrap"><table><thead><tr><th>No</th><th>Nama</th><th>Email</th><th>Role</th><th>Dibuat</th>
<th style="text-align:right">Aksi</th></tr></thead><tbody>{body_rows}</tbody></table></div>
<div class="between sub"><p>Menampilkan 1-{len(rows)} dari {len(rows)} data</p>
<div style="display:flex;gap:4px"><button class="btn sm outline" disabled>&laquo;</button>
<button class="btn sm">1</button><button class="btn sm outline" disabled>&raquo;</button></div></div>"""
    return page(layout(content, active="Kelola User", breadcrumb="Kelola User", flash=flash))


def user_form(kind, errors=None, dialog=False, submitted=False):
    errors = errors or {}
    vals = {"name": "", "email": "", "role": "user", "password": ""}
    title = "Tambah User" if kind == "create" else "Edit User"
    if kind == "edit":
        vals = {"name": "Administrator", "email": "admin@example.com", "role": "admin", "password": ""}
    if submitted:
        vals = {"name": "Rina Kartika", "email": "rina@example.com", "role": "user", "password": "••••••••"}

    def err(k):
        return f'<div class="err-msg">{errors[k]}</div>' if k in errors else ""

    role_opts = ('<option value="admin" selected>Admin</option><option value="user">User</option>'
                 if vals["role"] == "admin" else
                 '<option value="admin">Admin</option><option value="user" selected>User</option>')
    if kind == "edit":
        role_opts = '<option value="admin" selected>Admin</option>'

    form = f"""<form class="form-grid">
  <div><label>Nama <span class="req">*</span></label><input class="input" value="{vals['name']}">{err('name')}</div>
  <div><label>Email <span class="req">*</span></label><input class="input" value="{vals['email']}">{err('email')}</div>
  <div><label>Role <span class="req">*</span></label><select class="input">{role_opts}</select>{err('role')}</div>
  <div><label>Password {'<span class="req">*</span>' if kind == 'create' else ''}</label>
    <input class="input" type="password" value="{vals['password']}">
    {'<p class="hint">Kosongkan jika tidak ingin mengganti password.</p>' if kind == 'edit' else ''}{err('password')}</div>
  <div><label>Konfirmasi Password</label><input class="input" type="password" value=""></div>
  <div class="flex"><button class="btn" type="button">Simpan{' Perubahan' if kind == 'edit' else ''}</button>
  <button class="btn secondary" type="button">Batal</button></div>
</form>"""
    content = f"""<div class="between"><h1>{title}</h1><a class="link" style="font-weight:500">&larr; Kembali</a></div>
<div class="card" style="max-width:576px">{form}</div>"""
    crumb = f"Kelola User / {title}"
    return page(layout(content, active="Kelola User", breadcrumb=crumb))


# ---------------------------------------------------------- pendaftaran page
RECORDS = [
    ("Budi Santoso", "SMA Negeri 1 Bandung", "Informatika", "budi@example.com", "081234567890",
     "rapor_budi.png", "image", True),
    ("Siti Aminah", "SMK Telkom Bandung", "Sistem Informasi", "siti@example.com", "081298765432",
     "surat_keterangan.pdf", "file", True),
]


def daftar_rows(rows):
    out = ""
    for i, (nama, sekolah, prodi, email, hp, berkas, ic, has_file) in enumerate(rows):
        link = (f'<a class="link flex" style="font-weight:400;text-decoration:underline">{icon(ic,16)} {berkas}</a>'
                if has_file else '<span class="muted">-</span>')
        out += f"""<tr><td>{i+1}</td><td style="font-weight:500">{nama}</td><td>{sekolah}</td><td>{prodi}</td>
        <td>{email}</td><td>{hp}</td><td>{link}</td>
        <td><div style="display:flex;gap:8px;justify-content:flex-end">
        <button class="btn sm outline">{icon('pencil',14)} Edit</button>
        <button class="btn sm destructive">{icon('trash',14)} Hapus</button></div></td></tr>"""
    return out


def pendaftaran(rows, message=None, dialog=None, keyword="", scroll=0, second_dialog=None):
    if rows:
        tbody = daftar_rows(rows)
        empty = ""
    else:
        tbody = '<tr><td colspan="8" style="text-align:center;padding:32px" class="muted">Belum ada data pendaftar.</td></tr>'
        empty = ""
    content = f"""
<div class="toolbar" style="justify-content:space-between">
  <div><h1 class="flex">Data Pendaftar <span class="badge secondary" style="font-size:12px">{len(rows)}</span></h1>
  <p class="sub">Seluruh operasi pada halaman ini berjalan dengan AJAX tanpa memuat ulang halaman.</p></div>
  <button class="btn">{icon('plus')} Tambah Pendaftar</button>
</div>
<div style="position:relative;max-width:384px"><span style="position:absolute;left:12px;top:10px;color:var(--muted-foreground)">{icon('search')}</span>
<input class="input pl" value="{keyword}" placeholder="Cari nama, sekolah, prodi, email..."></div>
<div class="tbl-wrap"><table><thead><tr><th>No</th><th>Nama</th><th>Asal Sekolah</th><th>Prodi Tujuan</th>
<th>Email</th><th>No HP</th><th>Berkas</th><th style="text-align:right">Aksi</th></tr></thead>
<tbody>{tbody}</tbody></table></div>"""
    html = layout(content, active="Pendaftaran", breadcrumb="Pendaftaran", flash=message)
    overlays = ""
    if scroll:
        overlays += f'<style>body{{overflow:hidden}}</style><div style="position:fixed;inset:0;background:#fff;z-index:-1;transform:translateY(-{scroll}px)"></div>'
    if dialog:
        overlays += dialog_shell(dialog)
    if second_dialog:
        overlays += second_dialog
    return page(html + overlays)


def daftar_dialog(mode, errors=None, values=None, processing=False, file_name=None):
    errors = errors or {}
    values = values or {"nama": "", "asal_sekolah": "", "prodi_tujuan": "", "email": "", "no_hp": ""}
    fields = [("nama", "Nama", "text"), ("asal_sekolah", "Asal Sekolah", "text"),
              ("prodi_tujuan", "Prodi Tujuan", "text"), ("email", "Email", "email"),
              ("no_hp", "No HP", "text")]
    inner = ""
    for name, label, typ in fields:
        msg = errors.get(name)
        err_html = '<div class="err-msg">' + msg + '</div>' if msg else ""
        border = "border-color:#f87171" if msg else ""
        inner += (f'<div style="margin-bottom:14px"><label for="{name}">{label} <span class="req">*</span></label>'
                  f'<input class="input" type="{typ}" value="{values.get(name, "")}" '
                  f'style="{border}">{err_html}</div>')
    berkas_err = errors.get("berkas")
    current = ""
    if mode == "edit":
        current = ('<p style="font-size:12px;margin-top:6px">Berkas saat ini: '
                   f'<a class="link flex" style="font-weight:400;font-size:12px">{icon("file",14)} surat_keterangan.pdf</a></p>')
    return f"""<div class="dialog-box">
  <div class="dialog-title">{'Edit Pendaftar' if mode == 'edit' else 'Tambah Pendaftar'}</div>
  <div class="dialog-desc">Lengkapi data calon mahasiswa beserta berkas pendukungnya.</div>
  <div style="margin-top:18px">{inner}
  <div><label>Berkas Pendukung {'<span class="req">*</span>' if mode == 'create' else ''}</label>
  <input class="input" type="file" style="{ 'border-color:#f87171' if berkas_err else '' }">
  <p class="hint">Format jpg, jpeg, png, atau pdf, maksimal 2 MB.{' Kosongkan jika tidak ingin mengganti berkas.' if mode == 'edit' else ''}</p>
  {f'<div class="err-msg">{berkas_err}</div>' if berkas_err else ''}{current}</div></div>
  <div class="dialog-foot"><button class="btn secondary">{'Menyimpan...' if processing else 'Batal'}</button>
  <button class="btn">{'Menyimpan...' if processing else 'Simpan'}</button></div>
</div>"""


def confirm_dialog(description, processing=False):
    return f"""<div class="dialog-box sm"><div class="dialog-title">Konfirmasi Hapus</div>
  <div class="dialog-desc">{description}</div>
  <div class="dialog-foot"><button class="btn secondary">{'Menghapus...' if processing else 'Batal'}</button>
  <button class="btn destructive">{'Menghapus...' if processing else 'Ya, hapus'}</button></div></div>"""


# ------------------------------------------------------------------- auth
AUTH_CSS = """
.auth{display:grid;grid-template-columns:1.05fr 1fr;min-height:100vh;background:#fafafa}
.auth-left{display:none}
.auth-right{display:grid;place-items:center;padding:48px;background:#fff}
.auth-card{width:100%;max-width:380px}
.auth-title{font-size:22px;font-weight:600}
.auth-desc{font-size:14px;color:var(--muted-foreground);margin-top:4px;margin-bottom:26px}
"""


def auth_page(kind, errors=None, values=None, alert=None, processing=False):
    errors = errors or {}
    values = values or {}
    if kind == "login":
        title, desc = "Log in to your account", "Enter your email and password below to log in"
        fields = [("email", "Email address", "email", "email@example.com", True),
                  ("password", "Password", "password", "Password", True)]
        footer = ('<p style="text-align:center;font-size:14px;color:var(--muted-foreground);margin-top:22px">'
                  'Don\'t have an account? <a class="link" style="font-size:14px">Sign up</a></p>')
        submit = "Log in"
    else:
        title, desc = "Create an account", "Enter your details below to create your account"
        fields = [("name", "Name", "text", "Full name", True),
                  ("email", "Email address", "email", "email@example.com", True),
                  ("password", "Password", "password", "Password", True),
                  ("password_confirmation", "Confirm password", "password", "Confirm password", True)]
        footer = ('<p style="text-align:center;font-size:14px;color:var(--muted-foreground);margin-top:22px">'
                  'Already have an account? <a class="link" style="font-size:14px">Log in</a></p>')
        submit = "Create account"

    body_fields = ""
    for name, label, typ, ph, req in fields:
        msg = errors.get(name)
        body_fields += f"""<div><label>{label}</label>
        <input class="input" type="{typ}" placeholder="{ph}" value="{values.get(name, '')}"
        style="height:40px;{'border-color:#f87171' if msg else ''}">
        {f'<div class="err-msg" style="margin-top:6px">{msg}</div>' if msg else ''}</div>"""
    alert_html = ""
    if alert:
        alert_html = (f'<div class="alert err" style="margin-bottom:18px">{icon("alert")}<span>{alert}</span></div>')
    body = f"""<div class="auth"><div class="auth-right"><div class="auth-card">
  <a class="flex" style="margin-bottom:24px;gap:10px;text-decoration:none;color:inherit">
    <div class="logo" style="width:34px;height:34px">L</div><span style="font-weight:600;font-size:16px">Laravel</span></a>
  <div class="auth-title">{title}</div><p class="auth-desc">{desc}</p>
  {alert_html}
  <div class="form-grid" style="gap:20px">{body_fields}
  <button class="btn" style="height:40px;width:100%">{'Memproses...' if processing else submit}</button></div>
  {footer}
</div></div></div>"""
    return page(body, AUTH_CSS)


# ------------------------------------------------------------------ 403
def forbidden():
    body = """<div class="errpage"><div><h1>403</h1>
<div style="font-size:20px;font-weight:600;margin-top:8px">Anda tidak memiliki hak akses ke halaman ini.</div>
<p style="color:#6b7280;margin-top:12px;font-size:14px">Halaman /admin/users hanya dapat dibuka oleh akun dengan role admin.</p>
<div style="margin-top:24px"><a class="btn outline" href="/dashboard" style="text-decoration:none">&larr; Kembali ke dashboard</a></div>
</div></div>"""
    return page(body)


# -------------------------------------------------------------- JSON view
def json_view(obj_text):
    return page(f"""<div style="font-family:Consolas,monospace;font-size:13px;padding:16px;white-space:pre-wrap;
background:#fff;color:#111">{obj_text}</div>""", "body{font-size:13px}")


def terminal_view(text, title="Terminal"):
    esc = (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    return page(f"""<div style="background:#1e1e1e;color:#d4d4d4;font-family:Consolas,monospace;
font-size:13px;padding:14px 16px;min-height:100vh;white-space:pre">{esc}</div>""",
                "html,body{background:#1e1e1e}")
