import { CircleAlert, CircleCheck, X } from 'lucide-react';
import { useEffect, useState } from 'react';
import { useSharedProps } from '@/hooks/use-shared-props';

type AlertMessageProps = {
  type: 'success' | 'error';
  message?: string | null;
  onClose?: () => void;
};

export function AlertMessage({ type, message, onClose }: AlertMessageProps) {
  // Pesan berhasil otomatis tertutup setelah 4 detik
  useEffect(() => {
    if (!message || type !== 'success' || !onClose) {
      return;
    }
    const timer = setTimeout(onClose, 4000);
    return () => clearTimeout(timer);
  }, [message, type, onClose]);

  if (!message) {
    return null;
  }

  const Icon = type === 'success' ? CircleCheck : CircleAlert;
  
  const color =
    type === 'success'
      ? 'border-green-200 bg-green-50 text-green-800 dark:border-green-900 dark:bg-green-950 dark:text-green-200'
      : 'border-red-200 bg-red-50 text-red-800 dark:border-red-900 dark:bg-red-950 dark:text-red-200';

  return (
    <div role="alert" className={`flex items-start gap-3 rounded-lg border px-4 py-3 text-sm ${color}`}>
      <Icon className="mt-0.5 size-4 shrink-0" />
      <p className="flex-1">{message}</p>
      {onClose && (
        <button
          type="button"
          onClick={onClose}
          className="opacity-70 hover:opacity-100"
          aria-label="Tutup"
        >
          <X className="size-4" />
        </button>
      )}
    </div>
  );
}

export function FlashMessage() {
  const { flash } = useSharedProps();
  const [success, setSuccess] = useState(flash.success);
  const [error, setError] = useState(flash.error);

  // Tampilkan ulang pesan setiap kali server mengirim flash baru
  useEffect(() => {
    setSuccess(flash.success);
    setError(flash.error);
  }, [flash]);

  return (
    <>
      <AlertMessage
        type="success"
        message={success}
        onClose={() => setSuccess(null)}
      />
      <AlertMessage
        type="error"
        message={error}
        onClose={() => setError(null)}
      />
    </>
  );
}