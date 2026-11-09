<?php

namespace Database\Seeders;

use App\Models\User;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    use WithoutModelEvents;

    /**
     * Seed the application's database.
     */
    public function run(): void
    {
        $admin = User::factory()->admin()->make([
            'name' => 'Administrator',
            'password' => 'password',
        ])->forceFill(['email' => 'admin@example.com'])->getAttributes();

        User::firstOrCreate(['email' => 'admin@example.com'], $admin);

        $user = User::factory()->make([
            'name' => 'User Biasa',
            'password' => 'password',
        ])->forceFill(['email' => 'user@example.com'])->getAttributes();

        User::firstOrCreate(['email' => 'user@example.com'], $user);
    }
}