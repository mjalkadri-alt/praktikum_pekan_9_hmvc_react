import { Head, Link } from '@inertiajs/react';
import { ClipboardList, ShieldCheck, Users } from 'lucide-react';
import { useSharedProps } from '@/hooks/use-shared-props';
import AppLayout from '@/layouts/app-layout';
import type { BreadcrumbItem } from '@/types';

type DashboardProps = {
  totalPendaftar: number;
  totalUsers: number | null;
};

const breadcrumbs: BreadcrumbItem[] = [{ title: 'Dashboard', href: '/dashboard' }];

export default function Dashboard({ totalPendaftar, totalUsers }: DashboardProps) {
  const { user, isAdmin } = useSharedProps();

  return (
    <AppLayout breadcrumbs={breadcrumbs}>
      <Head title="Dashboard" />
      <div className="flex flex-1 flex-col gap-4 p-4">
        {/* Banner Selamat Datang */}
        <div className="rounded-xl border border-sidebar-border/70 p-6 dark:border-sidebar-border">
          <h1 className="text-xl font-semibold">Selamat datang, {user.name}!</h1>
          <p className="mt-1 flex items-center gap-2 text-sm text-muted-foreground">
            <ShieldCheck className="size-4" />
            Anda login sebagai {isAdmin ? 'Admin' : 'User'}.
          </p>
        </div>

        {/* Grid Statistik */}
        <div className="grid gap-4 md:grid-cols-2">
          {/* Card Total Pendaftar */}
          <div className="flex flex-col justify-between rounded-xl border border-sidebar-border/70 p-6 dark:border-sidebar-border">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-muted-foreground">Total Pendaftar</span>
              <ClipboardList className="size-5 text-muted-foreground" />
            </div>
            <div className="mt-4">
              <div className="text-2xl font-bold">{totalPendaftar}</div>
            </div>
            <div className="mt-4">
              <Link
                href="/pendaftaran"
                className="text-sm font-medium text-primary hover:underline"
              >
                Kelola pendaftaran &rarr;
              </Link>
            </div>
          </div>

          {/* Card Total Users (Khusus Admin) */}
          {isAdmin && totalUsers !== null && (
            <div className="flex flex-col justify-between rounded-xl border border-sidebar-border/70 p-6 dark:border-sidebar-border">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-muted-foreground">Total Pengguna</span>
                <Users className="size-5 text-muted-foreground" />
              </div>
              <div className="mt-4">
                <div className="text-2xl font-bold">{totalUsers}</div>
              </div>
              <div className="mt-4">
                <Link
                  href="/admin/users"
                  className="text-sm font-medium text-primary hover:underline"
                >
                  Kelola user &rarr;
                </Link>
              </div>
            </div>
          )}
        </div>
      </div>
    </AppLayout>
  );
}