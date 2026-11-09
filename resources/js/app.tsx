import '../css/app.css';

import { createInertiaApp } from '@inertiajs/react';
import { resolvePageComponent } from 'laravel-vite-plugin/inertia-helpers';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { initializeTheme } from './hooks/use-appearance';

const appName = import.meta.env.VITE_APP_NAME || 'Laravel';

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

    setup({ el, App, props }) {
        const root = createRoot(el);

        root.render(
            <StrictMode>
                <App {...props} />
            </StrictMode>
        );
    },

    progress: {
        color: '#485563',
    },
});

// This will set light / dark mode on load...
initializeTheme();
