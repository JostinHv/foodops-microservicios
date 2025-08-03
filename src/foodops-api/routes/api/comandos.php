<?php

use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\Route;

Route::prefix('artisan')->group(function () {
    Route::get('/storage-link', function () {
        $exitCode = Artisan::call('storage:link');
        return 'storage:link';
    });

    Route::get('/optimize', function () {
        $exitCode = Artisan::call('optimize');
        return 'optimize';
    });

    Route::get('/config-cache', function () {
        $exitCode = Artisan::call('config:cache');
        return 'config:cache';
    });

    Route::get('/config-clear', function () {
        $exitCode = Artisan::call('config:clear');
        return 'config:clear';
    });

    Route::get('/cache-clear', function () {
        $exitCode = Artisan::call('cache:clear');
        return 'cache:clear';
    });

    Route::get('/route-cache', function () {
        $exitCode = Artisan::call('route:cache');
        return 'route:cache';
    });

    Route::get('/route-clear', function () {
        $exitCode = Artisan::call('route:clear');
        return 'route:clear';
    });

    Route::get('/view-clear', function () {
        $exitCode = Artisan::call('view:clear');
        return 'view:clear';
    });

    Route::get('/migrate-refresh', function () {
        $exitCode = Artisan::call('migrate:refresh', [
            '--force' => true,
        ]);
        return 'migrate:refresh';
    });

});




