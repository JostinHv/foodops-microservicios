<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('tenants_suscripciones', static function (Blueprint $table) {
            $table->id()->autoIncrement();
            $table->foreignId('plan_suscripcion_id')->nullable()->constrained('planes_suscripciones');
            $table->foreignId('tenant_id')->nullable()->constrained('tenants');
            $table->foreignId('metodo_pago_id')->nullable()->constrained('metodos_pagos');
            $table->date('fecha_inicio')->nullable();
            $table->date('fecha_fin')->nullable();
            $table->string('estado')->nullable();
            $table->decimal('precio_acordado', 10, 2)->nullable();
            $table->boolean('renovacion_automatica')->default(true);
            $table->text('notas')->nullable();
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        if (app()->environment('production')) {
            throw new Exception('The "down" method is disabled in production.');
        }
        Schema::dropIfExists('tenants_suscripciones');
    }
};
