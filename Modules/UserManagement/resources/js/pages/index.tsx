import { Head, Link, router } from '@inertiajs/react';
import { Pencil, Plus, Search, Trash2 } from 'lucide-react';
import { useState } from 'react';
import type { FormEvent } from 'react';
import { FlashMessage } from '@/components/alert-message';
import { ConfirmDialog } from '@/components/confirm-dialog';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useSharedProps } from '@/hooks/use-shared-props';
import AppLayout from '@/layouts/app-layout';
import type { BreadcrumbItem } from '@/types';

type UserRow = {
  id: number;
  name: string;
  email: string;
  role: 'admin' | 'user';
  role_label: string;
  created_at: string | null;
};

type PaginationLink = {
  url: string | null;
  label: string;
  active: boolean;
};

type IndexProps = {
  users: {
    data: UserRow[];
    links: PaginationLink[];
    from: number | null;
    to: number | null;
    total: number;
  };
  filters: {
    search: string;
    role: string;
  };
  roles: {
    value: string;
    label: string;
  }[];
};

const breadcrumbs: BreadcrumbItem[] = [{ title: 'Kelola User', href: '/admin/users' }];

export default function Index({ users, filters, roles }: IndexProps) {
  const { user: currentUser } = useSharedProps();
  const [search, setSearch] = useState(filters.search);
  const [deleting, setDeleting] = useState<UserRow | null>(null);
  const [processing, setProcessing] = useState(false);

  // Kirim ulang request GET /admin/users dengan kata kunci dan filter role
  const applyFilters = (params: { search?: string; role?: string }) => {
    router.get(
      '/admin/users',
      { ...filters, search, ...params },
      { preserveState: true, replace: true },
    );
  };

  const handleSearch = (event: FormEvent) => {
    event.preventDefault();
    applyFilters({ search });
  };

  const handleDelete = () => {
    if (!deleting) {
      return;
    }

    router.delete(`/admin/users/${deleting.id}`, {
      preserveScroll: true,
      onStart: () => setProcessing(true),
      onFinish: () => {
        setProcessing(false);
        setDeleting(null);
      },
    });
  };

  return (
    <AppLayout breadcrumbs={breadcrumbs}>
      <Head title="Kelola User" />
      <div className="flex flex-1 flex-col gap-4 p-4">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div>
            <h1 className="text-xl font-semibold">Kelola User</h1>
            <p className="text-sm text-muted-foreground">Total {users.total} user terdaftar.</p>
          </div>
          <Button asChild>
            <Link href="/admin/users/create">
              <Plus /> Tambah User
            </Link>
          </Button>
        </div>

        <FlashMessage />

        <div className="flex flex-wrap gap-2">
          <form onSubmit={handleSearch} className="flex flex-1 gap-2">
            <Input
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Cari nama atau email..."
              className="max-w-sm"
            />
            <Button type="submit" variant="secondary">
              <Search /> Cari
            </Button>
          </form>

          <select
            value={filters.role}
            onChange={(event) => applyFilters({ role: event.target.value })}
            className="h-9 rounded-md border border-input bg-transparent px-3 text-sm shadow-xs"
          >
            <option value="">Semua role</option>
            {roles.map((role) => (
              <option key={role.value} value={role.value}>
                {role.label}
              </option>
            ))}
          </select>
        </div>

        <div className="overflow-x-auto rounded-xl border">
          <table className="w-full text-sm">
            <thead className="bg-muted/50 text-left">
              <tr>
                <th className="px-4 py-3 font-medium">No</th>
                <th className="px-4 py-3 font-medium">Nama</th>
                <th className="px-4 py-3 font-medium">Email</th>
                <th className="px-4 py-3 font-medium">Role</th>
                <th className="px-4 py-3 font-medium">Dibuat</th>
                <th className="px-4 py-3 text-right font-medium">Aksi</th>
              </tr>
            </thead>
            <tbody>
              {users.data.length === 0 && (
                <tr>
                  <td colSpan={6} className="px-4 py-8 text-center text-muted-foreground">
                    Data user tidak ditemukan.
                  </td>
                </tr>
              )}

              {users.data.map((user, index) => (
                <tr key={user.id} className="border-t">
                  <td className="px-4 py-3">{(users.from ?? 1) + index}</td>
                  <td className="px-4 py-3 font-medium">
                    {user.name}
                    {user.id === currentUser.id && (
                      <Badge variant="outline" className="ml-2">
                        Anda
                      </Badge>
                    )}
                  </td>
                  <td className="px-4 py-3">{user.email}</td>
                  <td className="px-4 py-3">
                    <Badge variant={user.role === 'admin' ? 'default' : 'secondary'}>
                      {user.role_label}
                    </Badge>
                  </td>
                  <td className="px-4 py-3 text-muted-foreground">{user.created_at}</td>
                  <td className="px-4 py-3">
                    <div className="flex justify-end gap-2">
                      <Button asChild size="sm" variant="outline">
                        <Link href={`/admin/users/${user.id}/edit`}>
                          <Pencil /> Edit
                        </Link>
                      </Button>

                      {user.id !== currentUser.id && (
                        <Button
                          size="sm"
                          variant="destructive"
                          onClick={() => setDeleting(user)}
                        >
                          <Trash2 /> Hapus
                        </Button>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="flex flex-wrap items-center justify-between gap-2 text-sm">
          <p className="text-muted-foreground">
            Menampilkan {users.from ?? 0}-{users.to ?? 0} dari {users.total} data
          </p>

          <div className="flex flex-wrap gap-1">
            {users.links.map((link, index) =>
              link.url ? (
                <Button
                  key={index}
                  asChild
                  size="sm"
                  variant={link.active ? 'default' : 'outline'}
                >
                  <Link href={link.url} preserveScroll>
                    {cleanLabel(link.label)}
                  </Link>
                </Button>
              ) : (
                <Button key={index} size="sm" variant="outline" disabled>
                  {cleanLabel(link.label)}
                </Button>
              ),
            )}
          </div>
        </div>
      </div>

      <ConfirmDialog
        open={deleting !== null}
        description={`Yakin ingin menghapus user ${deleting?.name}? Tindakan ini tidak dapat dibatalkan.`}
        processing={processing}
        onConfirm={handleDelete}
        onOpenChange={(open) => !open && setDeleting(null)}
      />
    </AppLayout>
  );
}

// Label pagination Laravel berisi entitas HTML &laquo; dan &raquo;
function cleanLabel(label: string): string {
  return label.replace('&laquo;', '«').replace('&raquo;', '»');
}