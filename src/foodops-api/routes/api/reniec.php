<?php

use App\Http\Controllers\Api\ReniecController;
use Illuminate\Support\Facades\Route;

Route::prefix('reniec')->group(function () {
    Route::post('/consultar', [ReniecController::class, 'consultarPersona'])->name('api.reniec.consultar');
    Route::get('/estado', [ReniecController::class, 'verificarEstado'])->name('api.reniec.estado');
}); 