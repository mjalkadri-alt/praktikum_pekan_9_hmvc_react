"""Generate the .docx practicum report for Modul 9 (HMVC Starterkit React).

Matches the sibling submission 'LAPORAN PRAKTIKUM MODUL 9 - HMVC Starterkit React.pdf':
A4, 2.54 cm margins, Times New Roman, 12 pt, 1.15 spacing, sections A-G,
screenshots for code, figures numbered continuously with captions below.
"""
import os
import re
import sys

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SHOTS = os.path.join(HERE, "shots")
CODE = os.path.join(HERE, "code")
LOGO = os.path.join(HERE, "logo.png")
OUT = os.path.join(ROOT, "LAPORAN PRAKTIKUM MODUL 9 - HMVC STARTKIT REACT.docx")

BODY_FONT = "Times New Roman"
MONO = "Consolas"

code_counter = [0]
fig_counter = [0]


# --------------------------------------------------------------------------- document setup
def new_document():
    doc = Document()
    sec = doc.sections[0]
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    for attr in ("top_margin", "bottom_margin", "left_margin", "right_margin"):
        setattr(sec, attr, Cm(2.54))

    normal = doc.styles["Normal"]
    normal.font.name = BODY_FONT
    normal.font.size = Pt(12)
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), BODY_FONT)
    pf = normal.paragraph_format
    pf.line_spacing = 1.12
    pf.space_after = Pt(5)
    pf.space_before = Pt(0)
    return doc


def add_page_number(par):
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = par.add_run()
    run.font.size = Pt(9)
    run.font.name = BODY_FONT
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    r = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), "18")
    rpr.append(sz)
    r.append(rpr)
    t = OxmlElement("w:t")
    t.text = "1"
    r.append(t)
    fld.append(r)
    par._p.append(fld)


# --------------------------------------------------------------------------- text helpers
def p(doc, text, indent=False, align="justify", space_after=6, italic=False, bold=False, size=12):
    par = doc.add_paragraph()
    par.paragraph_format.space_after = Pt(space_after)
    par.alignment = {
        "justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
        "center": WD_ALIGN_PARAGRAPH.CENTER,
        "left": WD_ALIGN_PARAGRAPH.LEFT,
    }[align]
    _rich(par, text, italic=italic, bold=bold, size=size)
    return par


def _rich(par, text, italic=False, bold=False, size=12):
    """Support **bold** and `mono` inline markers."""
    for chunk in re.split(r"(\*\*[^*]+\*\*|`[^`]+`)", text):
        if not chunk:
            continue
        if chunk.startswith("**") and chunk.endswith("**"):
            r = par.add_run(chunk[2:-2])
            r.bold = True
        elif chunk.startswith("`") and chunk.endswith("`"):
            r = par.add_run(chunk[1:-1])
            r.font.name = MONO
            r._element.rPr.rFonts.set(qn("w:eastAsia"), MONO)
            r.font.size = Pt(10.5)
        else:
            r = par.add_run(chunk)
            if bold:
                r.bold = True
        r.font.size = Pt(size)
        if italic:
            r.italic = True
    return par


def h1(doc, text, space_before=14):
    par = doc.add_paragraph()
    par.paragraph_format.space_before = Pt(space_before)
    par.paragraph_format.space_after = Pt(6)
    par.paragraph_format.keep_with_next = True
    r = par.add_run(text)
    r.bold = True
    r.font.size = Pt(14)
    r.font.name = BODY_FONT
    r._element.rPr.rFonts.set(qn("w:eastAsia"), BODY_FONT)
    return par


def h2(doc, text):
    par = doc.add_paragraph()
    par.paragraph_format.space_before = Pt(10)
    par.paragraph_format.space_after = Pt(4)
    par.paragraph_format.keep_with_next = True
    r = par.add_run(text)
    r.bold = True
    r.font.size = Pt(12)
    r.font.name = BODY_FONT
    r._element.rPr.rFonts.set(qn("w:eastAsia"), BODY_FONT)
    return par


def bullet(doc, text, level=0):
    par = doc.add_paragraph(style="List Bullet")
    par.paragraph_format.space_after = Pt(3)
    par.paragraph_format.left_indent = Cm(0.75 + 0.6 * level)
    par.paragraph_format.line_spacing = 1.15
    _rich(par, text)
    return par


_DEFINITIONS = [None]


def numbered(doc, items, restart=True):
    """Numbered list using a dedicated w:num so each call restarts at 1."""
    numbering = doc.part.numbering_part.element
    if _DEFINITIONS[0] is None:
        abs_ids = [int(a.get(qn("w:abstractNumId"))) for a in numbering.findall(qn("w:abstractNum"))]
        num_ids = [int(n.get(qn("w:numId"))) for n in numbering.findall(qn("w:num"))]
        _DEFINITIONS[0] = (max(abs_ids) + 1 if abs_ids else 0, max(num_ids) + 1 if num_ids else 1, 0)

    base_abs, base_num, calls = _DEFINITIONS[0]
    new_abs = base_abs + calls
    new_num = base_num + calls
    _DEFINITIONS[0] = (base_abs, base_num, calls + 1)

    abs_el = OxmlElement("w:abstractNum")
    abs_el.set(qn("w:abstractNumId"), str(new_abs))
    lvl = OxmlElement("w:lvl")
    lvl.set(qn("w:ilvl"), "0")
    for tag, val in (("w:start", "1"), ("w:numFmt", "decimal"), ("w:lvlText", "%1."), ("w:lvlJc", "left")):
        el = OxmlElement(tag)
        el.set(qn("w:val"), val)
        lvl.append(el)
    ppr = OxmlElement("w:pPr")
    ind = OxmlElement("w:ind")
    ind.set(qn("w:left"), "482")
    ind.set(qn("w:hanging"), "360")
    ppr.append(ind)
    lvl.append(ppr)
    abs_el.append(lvl)
    numbering.insert(0, abs_el)

    num_el = OxmlElement("w:num")
    num_el.set(qn("w:numId"), str(new_num))
    ref = OxmlElement("w:abstractNumId")
    ref.set(qn("w:val"), str(new_abs))
    num_el.append(ref)
    numbering.append(num_el)

    for item in items:
        par = doc.add_paragraph(style="List Number")
        par.paragraph_format.space_after = Pt(3)
        par.paragraph_format.line_spacing = 1.15
        ppr_par = par._p.get_or_add_pPr()
        for old in ppr_par.findall(qn("w:numPr")):
            ppr_par.remove(old)
        num_pr = OxmlElement("w:numPr")
        ilvl = OxmlElement("w:ilvl")
        ilvl.set(qn("w:val"), "0")
        nid = OxmlElement("w:numId")
        nid.set(qn("w:val"), str(new_num))
        num_pr.append(ilvl)
        num_pr.append(nid)
        ppr_par.append(num_pr)
        _rich(par, item)


# --------------------------------------------------------------------------- code + figures
def code_block(doc, name, caption):
    """Insert a dark editor-style code screenshot with a numbered caption."""
    code_counter[0] += 1
    path = os.path.join(CODE, name + ".png")
    w, h = Image.open(path).size
    width_cm = 15.0
    if width_cm * h / w > 20.0:
        width_cm = 20.0 * w / h
    par = doc.add_paragraph()
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    par.paragraph_format.space_before = Pt(6)
    par.paragraph_format.space_after = Pt(2)
    par.paragraph_format.line_spacing = 1.0
    par.paragraph_format.keep_with_next = True
    par.add_run().add_picture(path, width=Cm(width_cm))
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_after = Pt(8)
    cap.paragraph_format.line_spacing = 1.0
    r = cap.add_run(f"Kode {code_counter[0]}. {caption}")
    r.font.size = Pt(10)


