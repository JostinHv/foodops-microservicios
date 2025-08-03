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
        Schema::create('limites_usos', function (Blueprint $table) {
            $table->id()->autoIncrement();
            $table->foreignId('tenant_suscripcion_id')->nullable()->constrained('tenants_suscripciones');
            $table->string('tipo_recurso')->nullable();
            $table->unsignedInteger('limite_maximo')->nullable();
            $table->unsignedInteger('uso_actual')->nullable();
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
        Schema::dropIfExists('limites_usos');
    }
};
