import { Link } from '@inertiajs/react';
import type { FormEvent } from 'react';
import InputError from '@/components/input-error';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

export type UserFormData = {
    name: string;
    email: string;
    role: string;
    password: string;
    password_confirmation: string;
};

type UserFormProps = {
    data: UserFormData;
    errors: Partial<Record<keyof UserFormData, string>>;
    processing: boolean;
    roles: { value: string; label: string }[];
    isEdit?: boolean;
    submitLabel: string;
    setData: (key: keyof UserFormData, value: string) => void;
    onSubmit: (event: FormEvent) => void;
};

export function UserForm({
    data,
    errors,
    processing,
    roles,
    isEdit = false,
    submitLabel,
    setData,
    onSubmit,
}: UserFormProps) {
    return (
        <form onSubmit={onSubmit} noValidate className="max-w-xl space-y-5 rounded-xl border p-6">
            <div className="grid gap-2">
                <Label htmlFor="name">
                    Nama <span className="text-red-500">*</span>
                </Label>
                <Input
                    id="name"
                    value={data.name}
                    onChange={(event) => setData('name', event.target.value)}
                    autoFocus
                />
                <InputError message={errors.name} />
            </div>

            <div className="grid gap-2">
                <Label htmlFor="email">
                    Email <span className="text-red-500">*</span>
                </Label>
                <Input
                    id="email"
                    type="email"
                    value={data.email}
                    onChange={(event) => setData('email', event.target.value)}
                />
                <InputError message={errors.email} />
            </div>

            <div className="grid gap-2">
                <Label htmlFor="role">
                    Role <span className="text-red-500">*</span>
                </Label>
                <select
                    id="role"
                    value={data.role}
                    onChange={(event) => setData('role', event.target.value)}
                    className="h-9 rounded-md border border-input bg-transparent px-3 text-sm shadow-xs"
                >
                    {roles.map((role) => (
                        <option key={role.value} value={role.value}>
                            {role.label}
                        </option>
                    ))}
                </select>
                <InputError message={errors.role} />
            </div>

            <div className="grid gap-2">
                <Label htmlFor="password">
                    Password {!isEdit && <span className="text-red-500">*</span>}
                </Label>
                <Input
                    id="password"
                    type="password"
                    value={data.password}
                    onChange={(event) => setData('password', event.target.value)}
                />
                {isEdit && (
                    <p className="text-xs text-muted-foreground">
                        Kosongkan jika tidak ingin mengganti password.
                    </p>
                )}
                <InputError message={errors.password} />
            </div>

            <div className="grid gap-2">
                <Label htmlFor="password_confirmation">Konfirmasi Password</Label>
                <Input
                    id="password_confirmation"
                    type="password"
                    value={data.password_confirmation}
                    onChange={(event) => setData('password_confirmation', event.target.value)}
                />
            </div>

            <div className="flex gap-2">
                <Button type="submit" disabled={processing}>
                    {processing ? 'Menyimpan...' : submitLabel}
                </Button>
                <Button asChild variant="secondary">
                    <Link href="/admin/users">Batal</Link>
                </Button>
            </div>
        </form>
    );
}
