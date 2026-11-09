export type ValidationErrors = Record<string, string[]>;
type ErrorBody = { message?: string; errors?: ValidationErrors } | null;
export class HttpError extends Error {
    status: number;
    data: ErrorBody;
    constructor(status: number, data: ErrorBody) {
        super(data?.message ?? `Request gagal dengan status ${status}`);
        this.status = status;
        this.data = data;
    }
}
// Membaca token CSRF dari cookie XSRF-TOKEN yang dibuat oleh Laravel
function getXsrfToken(): string {
    const cookie = document.cookie.split('; ').find((row) => row.startsWith('XSRF-TOKEN='));

    return cookie ? decodeURIComponent(cookie.substring('XSRF-TOKEN='.length)) : '';
}
type RequestOptions = {
    method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
    body?: FormData;
};
export async function http<T>(url: string, { method = 'GET', body }: RequestOptions =    {}): Promise<T> {
    const response = await fetch(url, {
        method,
        body,
        credentials: 'same-origin',
        headers: {
            Accept: 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-XSRF-TOKEN': getXsrfToken(),
        },
    });
    const data = await response.json().catch(() => null);
    if (!response.ok) {
        throw new HttpError(response.status, data);
    }
    return data as T;
}