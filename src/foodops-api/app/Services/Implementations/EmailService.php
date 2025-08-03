<?php

namespace App\Services\Implementations;

use App\Services\Interfaces\IEmailService;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class EmailService implements IEmailService
{
    private string $emailServiceUrl;

    public function __construct()
    {
        // ✅ URL directamente definida (sin depender de .env)
        $this->emailServiceUrl = 'http://email-microservice:8080/email-service';
    }

    public function enviarFormularioContacto(array $data): array
    {
        try {
            $payload = [
                'fullName' => $data['nombre'],
                'email' => $data['email'],
                'phone' => $data['telefono'],
                'companyName' => $data['empresa'] ?? '',
                'interestedPlan' => $data['plan_nombre'] ?? '',
                'message' => $data['mensaje'] ?? null
            ];
    
            $url = $this->emailServiceUrl . '/api/v1/contact/submit';
    
            Log::info('[EmailService] → Enviando formulario al microservicio de email', [
                'request_url' => $url,
                'payload' => $payload
            ]);
    
            $response = Http::timeout(30)->post($url, $payload);
    
            Log::info('[EmailService] ← Respuesta recibida del microservicio', [
                'status' => $response->status(),
                'body' => $response->body()
            ]);
    
            if ($response->successful()) {
                $result = $response->json();
                Log::info('[EmailService] ✓ Envío exitoso', $result);
    
                return [
                    'success' => true,
                    'message' => 'Formulario enviado exitosamente',
                    'data' => $result
                ];
            } else {
                Log::warning('[EmailService] ⚠ Error al enviar formulario', [
                    'status' => $response->status(),
                    'body' => $response->body()
                ]);
    
                return [
                    'success' => false,
                    'message' => 'Error al enviar el formulario',
                    'error' => $response->body()
                ];
            }
        } catch (\Exception $e) {
            Log::error('[EmailService] ❌ Excepción al enviar formulario', [
                'exception' => $e->getMessage(),
                'trace' => $e->getTraceAsString()
            ]);
    
            return [
                'success' => false,
                'message' => 'Error de conexión con el servicio de email',
                'error' => $e->getMessage()
            ];
        }
    }
    
    public function verificarEstado(): array
    {
        try {
            $url = $this->emailServiceUrl . '/api/v1/contact/health';

            Log::info('Verificando estado del microservicio de email', ['url' => $url]);

            $response = Http::timeout(10)->get($url);

            if ($response->successful()) {
                return [
                    'success' => true,
                    'status' => 'online',
                    'message' => $response->body()
                ];
            } else {
                return [
                    'success' => false,
                    'status' => 'offline',
                    'message' => 'Servicio no disponible'
                ];
            }
        } catch (\Exception $e) {
            return [
                'success' => false,
                'status' => 'error',
                'message' => 'Error de conexión: ' . $e->getMessage()
            ];
        }
    }
}
