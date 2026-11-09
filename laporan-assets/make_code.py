"""Cut the real source files into the exact excerpts used by the report."""
import os
import re

import codeshot

ROOT = r"C:\xampp\htdocs\PABW\pertemuan9_hmvc_react"


def read(rel):
    return open(os.path.join(ROOT, rel.replace("/", "\\")), encoding="utf-8").read()


def indent_block(src, needle, extra=0):
    """Return the block starting at `needle` up to the closing brace at the same indent."""
    lines = src.split("\n")
    start = next(i for i, l in enumerate(lines) if needle in l)
    base = len(lines[start]) - len(lines[start].lstrip())
    out = [lines[start]]
    for l in lines[start + 1:]:
        if l.strip() and (len(l) - len(l.lstrip())) <= base and l.strip()[0] in "}]":
            out.append(l)
            break
        out.append(l)
    block = "\n".join(out)
    if extra:
        block = "\n".join(("" if not b.strip() else b) for b in block.split("\n"))
    return block


SNIPPETS = {}

# 01 composer.json
SNIPPETS["01_composer"] = ("""{
  "require": {
    "php": "^8.2",
    "inertiajs/inertia-laravel": "^2.0",
    "laravel/framework": "^12.0",
    "laravel/tinker": "^2.10.1",
    "nwidart/laravel-modules": "^12.0",
    "tightenco/ziggy": "^2.4"
  },
  "extra": {
    "laravel": { "dont-discover": [] },
    "merge-plugin": {
      "include": ["Modules/*/composer.json"]
    }
  },
  "config": {
    "optimize-autoloader": true,
    "preferred-install": "dist",
    "sort-packages": true,
    "allow-plugins": {
      "pestphp/pest-plugin": true,
      "php-http/discovery": true,
      "wikimedia/composer-merge-plugin": true
    }
  }
}""", "json")

# 02 modules_statuses.json + api.php
SNIPPETS["02_modules_status"] = ("""// modules_statuses.json
{
    "UserManagement": true,
    "Pendaftaran": true
}

// Modules/Pendaftaran/routes/api.php
<?php
// modul ini tidak menyediakan endpoint API
""", "json")

# 03 bootstrap/app.php
src = read("bootstrap/app.php")
b = src[src.index("return Application::configure"):]
SNIPPETS["03_bootstrap"] = ("""<?php

use App\\Http\\Middleware\\HandleInertiaRequests;
use App\\Http\\Middleware\\EnsureUserHasRole;
use Illuminate\\Foundation\\Application;
use Illuminate\\Http\\Middleware\\AddLinkHeadersForPreloadedAssets;

""" + b.strip(), "php")

# 04 app.tsx resolve
src = read("resources/js/app.tsx")
SNIPPETS["04_app_tsx"] = ("""import '../css/app.css';
import { createInertiaApp } from '@inertiajs/react';
import { resolvePageComponent } from 'laravel-vite-plugin/inertia-helpers';

createInertiaApp({
    title: (title) => (title ? `${title} - ${appName}` : appName),

    resolve: (name) => {
        const pages = import.meta.glob([
            './pages/**/*.tsx',
            '../../Modules/*/resources/js/pages/**/*.tsx',
        ]);

        // Halaman modul ditulis dengan format NamaModul::nama-halaman
        if (name.includes('::')) {
            const [module, page] = name.split('::');
            return resolvePageComponent(
                `../../Modules/${module}/resources/js/pages/${page}.tsx`,
                pages
            );
        }

        return resolvePageComponent(`./pages/${name}.tsx`, pages);
    },
    /* ... setup() dan progress() ... */
});""", "ts")

# 05 app.css @source + tsconfig include
SNIPPETS["05_tailwind_tsconfig"] = ("""/* resources/css/app.css */
@import 'tailwindcss';
@plugin 'tailwindcss-animate';

@source '../../vendor/laravel/framework/src/Illuminate/Pagination/resources/views/*.blade.php';
@source '../../Modules/*/resources/js/**/*.{ts,tsx}';

/* tsconfig.json */
{
  "include": [
    "resources/js/**/*.ts",
    "resources/js/**/*.d.tsx",
    "resources/js/**/*.tsx",
    "Modules/*/resources/js/**/*.ts",
    "Modules/*/resources/js/**/*.d.tsx"
  ]
}""", "ts")

# 06 migration
SNIPPETS["06_migration_role"] = ("""<?php

use Illuminate\\Database\\Migrations\\Migration;
use Illuminate\\Database\\Schema\\Blueprint;
use Illuminate\\Support\\Facades\\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table('users', function (Blueprint $table) {
            $table->string('role')->default('user')->after('email');
        });
    }

    public function down(): void
    {
        Schema::table('users', function (Blueprint $table) {
            $table->dropColumn('role');
        });
    }
};""", "php")

# 07 enum
SNIPPETS["07_enum"] = (read("app/Enums/UserRole.php").strip(), "php")

