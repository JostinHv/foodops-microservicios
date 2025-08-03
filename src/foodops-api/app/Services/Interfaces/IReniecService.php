<?php

namespace App\Services\Interfaces;

interface IReniecService
{
    /**
     * Consultar persona por DNI
     * 
     * @param string $dni
     * @return array
     */
    public function consultarPersona(string $dni): array;

    /**
     * Verificar estado del microservicio RENIEC
     * 
     * @return array
     */
    public function verificarEstado(): array;
} 