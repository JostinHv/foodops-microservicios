<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Services\Interfaces\IReniecService;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

class ReniecController extends Controller
{
    private IReniecService $reniecService;

    public function __construct(IReniecService $reniecService)
    {
        $this->reniecService = $reniecService;
    }

    /**
     * Consultar persona por DNI
     * 
     * @param Request $request
     * @return JsonResponse
     */
    public function consultarPersona(Request $request): JsonResponse
    {
        $validator = Validator::make($request->all(), [
            'dni' => 'required|string|regex:/^[0-9]{8}$/'
        ], [
            'dni.required' => 'El DNI es obligatorio',
            'dni.string' => 'El DNI debe ser una cadena de texto',
            'dni.regex' => 'El DNI debe tener exactamente 8 dígitos numéricos'
        ]);

        if ($validator->fails()) {
            return response()->json([
                'success' => false,
                'message' => 'Datos inválidos',
                'errors' => $validator->errors()
            ], 400);
        }

        $dni = $request->input('dni');
        $result = $this->reniecService->consultarPersona($dni);

        if ($result['success']) {
            return response()->json([
                'success' => true,
                'message' => $result['message'],
                'data' => $result['data']
            ]);
        }

        return response()->json([
            'success' => false,
            'message' => $result['message']
        ], 404);
    }

    /**
     * Verificar estado del microservicio RENIEC
     * 
     * @return JsonResponse
     */
    public function verificarEstado(): JsonResponse
    {
        $result = $this->reniecService->verificarEstado();

        if ($result['success']) {
            return response()->json([
                'success' => true,
                'message' => $result['message']
            ]);
        }

        return response()->json([
            'success' => false,
            'message' => $result['message']
        ], 503);
    }
} 