# 08 user model
src = read("app/Models/User.php")
head = src[: src.index("    /**\n     * Determine whether the user has the admin role.")]
head = head.replace("// use Illuminate\\Contracts\\Auth\\MustVerifyEmail;\n", "")
SNIPPETS["08_user_model"] = (head.rstrip() + """

    public function isAdmin(): bool
    {
        return $this->role === UserRole::Admin;
    }

    public function hasRole(UserRole|string ...$roles): bool
    {
        foreach ($roles as $role) {
            $targetRole = $role instanceof UserRole ? $role : UserRole::tryFrom($role);

            if ($this->role === $targetRole) {
                return true;
            }
        }

        return false;
    }
}""", "php")

# 09 factory + seeder
src_f = read("database/factories/UserFactory.php")
src_s = read("database/seeders/DatabaseSeeder.php")
f_def = src_f[src_f.index("    public function definition"):]
s_run = src_s[src_s.index("    public function run"):]
SNIPPETS["09a_user_factory"] = (f_def.rstrip(), "php")
SNIPPETS["09b_seeder"] = (s_run.rstrip(), "php")

# 10 registered user controller store
src = read("app/Http/Controllers/Auth/RegisteredUserController.php")
SNIPPETS["10_register"] = (src[src.index("    public function store"):].rstrip(), "php")

# 11 handle inertia requests share
src = read("app/Http/Middleware/HandleInertiaRequests.php")
SNIPPETS["11_handle_inertia"] = ("""<?php

namespace App\\Http\\Middleware;

use Illuminate\\Http\\Request;
use Inertia\\Middleware;

class HandleInertiaRequests extends Middleware
{
    protected $rootView = 'app';

""" + src[src.index("    public function share"):].rstrip(), "php")

# 12 hook
SNIPPETS["12_use_shared"] = (read("resources/js/hooks/use-shared-props.ts").strip(), "ts")

# 13 alert
_alert = read("resources/js/components/alert-message.tsx")
SNIPPETS["13a_alert"] = (_alert[:_alert.index("export function FlashMessage")].rstrip(), "ts")
SNIPPETS["13b_flash"] = (_alert[_alert.index("export function FlashMessage"):].rstrip(), "ts")

# 14 confirm
SNIPPETS["14_confirm"] = (read("resources/js/components/confirm-dialog.tsx").strip(), "ts")

# 15 sidebar
src = read("resources/js/components/app-sidebar.tsx")
SNIPPETS["15_sidebar"] = (src[src.index("export function AppSidebar"):].rstrip(), "ts")

# 16 dashboard controller + route
SNIPPETS["16_dashboard_ctrl"] = (read("app/Http/Controllers/DashboardController.php").strip(), "php")
SNIPPETS["16b_dashboard_route"] = ("""<?php

use App\\Http\\Controllers\\DashboardController;
use Illuminate\\Support\\Facades\\Route;
use Inertia\\Inertia;

Route::get('/', function () {
    return Inertia::render('welcome', [
        'canRegister' => Route::has('register'),
    ]);
})->name('home');

Route::middleware(['auth', 'verified'])->group(function () {
    Route::get('dashboard', DashboardController::class)->name('dashboard');
});

require __DIR__.'/auth.php';
require __DIR__.'/settings.php';""", "php")

# 17 dashboard.tsx
src = read("resources/js/pages/dashboard.tsx")
SNIPPETS["17_dashboard_tsx"] = (src[src.index("export default function Dashboard"):].rstrip(), "ts")

# 18 middleware
SNIPPETS["18_middleware"] = (read("app/Http/Middleware/EnsureUserHasRole.php").strip(), "php")

# 19 store request
src = read("Modules/UserManagement/app/Http/Requests/StoreUserRequest.php")
SNIPPETS["19_store_request"] = ("""<?php
namespace Modules\\UserManagement\\Http\\Requests;

use App\\Enums\\UserRole;
use Illuminate\\Foundation\\Http\\FormRequest;
use Illuminate\\Validation\\Rule;
use Illuminate\\Validation\\Rules\\Password;

""" + src[src.index("class StoreUserRequest"):].rstrip(), "php")

# 20 update request
SNIPPETS["20_update_request"] = (read("Modules/UserManagement/app/Http/Requests/UpdateUserRequest.php").strip(), "php")

# 21-23 controller parts
src = read("Modules/UserManagement/app/Http/Controllers/UserManagementController.php")
head = src[: src.index("    /**\n     * Show the form for creating a new user.")]
idx_store = src.index("    /**\n     * Store a newly created user.")
idx_destroy = src.index("    /**\n     * Remove the specified user.")
SNIPPETS["21_um_controller_1"] = ("""<?php

namespace Modules\\UserManagement\\Http\\Controllers;

use App\\Enums\\UserRole;
use App\\Http\\Controllers\\Controller;
use App\\Models\\User;
use Illuminate\\Database\\Eloquent\\Builder;
use Illuminate\\Http\\Request;
use Inertia\\Inertia;
use Inertia\\Response;

class UserManagementController extends Controller
{
""" + head[head.index("    /**\n     * Display a listing"):].rstrip(), "php")
SNIPPETS["22_um_controller_2"] = (src[idx_store:idx_destroy].rstrip(), "php")
SNIPPETS["23_um_controller_3"] = (src[idx_destroy:].rstrip(), "php")

