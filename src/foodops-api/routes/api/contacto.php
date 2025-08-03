<?php

use App\Http\Controllers\Api\ContactoController;
use Illuminate\Support\Facades\Route;

Route::prefix('contacto')->group(function () {
    Route::post('/enviar', [ContactoController::class, 'enviarFormulario'])->name('api.contacto.enviar');
    Route::get('/estado', [ContactoController::class, 'verificarEstado'])->name('api.contacto.estado');
}); 