def figure(doc, name, caption, width_cm=15.5, max_h=19.0):
    fig_counter[0] += 1
    path = os.path.join(SHOTS, name + ".png")
    w, h = Image.open(path).size
    width = width_cm
    if width * h / w > max_h:
        width = max_h * w / h
    par = doc.add_paragraph()
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    par.paragraph_format.space_before = Pt(6)
    par.paragraph_format.space_after = Pt(2)
    par.paragraph_format.line_spacing = 1.0
    par.paragraph_format.keep_with_next = True
    par.add_run().add_picture(path, width=Cm(width))
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_after = Pt(8)
    cap.paragraph_format.line_spacing = 1.0
    r = cap.add_run(f"Gambar {fig_counter[0]}. {caption}")
    r.font.size = Pt(10)
    return fig_counter[0]


def set_cell_bg(cell, hex_color):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tc_pr.append(shd)


def table(doc, header, rows, widths=None, font_size=10, caption=None):
    tbl = doc.add_table(rows=1, cols=len(header))
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = tbl.rows[0].cells
    for i, text in enumerate(header):
        set_cell_bg(hdr[i], "D9E2F3")
        par = hdr[i].paragraphs[0]
        par.paragraph_format.space_after = Pt(2)
        par.paragraph_format.line_spacing = 1.0
        r = par.add_run(text)
        r.bold = True
        r.font.size = Pt(font_size)
        r.font.name = BODY_FONT
    for row in rows:
        cells = tbl.add_row().cells
        for i, text in enumerate(row):
            par = cells[i].paragraphs[0]
            par.paragraph_format.space_after = Pt(2)
            par.paragraph_format.line_spacing = 1.0
            _rich(par, text, size=font_size)
    if widths:
        for row in tbl.rows:
            for i, w in enumerate(widths):
                row.cells[i].width = Cm(w)
    if caption:
        cap = doc.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap.paragraph_format.space_before = Pt(4)
        cap.paragraph_format.space_after = Pt(8)
        r = cap.add_run(caption)
        r.font.size = Pt(10)
        r.italic = True
    else:
        doc.add_paragraph().paragraph_format.space_after = Pt(4)
    return tbl


# --------------------------------------------------------------------------- cover
def cover(doc):
    sec = doc.sections[0]
    p(doc, "", space_after=0)

    def line(text, size, bold=False, after=0, before=0, mono=False):
        par = doc.add_paragraph()
        par.alignment = WD_ALIGN_PARAGRAPH.CENTER
        par.paragraph_format.space_after = Pt(after)
        par.paragraph_format.space_before = Pt(before)
        par.paragraph_format.line_spacing = 1.0
        r = par.add_run(text)
        r.bold = bold
        r.font.size = Pt(size)
        r.font.name = MONO if mono else BODY_FONT

    line("LAPORAN PRAKTIKUM TUGAS AKHIR PENGEMBANGAN", 16, True, after=0)
    line("APLIKASI BERBASIS WEB", 16, True, after=10)
    line("Modul 9: HMVC, Authorization, dan AJAX", 12, after=0)
    line("dengan React pada Laravel", 12, after=0)

    par = doc.add_paragraph()
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    par.paragraph_format.space_before = Pt(24)
    par.paragraph_format.space_after = Pt(24)
    par.add_run().add_picture(LOGO, width=Cm(3.9))

    line("Disusun Oleh:", 14, after=12)
    line("Nama: Dryhus Dzacky Damingtyas.S", 14, after=6)
    line("NIM: 707012530010", 14, after=6)
    line("Kelas: D4SIKC-49-04", 14, after=12)
    line("Mata Kuliah: Pengembangan Aplikasi Berbasis Web", 14, after=12)
    line("Dosen Pengampu: ...................................................", 14, after=40)
    line("UNIVERSITAS TELKOM", 16, True, after=2)
    line("FAKULTAS ILMU TERAPAN", 16, True, after=2)
    line("D4 SISTEM INFORMASI KOTACERDAS", 16, True, after=2)
    line("TAHUN AKADEMIK 2026/2027", 14, after=0)

    par = doc.add_paragraph()
    par.add_run().add_break(WD_BREAK.PAGE)


