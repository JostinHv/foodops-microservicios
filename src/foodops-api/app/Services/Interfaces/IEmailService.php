<?php

namespace App\Services\Interfaces;

interface IEmailService
{
    /**
     * Envía un formulario de contacto al microservicio de email
     *
     * @param array $data
     * @return array
     */
    public function enviarFormularioContacto(array $data): array;

    /**
     * Verifica el estado del microservicio de email
     *
     * @return array
     */
    public function verificarEstado(): array;
} 