# 24 routes
SNIPPETS["24_um_routes"] = (read("Modules/UserManagement/routes/web.php").strip(), "php")

# 25 um index.tsx (chunk to keep image height sane)
src = read("Modules/UserManagement/resources/js/pages/index.tsx")
SNIPPETS["25_um_index"] = (src[: src.index("// Label pagination Laravel")].rstrip() + "\n}", "ts")

# 26 user form
SNIPPETS["26_um_form"] = (read("Modules/UserManagement/resources/js/components/user-form.tsx").strip(), "ts")

# 27 create + edit (separate blocks)
SNIPPETS["27_um_create"] = (read("Modules/UserManagement/resources/js/pages/create.tsx").strip(), "ts")
SNIPPETS["27b_um_edit"] = (read("Modules/UserManagement/resources/js/pages/edit.tsx").strip(), "ts")

# 28 migrations
SNIPPETS["28a_daftars_table"] = (read("Modules/Pendaftaran/database/migrations/2026_11_09_034359_create_daftars_table.php").strip(), "php")
SNIPPETS["28b_berkas_column"] = (read("Modules/Pendaftaran/database/migrations/2026_11_09_034652_add_berkas_to_daftars_table.php").strip(), "php")

# 29 model + factory
SNIPPETS["29_daftar_model"] = (read("Modules/Pendaftaran/app/Models/Daftar.php").strip(), "php")
SNIPPETS["29b_daftar_factory"] = (read("Modules/Pendaftaran/database/factories/DaftarFactory.php").strip(), "php")

# 30 request
SNIPPETS["30_daftar_request"] = (read("Modules/Pendaftaran/app/Http/Requests/DaftarRequest.php").strip(), "php")

# 31 controller
SNIPPETS["31_pendaftaran_ctrl"] = (read("Modules/Pendaftaran/app/Http/Controllers/PendaftaranController.php").strip(), "php")

# 32 routes
SNIPPETS["32_pendaftaran_routes"] = (read("Modules/Pendaftaran/routes/web.php").strip(), "php")

# 33 http.ts
SNIPPETS["33_http"] = (read("resources/js/lib/http.ts").strip(), "ts")

# 34-38 pendaftaran index chunks
src = read("Modules/Pendaftaran/resources/js/pages/index.tsx").rstrip()
cuts = [
    src.index("export default function Index"),
    src.index("    // Pencarian dilakukan di browser"),
    src.index("    const resetFileAndErrors"),
    src.index("    // Menyimpan data (tambah dan edit)"),
    src.index("    const handleChange"),
    src.index("    return (\n        <AppLayout"),
    src.index("                <div className=\"overflow-x-auto rounded-xl border\">"),
    src.index("            <Dialog"),
    src.index("            <ConfirmDialog"),
]
header = src[: cuts[0]]
SNIPPETS["34_pend_index_1"] = ("""import { Head } from '@inertiajs/react';
import { FileImage, FileText, LoaderCircle, Pencil, Plus, Search, Trash2 } from 'lucide-react';
import { useEffect, useMemo, useState } from 'react';
import type { ChangeEvent, FormEvent } from 'react';
import { AlertMessage } from '@/components/alert-message';
import { ConfirmDialog } from '@/components/confirm-dialog';
import InputError from '@/components/input-error';
import { Dialog, DialogContent, DialogDescription, DialogFooter,
         DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { http, HttpError } from '@/lib/http';
import type { ValidationErrors } from '@/lib/http';

""" + header[header.index("type Daftar = {"):].rstrip(), "ts")

SNIPPETS["35_pend_index_2"] = (src[cuts[0]:cuts[2]].rstrip(), "ts")
SNIPPETS["36_pend_index_3"] = (src[cuts[3]:cuts[5]].rstrip(), "ts")
SNIPPETS["37_pend_index_4"] = (src[cuts[5]:cuts[6]].rstrip() + "\n/* ... markup tombol Edit/Hapus ... */\n"
                               "        </AppLayout>\n    );\n}", "ts")
SNIPPETS["38a_pend_index_5"] = (src[cuts[7]:cuts[8]].rstrip() + "\n            </Dialog>", "ts")
SNIPPETS["38b_pend_index_6"] = ("            " + src[cuts[8]:].rstrip() + "\n}", "ts")


if __name__ == "__main__":
    for name, (code, lang) in SNIPPETS.items():
        path, w, h = codeshot.render(name, code, lang)
        print(name, w, h, os.path.basename(path))
