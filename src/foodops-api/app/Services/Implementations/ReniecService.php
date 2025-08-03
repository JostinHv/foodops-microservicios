<?php

namespace App\Services\Implementations;

use App\Services\Interfaces\IReniecService;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class ReniecService implements IReniecService
{
    private string $reniecServiceUrl;

    public function __construct()
    {
        $this->reniecServiceUrl = env('RENIEC_SERVICE_URL', 'http://reniec-microservice:8080');
    }

    /**
     * Consultar persona por DNI
     * 
     * @param string $dni
     * @return array
     */
    public function consultarPersona(string $dni): array
    {
        try {
            Log::info('Consultando persona en RENIEC', ['dni' => $dni]);

            $response = Http::timeout(10)->get("{$this->reniecServiceUrl}/api/v1/reniec/persona/{$dni}");

            if ($response->successful()) {
                $data = $response->json();
                Log::info('Persona encontrada en RENIEC', ['dni' => $dni, 'nombres' => $data['nombres_completos'] ?? '']);
                
                return [
                    'success' => true,
                    'data' => $data,
                    'message' => 'Persona encontrada'
                ];
            }

            if ($response->status() === 404) {
                Log::warning('Persona no encontrada en RENIEC', ['dni' => $dni]);
                return [
                    'success' => false,
                    'message' => 'Persona no encontrada'
                ];
            }

            Log::error('Error al consultar RENIEC', [
                'dni' => $dni,
                'status' => $response->status(),
                'response' => $response->body()
            ]);

            return [
                'success' => false,
                'message' => 'Error al consultar RENIEC'
            ];

        } catch (\Exception $e) {
            Log::error('Excepción al consultar RENIEC', [
                'dni' => $dni,
                'error' => $e->getMessage()
            ]);

            return [
                'success' => false,
                'message' => 'Error de conexión con RENIEC'
            ];
        }
    }

    /**
     * Verificar estado del microservicio RENIEC
     * 
     * @return array
     */
    public function verificarEstado(): array
    {
        try {
            $response = Http::timeout(5)->get("{$this->reniecServiceUrl}/api/v1/reniec/health");

            if ($response->successful()) {
                return [
                    'success' => true,
                    'message' => 'Servicio RENIEC disponible'
                ];
            }

            return [
                'success' => false,
                'message' => 'Servicio RENIEC no disponible'
            ];

        } catch (\Exception $e) {
            Log::error('Error al verificar estado de RENIEC', [
                'error' => $e->getMessage()
            ]);

            return [
                'success' => false,
                'message' => 'Error de conexión con RENIEC'
            ];
        }
    }
} 