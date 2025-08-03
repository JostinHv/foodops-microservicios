<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Services\Interfaces\IEmailService;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;

class ContactoController extends Controller
{
    protected IEmailService $emailService;

    public function __construct(IEmailService $emailService)
    {
        $this->emailService = $emailService;
    }

    /**
     * Envía el formulario de contacto al microservicio de email
     *
     * @param Request $request
     * @return JsonResponse
     */
    public function enviarFormulario(Request $request): JsonResponse
    {
        $request->validate([
            'nombre' => 'required|string|max:255',
            'email' => 'required|email|max:255',
            'telefono' => 'required|string|max:20',
            'empresa' => 'nullable|string|max:255',
            'plan_id' => 'required|integer',
            'plan_nombre' => 'required|string|max:255',
            'mensaje' => 'nullable|string|max:1000'
        ]);

        $data = $request->only([
            'nombre',
            'email', 
            'telefono',
            'empresa',
            'plan_id',
            'plan_nombre',
            'mensaje'
        ]);

        $result = $this->emailService->enviarFormularioContacto($data);

        if ($result['success']) {
            return response()->json([
                'success' => true,
                'message' => 'Formulario enviado exitosamente',
                'data' => $result['data'] ?? null
            ], 200);
        } else {
            return response()->json([
                'success' => false,
                'message' => $result['message'],
                'error' => $result['error'] ?? null
            ], 500);
        }
    }

    /**
     * Verifica el estado del microservicio de email
     *
     * @return JsonResponse
     */
    public function verificarEstado(): JsonResponse
    {
        $result = $this->emailService->verificarEstado();

        return response()->json($result, $result['success'] ? 200 : 503);
    }
} 