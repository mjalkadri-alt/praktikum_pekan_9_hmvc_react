/**
 * Ziggy menempelkan helper global `route()` lewat `@routes` di resources/views/app.blade.php.
 * Halaman (welcome, auth, settings) memanggilnya tanpa import, jadi tipenya
 * dideklarasikan di sini agar `tsc` tidak melaporkan "Cannot find name 'route'".
 */
import type { Config, route as ziggyRoute } from 'ziggy-js';

declare global {
    const route: typeof ziggyRoute;

    // eslint-disable-next-line no-var
    var Ziggy: Config & { location: string };
}

export {};