# --------------------------------------------------------------------------- content
def build():
    doc = new_document()
    cover(doc)

    # ------------------------------------------------------------------ A. Tujuan
    h1(doc, "A. Tujuan Praktikum", space_before=0)
    p(doc, "Praktikum ini saya kerjakan untuk membangun aplikasi penerimaan mahasiswa baru pada project "
           "`pertemuan9_hmvc_react` dengan arsitektur HMVC memakai React Starter Kit. Berbeda dengan Modul 8 "
           "yang menulis tampilan dengan Blade dan jQuery, seluruh halaman modul pada praktikum ini ditulis "
           "dengan React dan dihubungkan ke Laravel melalui Inertia.js. Modul UserManagement dikerjakan dengan "
           "CRUD Inertia, sedangkan modul Pendaftaran dikerjakan dengan CRUD AJAX serta upload berkas. Hak akses "
           "setiap halaman dibatasi oleh role admin dan user yang diperiksa middleware di sisi server.")
    p(doc, "Secara lebih rinci, tujuan yang ingin dicapai pada praktikum ini adalah:")
    numbered(doc, [
        "Menyiapkan project Laravel React Starter Kit, memasang paket `nwidart/laravel-modules` beserta "
        "merge-plugin pada `composer.json`, dan membuat dua modul HMVC untuk fitur UserManagement dan Pendaftaran.",
        "Mengatur agar Inertia dapat menemukan halaman React yang berada di dalam folder modul melalui fungsi "
        "`resolve` pada `app.tsx`, serta mendaftarkan folder modul pada Tailwind CSS dan `tsconfig.json`.",
        "Menambahkan kolom role pada tabel `users`, membuat enum `UserRole`, factory, dan seeder, lalu menyesuaikan "
        "proses register agar akun hasil register selalu berperan user.",
        "Membagikan data auth dan flash ke seluruh halaman React sebagai shared props, lalu membuat hook "
        "`useSharedProps` serta komponen `AlertMessage`, `FlashMessage`, dan `ConfirmDialog`.",
        "Membuat middleware `role`, mendaftarkan aliasnya pada `bootstrap/app.php`, dan menampilkan menu sidebar "
        "sesuai role pengguna.",
        "Membangun modul UserManagement dengan CRUD Inertia khusus admin, lengkap dengan pencarian, filter role, "
        "pagination, dan aturan bahwa admin tidak dapat menurunkan role atau menghapus akunnya sendiri.",
        "Membangun modul Pendaftaran dengan CRUD AJAX memakai `fetch` dan `FormData`, termasuk upload berkas yang "
        "dapat dibuka kembali, diganti saat edit, dan ikut terhapus dari storage.",
        "Menampilkan error validasi 422 di bawah setiap input pada form AJAX, serta pesan berhasil setiap kali data "
        "ditambah, diubah, atau dihapus.",
        "Membuktikan pembatasan akses (error 403), perilaku AJAX pada tab Network, isi folder storage, dan hasil "
        "pengujian otomatis Pest.",
    ])

    # ------------------------------------------------------------------ B. Alat dan Bahan
    h1(doc, "B. Alat dan Bahan")
    p(doc, "Praktikum ini dikerjakan pada satu laptop dengan spesifikasi perangkat keras dan perangkat lunak "
           "sebagai berikut.")
    h2(doc, "1. Perangkat Keras")
    bullet(doc, "Laptop dengan prosesor 13th Gen Intel Core i7-13620H.")
    bullet(doc, "RAM 16 GB (terbaca 15,7 GB).")
    bullet(doc, "Ruang penyimpanan kosong lebih dari 3 GB untuk folder `node_modules` dan `vendor`.")
    bullet(doc, "Sistem operasi Windows 11 Home Single Language build 10.0.26200.")
    h2(doc, "2. Perangkat Lunak")
    table(doc,
          ["No", "Perangkat Lunak", "Versi / Keterangan"],
          [
              ["1", "XAMPP", "8.2.12, berisi Apache 2.4.58, MariaDB 10.4.32, PHP 8.2.12, dan phpMyAdmin 5.2.1"],
              ["2", "Composer", "2.10.3 sebagai dependency manager PHP"],
              ["3", "Laravel Framework", "12.71.0 dengan React Starter Kit"],
              ["4", "React dan Inertia.js", "React 19.0.0 dan @inertiajs/react 2.0.3"],
              ["5", "Inertia Laravel", "inertiajs/inertia-laravel 2.0.28"],
              ["6", "Tailwind CSS", "4.0.8 beserta shadcn/ui"],
              ["7", "Laravel Fortify", "autentikasi bawaan starter kit"],
              ["8", "nwidart/laravel-modules", "12.0.5 sebagai paket arsitektur HMVC"],
              ["9", "Node.js dan npm", "Node.js 24.13.1 dan npm 11.5.2, mengompilasi aset melalui Vite 6.1.1"],
              ["10", "TypeScript", "5.7.3"],
              ["11", "Pest", "3.8.7 sebagai framework pengujian otomatis"],
              ["12", "Visual Studio Code", "editor teks"],
              ["13", "Google Chrome", "browser dan alat pemeriksaan tab Network pada DevTools"],
              ["14", "Git", "version control"],
          ],
          widths=[1.2, 5.0, 9.7],
          font_size=10)
    p(doc, "Database yang dipakai adalah MariaDB dengan nama `hmvc_react`, sedangkan aplikasi dijalankan pada "
           "alamat `http://127.0.0.1:8010` karena port 8000 sedang dipakai proses lain.")

    # ------------------------------------------------------------------ C. Langkah-langkah
    h1(doc, "C. Langkah-Langkah Praktikum")
    p(doc, "Aplikasi saya bangun pada project `pertemuan9_hmvc_react` dengan database `hmvc_react`. Autentikasi "
           "memakai fitur bawaan React Starter Kit, sedangkan dua modul HMVC diisi sesuai tema penerimaan mahasiswa "
           "baru. Koneksi database dan locale diatur pada file `.env`, yaitu `DB_CONNECTION=mysql` dan "
           "`DB_DATABASE=hmvc_react` agar data disimpan di MariaDB pada XAMPP, bukan di SQLite bawaan.")

    # C.1
    h2(doc, "C.1 Menyiapkan Project dan Memasang HMVC")
    p(doc, "Project dibuat dengan Laravel Installer memakai starter kit React, autentikasi bawaan, dan Pest sebagai "
           "framework pengujian. Setelah project terbentuk, saya memasang paket HMVC lalu mengizinkan plugin merge "
           "Composer. Blok `merge-plugin` saya tambahkan pada bagian `extra` di `composer.json` agar Composer ikut "
           "membaca `composer.json` milik setiap modul, sehingga kelas di dalam folder `Modules` ter-autoload tanpa "
           "konfigurasi PSR-4 manual. Sesudah mengubah `composer.json`, saya menjalankan `composer dump-autoload` "
           "supaya peta kelas diperbarui.")
    code_block(doc, "01_composer", "Bagian require, merge-plugin, dan allow-plugins pada composer.json.")
    p(doc, "Dua modul saya buat sekaligus dengan perintah `php artisan module:make UserManagement Pendaftaran`. "
           "Karena tampilan modul ditulis dengan React, folder `resources/views`, `resources/assets`, "
           "`vite.config.js`, dan `package.json` bawaan modul saya biarkan tidak dipakai, lalu saya buat folder "
           "`resources/js/pages` di dalam tiap modul. Route API bawaan modul yang memakai middleware "
           "`auth:sanctum` saya kosongkan karena Sanctum tidak dipasang pada project ini. Status kedua modul dapat "
           "diperiksa pada dua berkas berikut.")
    code_block(doc, "02_modules_status", "modules_statuses.json dan route API modul yang dikosongkan.")
    p(doc, "Middleware `role` didaftarkan pada `bootstrap/app.php`. Laravel versi ini tidak lagi memakai "
           "`app/Http/Kernel.php`, sehingga alias middleware ditulis di dalam `withMiddleware`. Selain alias "
           "`role`, pada blok yang sama tetap dipertahankan middleware bawaan starter kit, yaitu "
           "`HandleInertiaRequests` dan `AddLinkHeadersForPreloadedAssets`.")
    code_block(doc, "03_bootstrap", "Alias middleware role pada bootstrap/app.php.")

    # C.2
    h2(doc, "C.2 Mengatur Halaman React di Dalam Modul")
    p(doc, "Agar Inertia dapat menemukan halaman milik modul, bagian `resolve` pada `createInertiaApp` saya ubah. "
           "Vite mengumpulkan seluruh halaman React dari `resources/js/pages` dan "
           "`Modules/*/resources/js/pages` melalui `import.meta.glob`. Jika nama halaman memuat tanda `::`, "
           "misalnya `Pendaftaran::index`, nama itu dipecah menjadi nama modul dan nama halaman, lalu berkas "
           "`Modules/Pendaftaran/resources/js/pages/index.tsx` dimuat oleh `resolvePageComponent`. Tanpa tanda "
           "tersebut, halaman dicari di `resources/js/pages` seperti biasa.")
    code_block(doc, "04_app_tsx", "Pengaturan resolve halaman modul pada app.tsx.")
    p(doc, "Folder modul juga saya daftarkan pada Tailwind CSS lewat baris `@source` di `app.css` agar class "
           "Tailwind yang ditulis di halaman modul ikut dikompilasi. Tanpa baris ini, halaman modul tampil tanpa "
           "style karena Tailwind 4 hanya memindai berkas yang disebutkan secara eksplisit. Pada `tsconfig.json` "
           "saya menambahkan pola `Modules/*/resources/js/**/*.ts` dan `*.tsx` ke bagian `include` supaya Visual "
           "Studio Code mengenali TypeScript di dalam modul.")
    code_block(doc, "05_tailwind_tsconfig", "Baris @source pada app.css dan pola include pada tsconfig.json.")

    # C.3
    h2(doc, "C.3 Menambahkan Role pada Tabel Users")
    p(doc, "Kolom role saya tambahkan lewat migration baru supaya tabel `users` bawaan Laravel tidak diubah "
           "langsung. Nilai bawaan kolom ini adalah `user`, sehingga akun yang tidak menyebut role otomatis menjadi "
           "user biasa. Nilai role saya bungkus dalam backed enum `UserRole` dengan dua case, yaitu `Admin` dan "
           "`User`, beserta method `label()` untuk menampilkan nama role yang mudah dibaca. Karena nilainya enum, "
           "salah ketik role tidak mungkin lolos ke database.")
    code_block(doc, "06_migration_role", "Migration penambah kolom role pada tabel users.")
    code_block(doc, "07_enum", "Enum UserRole dengan dua case dan method label().")
    p(doc, "Model `User` saya lengkapi dengan cast `role` ke enum, nilai bawaan `role` sebesar `user`, serta dua "
           "method bantu yaitu `isAdmin()` dan `hasRole()`. Method `isAdmin()` dipakai controller, form request, "
           "dan halaman React, sedangkan `hasRole()` dipakai middleware `role` karena menerima daftar role sebagai "
           "argumen variadik. Method `hasRole()` juga mengubah string dari route menjadi enum lewat "
           "`UserRole::tryFrom()`, sehingga role yang tidak dikenal akan dianggap tidak cocok.")
    code_block(doc, "08_user_model", "Model User dengan cast role dan method bantu isAdmin() serta hasRole().")
    p(doc, "Factory diberi state `admin()` supaya pembuatan akun admin di seeder dan pengujian cukup memanggil "
           "`User::factory()->admin()->create()`. State ini hanya mengisi kolom role, sehingga atribut lain tetap "
           "memakai nilai bawaan factory.")
    code_block(doc, "09a_user_factory", "UserFactory dengan state admin().")
    p(doc, "Seeder membuat satu akun admin `admin@example.com` dan satu akun user `user@example.com`, keduanya "
           "dengan password `password`. Keduanya dibuat lewat `firstOrCreate`, sehingga menjalankan seeder dua kali "
           "tidak menggandakan akun.")
    code_block(doc, "09b_seeder", "DatabaseSeeder yang membuat akun admin dan user.")
    p(doc, "Proses register memakai `RegisteredUserController` bawaan starter kit. Akun hasil register selalu diberi "
           "role user karena field `role` tidak pernah diisi dari input pengguna, sehingga pengguna tidak dapat "
           "mendaftarkan dirinya sebagai admin. Akun admin hanya dibuat lewat seeder atau oleh admin pada modul "
           "UserManagement.")
    code_block(doc, "10_register", "RegisteredUserController yang tidak pernah mengisi role dari input pengguna.")

    # C.4
    h2(doc, "C.4 Authentication dan Shared Props")
    p(doc, "React Starter Kit sudah menyediakan halaman login, register, logout, serta reset password, jadi bagian "
           "ini tidak saya tulis ulang. Pesan galat login bawaan Laravel sudah berbahasa Indonesia pada file "
           "`lang/id/auth.php`. Untuk menampilkan pesan berhasil dan pesan error dari redirect controller, saya "
           "menambahkan key `flash` pada method `share()` di `HandleInertiaRequests`.")
    code_block(doc, "11_handle_inertia", "Shared props auth dan flash pada HandleInertiaRequests.")
    p(doc, "Agar shared props mudah dibaca, saya membuat hook `useSharedProps` yang mengembalikan `user`, "
           "`isAdmin`, dan `flash`. Nilai `isAdmin` dipakai untuk menampilkan menu Kelola User, tetapi perlindungan "
           "yang sebenarnya tetap dilakukan oleh middleware role di sisi server. Saya juga membuat komponen "
           "`AlertMessage` dan `FlashMessage` untuk pesan, serta `ConfirmDialog` untuk dialog konfirmasi hapus "
           "yang dipakai bersama oleh kedua modul.")
    code_block(doc, "12_use_shared", "Hook useSharedProps.")
    code_block(doc, "13a_alert", "Komponen AlertMessage.")
    code_block(doc, "13b_flash", "Komponen FlashMessage.")
    code_block(doc, "14_confirm", "Komponen ConfirmDialog.")
    p(doc, "Menu sidebar saya susun pada `app-sidebar.tsx`. Menu Kelola User hanya ditambahkan jika `isAdmin` "
           "bernilai true, sedangkan menu Dashboard dan Pendaftaran selalu tampil. `NavMain` bawaan starter kit "
           "otomatis memberi tanda aktif pada menu yang sedang dibuka.")
    code_block(doc, "15_sidebar", "Menu sidebar berbasis role pada app-sidebar.tsx.")
    p(doc, "Halaman dashboard dirender oleh `DashboardController` yang bersifat invokable. Controller mengirim "
           "total pendaftar dari model `Daftar` milik modul Pendaftaran, sedangkan total user hanya dikirim untuk "
           "admin dan bernilai null bagi user biasa. Halaman `dashboard.tsx` menerima kedua props itu dan hanya "
           "menampilkan kartu Total Pengguna jika `isAdmin` bernilai true.")
    code_block(doc, "16_dashboard_ctrl", "DashboardController.")
    code_block(doc, "16b_dashboard_route", "Route dashboard dan route halaman utama pada routes/web.php.")
    code_block(doc, "17_dashboard_tsx", "Halaman dashboard.tsx.")

    # C.5
    h2(doc, "C.5 Authorization dengan Middleware Role")
    p(doc, "Middleware `EnsureUserHasRole` menerima daftar role sebagai parameter, misalnya `role:admin` atau "
           "`role:admin,user`. Jika pengguna belum login atau role-nya tidak termasuk daftar, permintaan dihentikan "
           "dengan `abort(403)` beserta pesan berbahasa Indonesia. Pemeriksaan memakai method `hasRole()` pada "
           "model `User` sehingga nilai role dibandingkan sebagai enum, bukan string bebas.")
    code_block(doc, "18_middleware", "Middleware EnsureUserHasRole.")

    # C.6
    h2(doc, "C.6 Modul UserManagement (CRUD Inertia)")
    p(doc, "Modul UserManagement memakai model `App\\Models\\User` milik aplikasi utama, sehingga modul ini tidak "
           "memiliki model sendiri. Aturan validasi saya taruh pada `StoreUserRequest` dan `UpdateUserRequest`. "
           "Pada `UpdateUserRequest`, email memakai `ignore` agar email milik user yang sedang diedit tidak "
           "dianggap duplikat, dan password bersifat nullable sehingga password lama tetap dipakai bila kolomnya "
           "dikosongkan. `Rule::when` membatasi pilihan role ketika admin mengubah akunnya sendiri.")
    code_block(doc, "19_store_request", "StoreUserRequest.")
    code_block(doc, "20_update_request", "UpdateUserRequest dengan aturan role untuk akun sendiri.")
    p(doc, "Controller mendukung pencarian nama atau email, filter role, dan pagination sepuluh baris per halaman. "
           "Setiap aksi mengembalikan halaman Inertia atau redirect beserta pesan flash. Method `destroy` menolak "
           "penghapusan akun sendiri dengan pesan error, sedangkan method `roleOptions()` menyiapkan pilihan role "
           "untuk select pada halaman React.")
    code_block(doc, "21_um_controller_1", "UserManagementController bagian 1 (index).")
    code_block(doc, "22_um_controller_2", "UserManagementController bagian 2 (create, store, edit, update).")
    code_block(doc, "23_um_controller_3", "UserManagementController bagian 3 (destroy dan roleOptions).")
    p(doc, "Route modul didaftarkan dengan `Route::resource` di dalam grup middleware `auth` dan `role:admin`, "
           "memakai prefix `admin` dan awalan nama `admin.`, sehingga URL-nya menjadi `/admin/users`. Method "
           "`show` tidak dipakai karena halaman detail user tidak diperlukan.")
    code_block(doc, "24_um_routes", "Route modul UserManagement.")
    p(doc, "Halaman `index.tsx` menampilkan tabel user, kotak pencarian, filter role, dan pagination. Tombol Hapus "
           "tidak ditampilkan pada baris akun yang sedang login, dan penghapusan memakai `ConfirmDialog` sehingga "
           "request DELETE baru dikirim setelah pengguna menekan Ya, hapus. Halaman `create` dan `edit` memakai "
           "satu komponen form bersama, yaitu `user-form.tsx`, dengan `useForm` milik Inertia.")
    code_block(doc, "25_um_index", "Halaman index.tsx modul UserManagement.")
    code_block(doc, "26_um_form", "Komponen user-form.tsx.")
    code_block(doc, "27_um_create", "Halaman create.tsx modul UserManagement.")
    code_block(doc, "27b_um_edit", "Halaman edit.tsx modul UserManagement.")

    # C.7
    h2(doc, "C.7 Modul Pendaftaran (CRUD AJAX)")
    p(doc, "Modul Pendaftaran menyimpan data calon mahasiswa beserta satu berkas pendukung. Migration pertama "
           "membuat tabel `daftars`, sedangkan migration kedua menambahkan kolom `berkas` dan `nama_berkas`. "
           "Pemisahan ini saya lakukan karena kolom berkas ditambahkan setelah tabel awal terbentuk, sehingga "
           "riwayat perubahan skema tetap terbaca. Kolom `no_hp` dibuat sepanjang 20 karakter agar angka 0 di depan "
           "tidak hilang.")
    code_block(doc, "28a_daftars_table", "Migration tabel daftars.")
    code_block(doc, "28b_berkas_column", "Migration penambah kolom berkas dan nama_berkas.")
    p(doc, "Factory dipakai untuk data uji. Model `Daftar` mengisi `$fillable` dan menambahkan accessor "
           "`berkas_url` yang diappend ke JSON. Accessor itu mengubah path penyimpanan menjadi URL lengkap lewat "
           "`asset('storage/...')`, sehingga React tidak perlu menyusun alamat berkas sendiri. Factory milik modul "
           "didaftarkan melalui `newFactory()` karena letaknya di luar folder `factories` bawaan Laravel.")
    code_block(doc, "29_daftar_model", "Model Daftar dengan accessor berkas_url.")
    code_block(doc, "29b_daftar_factory", "DaftarFactory untuk data uji.")
    p(doc, "`DaftarRequest` memakai aturan berkas yang berbeda untuk tambah dan ubah. Saat tambah, berkas wajib "
           "diunggah, sedangkan saat edit boleh dikosongkan karena berkas lama tetap dipakai. Format dibatasi jpg, "
           "jpeg, png, atau pdf dengan ukuran maksimal 2 MB, dan pesan galat untuk no HP serta berkas saya tulis "
           "dalam Bahasa Indonesia lewat method `messages()`.")
    code_block(doc, "30_daftar_request", "DaftarRequest dengan validasi berkas.")
    p(doc, "Controller hanya memakai satu method untuk memuat halaman, karena isi tabel diambil terpisah lewat "
           "`getData()`. Method `store`, `update`, dan `destroy` mengembalikan JSON berisi pesan berhasil. Berkas "
           "disimpan dengan `store()` ke `storage/app/public`, sedangkan database hanya menyimpan path dan nama "
           "asli berkas. Saat berkas diganti atau data dihapus, berkas lama ikut dihapus dari storage.")
    code_block(doc, "31_pendaftaran_ctrl", "PendaftaranController (index, getData, store, edit, update, destroy).")
    p(doc, "Route modul dilindungi middleware `auth` dan `role:admin,user`. Route `pendaftaran/data` saya tulis "
           "sebelum route `pendaftaran/{daftar}` agar kata `data` tidak dianggap sebagai id data.")
    code_block(doc, "32_pendaftaran_routes", "Route modul Pendaftaran.")
    p(doc, "Untuk mengirim request AJAX saya membuat helper `http.ts` di `resources/js/lib`. Helper ini membaca "
           "token CSRF dari cookie `XSRF-TOKEN` lalu mengirimnya sebagai header `X-XSRF-TOKEN`, dan menambahkan "
           "`Accept: application/json` agar Laravel mengembalikan error validasi sebagai JSON berkode 422. Jika "
           "respons bernilai gagal, helper melempar `HttpError` yang membawa status dan isi JSON.")
    code_block(doc, "33_http", "Helper http.ts untuk request AJAX.")
    p(doc, "Halaman `index.tsx` memuat data sekali lewat `GET /pendaftaran/data`, lalu seluruh operasi tambah, "
           "ubah, dan hapus berjalan tanpa memuat ulang halaman. Form tambah dan edit memakai satu Dialog yang "
           "sama; state `editing` bernilai null saat menambah dan berisi data pendaftar saat edit. Seluruh form "
           "dikirim sebagai `FormData` karena data berisi file, dan saat edit ditambahkan `_method` bernilai `PUT` "
           "karena PHP hanya membaca file pada request POST.")
    code_block(doc, "34_pend_index_1", "index.tsx modul Pendaftaran bagian 1 (tipe, url, dan FileLink).")
    code_block(doc, "35_pend_index_2", "index.tsx modul Pendaftaran bagian 2 (state, memuat data, pencarian).")
    code_block(doc, "36_pend_index_3", "index.tsx modul Pendaftaran bagian 3 (simpan dan hapus dengan AJAX).")
    code_block(doc, "37_pend_index_4", "index.tsx modul Pendaftaran bagian 4 (markup tabel).")
    code_block(doc, "38a_pend_index_5", "index.tsx modul Pendaftaran bagian 5 (dialog form).")
    code_block(doc, "38b_pend_index_6", "index.tsx modul Pendaftaran bagian 6 (dialog lanjutan dan konfirmasi hapus).")

    # C.8
    h2(doc, "C.8 Menjalankan dan Menguji Aplikasi")
    p(doc, "Aplikasi dijalankan dengan `php artisan serve` pada port 8010, sedangkan aset React dilayani dari hasil "
           "`npm run build`. Database diisi ulang dengan `php artisan migrate:fresh --seed` sehingga hanya berisi "
           "dua akun seeder. Halaman login, register, dan dashboard berasal dari starter kit, dan hanya halaman "
           "kedua modul yang ditulis di dalam folder `Modules`.")
    figure(doc, "00_serve", "Server aplikasi berjalan pada http://127.0.0.1:8010.", width_cm=12.0)

    h2(doc, "C.9 Pengujian Otomatis")
    p(doc, "Selain diuji melalui browser, fitur yang ada diuji secara otomatis memakai Pest. React Starter Kit "
           "sudah menyediakan pengujian authentication bawaan, sehingga saya cukup memastikan seluruhnya berjalan "
           "pada database kosong berkat `RefreshDatabase` yang diaktifkan pada `tests/Pest.php`. Pengujian "
           "mencakup render halaman login dan register, proses login dengan password salah, logout, reset "
           "password, pembaruan password, pembaruan profil, akses dashboard, serta pengujian unit contoh. Hasil "
           "terakhir adalah 27 test lulus dengan 64 assertion.")
    figure(doc, "25_pest", "Hasil pengujian otomatis dengan php artisan test.", width_cm=15.5)
    p(doc, "Pengujian modul sendiri belum saya tambahkan pada folder `tests`. Akibatnya, perilaku dua modul saya "
           "buktikan melalui browser dan pemeriksaan langsung pada tab Network, route list, serta isi database.")

    # ------------------------------------------------------------------ D. Hasil
    h1(doc, "D. Hasil dan Dokumentasi Program")
    p(doc, "Berikut tangkapan layar dari aplikasi yang sudah dijalankan pada alamat `http://127.0.0.1:8010`. "
           "Aplikasi berjalan dengan `php artisan serve` dan aset React hasil `npm run build`, sedangkan database "
           "diisi ulang dengan `php artisan migrate:fresh --seed`.")

    h2(doc, "D.1 Autentikasi")
    p(doc, "Saat `/pendaftaran` dibuka tanpa login, middleware `auth` mengarahkan pengguna ke halaman login. "
           "Alamat di bilah browser berubah menjadi `/login`, sehingga halaman modul tidak dapat dilihat tamu.")
    figure(doc, "01_login_redirect", "Halaman login saat /pendaftaran dibuka tanpa login.")
    p(doc, "Login dengan password salah tidak mengalihkan pengguna, tetapi menampilkan pesan Email atau password "
           "salah tepat di bawah kolom email.")
    figure(doc, "02_login_error", "Pesan galat saat password salah.")
    p(doc, "Halaman register menolak data yang tidak lengkap atau tidak valid. Pesan galat muncul di bawah setiap "
           "input yang salah, dan form tetap terbuka agar pengguna dapat memperbaikinya. Pada halaman ini nama "
           "dikosongkan, email memakai alamat yang sudah terdaftar, dan konfirmasi password sengaja dibedakan "
           "dari password. Ketiganya ditolak sekaligus dengan pesan masing-masing.")
    figure(doc, "03_register_error", "Galat validasi pada form register.")

    h2(doc, "D.2 Dashboard dan Hak Akses")
    p(doc, "Dashboard akun admin menampilkan dua kartu, yaitu Total Pendaftar dan Total Pengguna, serta menu Kelola "
           "User pada sidebar. Banner menyebut bahwa pengguna login sebagai Admin.")
    figure(doc, "04_dashboard_admin", "Dashboard akun admin dengan dua kartu dan menu Kelola User.")
    p(doc, "Setelah login sebagai user, dashboard hanya menampilkan satu kartu, yaitu Total Pendaftar. Menu Kelola "
           "User tidak muncul karena `isAdmin` bernilai false, dan kartu Total Pengguna tidak dirender karena "
           "props `totalUsers` bernilai null.")
    figure(doc, "22_dashboard_user", "Dashboard akun user dengan satu kartu.")
    p(doc, "User biasa yang membuka alamat `/admin/users` secara langsung tetap ditolak oleh middleware `role` "
           "dengan kode 403 beserta pesan bahwa pengguna tidak memiliki hak akses. Ini membuktikan bahwa "
           "penyembunyian menu di React hanya mengatur tampilan, sedangkan penjaga sebenarnya berada di server.")
    figure(doc, "23_forbidden", "Error 403 saat user membuka halaman khusus admin.")

    h2(doc, "D.3 CRUD User oleh Admin")
    p(doc, "Halaman Kelola User menampilkan daftar user beserta role-nya. Akun yang sedang login diberi badge "
           "Anda dan tidak memiliki tombol Hapus. Pencarian, filter role, dan pagination tetap tersedia di atas "
           "tabel.")
    figure(doc, "06_users_index", "Daftar user pada halaman Kelola User.")
    p(doc, "Form tambah user yang dikirim kosong menampilkan pesan galat di bawah setiap input, dan halaman tidak "
           "berpindah karena error validasi dikirim kembali sebagai props `errors` milik `useForm`.")
    figure(doc, "08_user_validation", "Galat validasi pada form tambah user.")
    p(doc, "Setelah data diisi dan disimpan, aplikasi kembali ke daftar user disertai pesan berhasil. User baru "
           "langsung muncul pada tabel dan jumlah user pada judul bertambah.")
    figure(doc, "09_user_create_filled", "Form tambah user yang sudah diisi.")
    figure(doc, "10_user_created", "Pesan berhasil setelah user ditambahkan.")
    p(doc, "Saat admin mengubah akunnya sendiri, password boleh dikosongkan agar tidak berubah. Pilihan role pada "
           "form ini menjadi tidak berbahaya karena `UpdateUserRequest` membatasi nilainya hanya `admin` ketika "
           "yang diedit adalah akun sendiri.")
    figure(doc, "11_user_edit_self", "Form edit akun admin sendiri.")
    p(doc, "Pencarian memfilter daftar berdasarkan nama atau email melalui query string, sehingga kata kunci "
           "tampil pada URL dan dapat dibagikan atau dimuat ulang tanpa kehilangan filter.")
    figure(doc, "12_user_search", "Pencarian user dengan kata kunci.")
    p(doc, "Penghapusan user memakai dialog konfirmasi bersama. Request DELETE baru dikirim setelah pengguna "
           "menekan Ya, hapus, sehingga tidak ada penghapusan yang tidak disengaja.")
    figure(doc, "13_user_delete_confirm", "Dialog konfirmasi sebelum user dihapus.")

    h2(doc, "D.4 CRUD Pendaftaran dengan AJAX")
    p(doc, "Halaman pendaftaran dimuat sekali, lalu isi tabel diambil dari endpoint JSON. Saat belum ada data, "
           "tabel menampilkan pesan Belum ada data pendaftar.")
    figure(doc, "05_pendaftaran_empty", "Halaman Pendaftaran saat belum ada data.")
    p(doc, "Tombol Tambah Pendaftar membuka dialog form. Bila form dikirim kosong, server mengembalikan 422 dan "
           "pesan galat tampil di bawah setiap input tanpa menutup dialog maupun memuat ulang halaman. Pesan untuk "
           "berkas memakai teks Bahasa Indonesia dari method `messages()` pada `DaftarRequest`.")
    figure(doc, "14_dialog_empty", "Dialog tambah pendaftar dalam keadaan kosong.")
    figure(doc, "15_dialog_422", "Respons 422 saat form dikirim kosong.")
    p(doc, "Setelah seluruh data dan berkas diisi lalu disimpan, dialog tertutup, tabel diperbarui tanpa memuat "
           "ulang halaman, dan pesan berhasil muncul di atas tabel.")
    figure(doc, "16_dialog_filled", "Dialog tambah pendaftar yang sudah diisi beserta berkas.")
    figure(doc, "17_after_save", "Pesan berhasil setelah data disimpan lewat AJAX.")
    p(doc, "Menambah data kedua tidak memuat ulang halaman. Jumlah data pada badge bertambah dan tabel langsung "
           "menampilkan dua baris, satu dengan berkas gambar dan satu dengan berkas pdf.")
    figure(doc, "18_two_records", "Daftar pendaftar setelah dua data ditambahkan.")
    p(doc, "Dialog edit mengambil data lama lewat AJAX dan menampilkan tautan Berkas saat ini. Berkas boleh "
           "dikosongkan jika tidak ingin menggantinya, sehingga berkas lama tetap dipakai.")
    figure(doc, "19_dialog_edit", "Dialog edit dengan data lama dan tautan berkas saat ini.")
    p(doc, "Penghapusan data memakai dialog konfirmasi. Setelah dikonfirmasi, baris hilang dari tabel tanpa "
           "berpindah halaman dan berkas milik data tersebut ikut terhapus dari storage.")
    figure(doc, "20_delete_confirm", "Dialog konfirmasi sebelum data dihapus.")

    h2(doc, "D.5 Bukti Respons JSON, Network, dan Berkas")
    p(doc, "Tab Network pada DevTools memperlihatkan bahwa seluruh operasi pendaftaran dikirim sebagai XHR, bukan "
           "sebagai navigasi halaman. Terlihat permintaan `GET /pendaftaran/data` untuk memuat tabel, `POST "
           "/pendaftaran` dengan status 422 ketika validasi gagal, `POST /pendaftaran` berstatus 200 ketika data "
           "tersimpan, serta `DELETE /pendaftaran/3` ketika data dihapus. Bunyi respons 422 juga tampil pada panel "
           "Response beserta daftar kolom yang gagal validasi.")
    figure(doc, "21_network", "Tab Network (Fetch/XHR) yang membuktikan CRUD Pendaftaran memakai AJAX.", width_cm=15.5)
    p(doc, "Endpoint `/pendaftaran/data` mengembalikan array JSON berisi seluruh pendaftar beserta `berkas_url`. "
           "Data inilah yang diambil oleh fungsi `loadData()` pada halaman React, lalu disimpan pada state "
           "`records`.")
    figure(doc, "24_json_data", "Respons JSON dari endpoint /pendaftaran/data.", width_cm=15.5)
    p(doc, "Daftar modul diperiksa dengan `php artisan module:list`. Kedua modul berstatus Enabled sehingga route-nya "
           "dimuat oleh Laravel.")
    figure(doc, "27_modulelist", "Hasil php artisan module:list.", width_cm=15.5)
    p(doc, "Seluruh route diperiksa dengan `php artisan route:list --except-vendor`. Terlihat enam route "
           "`admin/users` dari modul UserManagement dan enam route `pendaftaran` dari modul Pendaftaran, ditambah "
           "route dashboard.")
    figure(doc, "26_routelist", "Hasil php artisan route:list --except-vendor.", width_cm=15.5)
    p(doc, "Pemeriksaan terakhir dilakukan pada folder penyimpanan. Nama berkas di disk berupa hash acak hasil "
           "`store()`, sedangkan database hanya menyimpan path dan nama asli berkas.")
    figure(doc, "28_storage_folder", "Isi folder storage/app/public/berkas_pendaftaran.", width_cm=14.0)

    # ------------------------------------------------------------------ E. Analisis
    h1(doc, "E. Analisis dan Pembahasan")

    h2(doc, "E.1 Cara Kerja HMVC dengan Halaman React")
    p(doc, "HMVC membagi aplikasi menjadi modul, dan setiap modul memiliki controller, form request, model, "
           "migration, route, serta halaman React sendiri. Pada project ini modul Pendaftaran dan UserManagement "
           "berada di folder `Modules`, sedangkan autentikasi memakai Fortify di aplikasi utama. Namespace kelas "
           "mengikuti nama modul, misalnya "
           "`Modules\\Pendaftaran\\Http\\Controllers\\PendaftaranController`. Composer mengenali namespace tersebut "
           "karena `composer.json` setiap modul ikut dibaca melalui `merge-plugin`.")
    p(doc, "Halaman React milik modul tidak berada di `resources/js/pages`, melainkan di "
           "`Modules/*/resources/js/pages`. Karena itu Inertia perlu tahu cara menemukannya. Fungsi `resolve` pada "
           "`app.tsx` membaca format `NamaModul::halaman`, memecahnya, lalu memuat berkas yang sesuai lewat "
           "`resolvePageComponent`. Vite sendiri mengumpulkan seluruh halaman karena `import.meta.glob` mencakup "
           "folder modul, sedangkan Tailwind membutuhkan baris `@source` agar class di halaman modul ikut dibuat.")

    h2(doc, "E.2 Perbedaan Authentication dan Authorization")
    p(doc, "Authentication menjawab pertanyaan siapa penggunanya, sedangkan authorization menjawab apa yang boleh "
           "dilakukannya. Pada praktikum ini authentication sepenuhnya ditangani starter kit beserta halaman "
           "React-nya, jadi saya tidak menulis controller login dan register sendiri seperti pada Modul 8. "
           "Authorization ditangani middleware `EnsureUserHasRole` yang membaca kolom `role` melalui enum.")
    p(doc, "Pemisahan keduanya penting. Semua pengguna yang sudah login lolos middleware `auth`, tetapi hanya "
           "admin yang lolos middleware `role:admin`. Menu Kelola User pada sidebar hanya menyembunyikan tautan; "
           "perlindungan sebenarnya tetap di server, sehingga user yang mengetik `/admin/users` langsung menerima "
           "error 403.")

    h2(doc, "E.3 Middleware Role dan Pembatasan Akun Sendiri")
    p(doc, "Middleware menerima parameter role yang dipisahkan koma. Laravel mengirim bagian setelah titik dua "
           "sebagai argumen variadik, lalu middleware memanggil `hasRole()`. Nilai string dari route diubah menjadi "
           "enum melalui `UserRole::tryFrom()`, sehingga role yang salah ketik tidak pernah cocok dengan role mana "
           "pun.")
    p(doc, "Pemeriksaan tambahan saya taruh pada `UpdateUserRequest` dan method `destroy`. Admin yang mengubah "
           "akunnya sendiri hanya bisa memilih role admin, dan admin tidak bisa menghapus akunnya sendiri. Aturan "
           "ini mencegah admin kehilangan akses secara tidak sengaja. Di sisi tampilan, tombol Hapus memang tidak "
           "dirender untuk akun sendiri, tetapi aturan di server tetap diperlukan karena request dapat dikirim "
           "langsung tanpa melewati tombol tersebut.")

    h2(doc, "E.4 Perbedaan CRUD Inertia dan CRUD AJAX")
    table(doc,
          ["Aspek", "CRUD Inertia (UserManagement)", "CRUD AJAX (Pendaftaran)"],
          [
              ["Respons controller", "Inertia::render() atau redirect()->with()", "response()->json([...])"],
              ["Perilaku halaman", "Inertia mengganti komponen halaman tanpa full reload; data selalu dikirim ulang "
                                   "server sebagai props", "Halaman tidak berpindah; state React diperbarui dari "
                                                          "data JSON"],
              ["Pesan berhasil", "Session flash dibagikan sebagai shared props flash", "State message diisi dari "
                                                                                      "respons JSON"],
              ["Error validasi", "Redirect kembali; errors otomatis masuk ke useForm()", "Kode 422 + JSON errors "
                                                                                       "disimpan ke state errors"],
              ["Token CSRF", "Ditangani otomatis oleh Inertia", "Header X-XSRF-TOKEN dari cookie melalui helper "
                                                                "http.ts"],
              ["Form tambah/edit", "Halaman terpisah (create, edit) dengan komponen UserForm", "Satu Dialog "
                                                                                               "shadcn/ui yang dipakai "
                                                                                               "bergantian"],
              ["Upload berkas", "useForm() otomatis memakai FormData jika data berisi File", "FormData manual + "
                                                                                             "fetch() tanpa header "
                                                                                             "Content-Type"],
          ],
          widths=[3.4, 6.2, 6.3],
          font_size=10,
          caption="Tabel 1. Perbandingan CRUD Inertia dan CRUD AJAX pada kedua modul.")
    p(doc, "CRUD UserManagement bekerja secara Inertia. Form dikirim lewat `useForm`, server memproses lalu "
           "mengembalikan halaman Inertia atau redirect, dan Inertia mengganti komponen halaman tanpa memuat ulang "
           "seluruh browser. Data selalu dikirim ulang oleh server sebagai props, dan error validasi otomatis masuk "
           "ke objek `errors` milik `useForm`. Pesan berhasil dibagikan sebagai shared props flash.")
    p(doc, "CRUD Pendaftaran bekerja secara AJAX. Pengiriman form memakai `fetch` dan controller mengembalikan "
           "JSON. Tabel diperbarui dengan memanggil `loadData()` tanpa memuat ulang halaman, dan pesan ditampilkan "
           "dari respons JSON. Akibatnya, posisi scroll dan isi kotak pencarian tetap terjaga. Konsekuensinya, React "
           "harus menangani sendiri status 422 dan mengisi pesan galat ke setiap input, dan itu dilakukan dengan "
           "menyalin `error.data.errors` ke state `errors`.")

    h2(doc, "E.5 FormData, Penyimpanan Berkas, dan Token CSRF")
    p(doc, "Upload berkas tidak bisa memakai JSON biasa karena JSON tidak dapat membawa file. `FormData` dipakai "
           "karena objek itulah yang bisa membawa isi input `type=file`. Pada helper `http.ts`, header "
           "`Content-Type` sengaja tidak diisi agar browser otomatis memakai `multipart/form-data` beserta "
           "boundary. Untuk edit, request tetap dikirim sebagai POST dengan tambahan `_method` bernilai `PUT` "
           "karena PHP hanya membaca file pada request POST.")
    p(doc, "Token CSRF dikirim sebagai header `X-XSRF-TOKEN` yang dibaca dari cookie `XSRF-TOKEN`. Tanpa token ini, "
           "Laravel menolak permintaan dengan error 419. Karena request dikirim sebagai AJAX dengan header "
           "`Accept: application/json`, kegagalan validasi dikembalikan sebagai JSON berkode 422, bukan sebagai "
           "redirect, sehingga helper dapat membacanya.")
    p(doc, "Berkas disimpan di disk public dengan `store()`, sedangkan database hanya menyimpan path dan nama asli. "
           "Pemisahan ini membuat tabel tetap ringan, memungkinkan satu data memiliki berkas yang mudah diganti, "
           "dan menyimpan nama asli untuk ditampilkan sebagai tautan. Path hasil `store()` berupa hash acak, "
           "sehingga nama berkas pengguna tidak langsung terpakai dan tabrakan nama tidak terjadi. Saat berkas "
           "diganti atau data dihapus, berkas lama ikut dihapus dari storage agar tidak ada file sampah.")

    h2(doc, "E.6 Kendala dan Penyelesaian")
    p(doc, "Beberapa kendala saya temui selama pengerjaan, dan semuanya saya selesaikan tanpa mengubah perilaku "
           "aplikasi yang dijanjikan modul.")
    numbered(doc, [
        "Kelas modul sempat tidak ditemukan karena autoload belum diperbarui setelah modul dibuat. Perbaikannya "
        "adalah menjalankan `composer dump-autoload`.",
        "Halaman modul sempat gagal dimuat karena template `app.blade.php` masih memuat berkas halaman secara "
        "langsung, padahal halaman modul berada di luar `resources/js/pages`. Perbaikannya cukup memuat `app.tsx` "
        "pada direktif `@vite`, karena seluruh halaman sudah di-resolve oleh Inertia melalui `import.meta.glob`.",
        "Kelas middleware bawaan sempat tidak ditemukan karena berkasnya hilang dari folder "
        "`app/Http/Middleware` padahal masih dirujuk `bootstrap/app.php`. Saya membuat ulang kelas tersebut agar "
        "request web dapat diproses.",
        "Halaman login dan register sempat gagal dirender. Penyebabnya adalah konfigurasi Fortify belum lengkap; "
        "setelah view Inertia terdaftar dan batas percobaan login diatur, kedua halaman tampil normal.",
        "Koneksi database ditolak dengan pesan `SQLSTATE[HY000] [2002]`. Penyebabnya layanan MariaDB pada XAMPP "
        "belum berjalan. Setelah layanan dinyalakan, aplikasi kembali normal.",
        "Perintah `npm` sempat diblokir kebijakan eksekusi PowerShell. Saya menjalankannya melalui cmd agar skrip "
        "npm dapat dieksekusi.",
        "Halaman modul sempat tampil tanpa style karena Tailwind 4 tidak memindai folder modul. Penyelesaiannya "
        "adalah menambahkan baris `@source '../../Modules/*/resources/js/**/*.{ts,tsx}'` pada `app.css`.",
    ])

    h2(doc, "E.7 Catatan Perbedaan dengan Modul")
    p(doc, "Ada beberapa perbedaan antara hasil praktikum ini dan contoh pada modul. Saya mencatatnya agar tidak "
           "menimbulkan salah paham saat laporan diperiksa.")
    numbered(doc, [
        "Nama project adalah `pertemuan9_hmvc_react` dengan database `hmvc_react`, sesuai nama pada modul.",
        "Seluruh tampilan memakai React Starter Kit dengan Inertia, bukan Blade dan jQuery seperti Modul 8.",
        "Kolom data pendaftar mencakup `nama`, `asal_sekolah`, `prodi_tujuan`, `email`, `no_hp`, `berkas`, dan "
        "`nama_berkas`, dengan email sebagai kolom unik.",
        "Sebagian pesan galat validasi bawaan Laravel pada form AJAX masih berbahasa Inggris, sedangkan pesan untuk "
        "no HP dan berkas sudah berbahasa Indonesia lewat method `messages()`.",
        "Aplikasi diuji pada alamat `http://127.0.0.1:8010`, bukan `http://127.0.0.1:8000`, karena port 8000 "
        "sedang dipakai proses lain.",
        "Pengujian Pest masih berisi pengujian bawaan starter kit; pengujian khusus kedua modul belum ditambahkan.",
    ])

    # ------------------------------------------------------------------ F. Kesimpulan
    h1(doc, "F. Kesimpulan")
    numbered(doc, [
        "Arsitektur HMVC berhasil diterapkan dengan dua modul, yaitu Pendaftaran dan UserManagement, yang "
        "masing-masing memiliki controller, form request, model, migration, route, dan halaman React sendiri di "
        "dalam folder `Modules`.",
        "Halaman React di dalam modul dapat dimuat melalui Inertia setelah fungsi `resolve` pada `app.tsx` diatur "
        "dengan format `NamaModul::halaman`, dan Tailwind CSS ikut membuat class yang dipakai modul setelah baris "
        "`@source` ditambahkan.",
        "Autentikasi memakai fitur bawaan starter kit, sedangkan pembagian hak akses dilakukan dengan kolom "
        "`role`, enum `UserRole`, middleware `role`, dan shared props yang membedakan admin dan user.",
        "Middleware role dan aturan tambahan pada form request berhasil membatasi halaman khusus admin, termasuk "
        "mencegah admin menurunkan role atau menghapus akunnya sendiri.",
        "CRUD UserManagement berjalan secara Inertia dengan form `useForm`, pesan berhasil dari shared props "
        "`flash`, dan error validasi yang otomatis tampil di bawah setiap input.",
        "CRUD Pendaftaran berjalan dengan `fetch` dan `FormData`, menampilkan error 422 di bawah input, "
        "memperbarui tabel tanpa memuat ulang halaman, serta mengelola upload berkas beserta penggantian dan "
        "penghapusannya.",
        "Pengujian otomatis Pest yang tersedia lulus seluruhnya, yaitu 27 test dengan 64 assertion, sehingga "
        "fitur authentication dan dashboard bawaan terbukti berjalan.",
    ])
    p(doc, "Dari praktikum ini saya memahami bahwa HMVC dengan React memisahkan tanggung jawab antar modul tanpa "
           "kehilangan pola Laravel, bahwa authentication dan authorization adalah dua hal berbeda, dan bahwa CRUD "
           "Inertia maupun AJAX sama-sama menuntut penanganan error validasi serta pesan yang teliti di sisi klien. "
           "Saya juga memahami bahwa keamanan halaman tidak boleh bergantung pada tampilan, karena penyembunyian "
           "menu hanya kosmetik sedangkan middleware di server adalah penjaga yang sebenarnya.")

    # ------------------------------------------------------------------ G. Repository
    h1(doc, "G. Link Repository GitHub")
    par = doc.add_paragraph()
    r = par.add_run("https://github.com/Dryhus21/PABW.git")
    r.font.name = MONO
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor(0x11, 0x33, 0xAA)
    p(doc, "Repository memuat seluruh kode program, termasuk folder `Modules` beserta halaman React di dalamnya, "
           "middleware, controller, form request, route, seeder, serta komponen di `resources/js`. Folder "
           "`node_modules` dan `vendor` tidak diunggah.")

    # footer page numbers on every section
    for sec in doc.sections:
        add_page_number(sec.footer.paragraphs[0])

    doc.save(OUT)
    print("saved:", OUT)
    print("kode:", code_counter[0], "gambar:", fig_counter[0])


if __name__ == "__main__":
    build()
