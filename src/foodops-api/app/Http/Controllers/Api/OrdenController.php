<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Requests\CrearOrdenRequest;
use App\Http\Responses\ApiResponse;
use App\Services\Interfaces\IOrdenService;
use App\Traits\AuthenticatedUserTrait;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class OrdenController extends Controller
{
    use AuthenticatedUserTrait;

    private IOrdenService $ordenService;

    public function __construct(IOrdenService $ordenService)
    {
        $this->ordenService = $ordenService;
    }

    /**
     * Obtener listado de órdenes
     */
    public function index(): JsonResponse
    {
        try {
            $ordenes = $this->ordenService->obtenerTodos();
            return ApiResponse::success($ordenes, 'Órdenes recuperadas exitosamente');
        } catch (\Exception $e) {
            return ApiResponse::error($e->getMessage());
        }
    }

    /**
     * Crear una nueva orden
     */
    public function store(Request $request): JsonResponse
    {
        try {
            $orden = $this->ordenService->crear($request->all());
            return ApiResponse::success($orden, 'Orden creada exitosamente', 201);
        } catch (\Exception $e) {
            return ApiResponse::error($e->getMessage());
        }
    }

    /**
     * Obtener una orden específica
     */
    public function show(int $id): JsonResponse
    {
        try {
            $orden = $this->ordenService->obtenerPorId($id);
            if (!$orden) {
                return ApiResponse::error('Orden no encontrada', null, 404);
            }

            return ApiResponse::success($orden, 'Orden recuperada exitosamente');
        } catch (\Exception $e) {
            return ApiResponse::error($e->getMessage());
        }
    }

    /**
     * Actualizar una orden existente
     */
    public function update(Request $request, int $id): JsonResponse
    {
        try {
            $actualizado = $this->ordenService->actualizar($id, $request->all());
            $usuario = $this->getCurrentUser();

            if (!$actualizado) {
                return ApiResponse::error('Orden no encontrada', null, 404);
            }

            return ApiResponse::success(null, 'Orden actualizada exitosamente');
        } catch (\Exception $e) {
            return ApiResponse::error($e->getMessage());
        }
    }

    /**
     * Eliminar una orden
     */
    public function destroy(int $id): JsonResponse
    {
        try {
            $eliminado = $this->ordenService->eliminar($id);

            if (!$eliminado) {
                return ApiResponse::error('Orden no encontrada', null, 404);
            }

            return ApiResponse::success(null, 'Orden eliminada exitosamente');
        } catch (\Exception $e) {
            return ApiResponse::error($e->getMessage());
        }
    }

    public function crearOrden(CrearOrdenRequest $request): JsonResponse
    {
        try {
            $orden = $this->ordenService->crearOrden($request->validated(), $this->getCurrentUser()->getAuthIdentifier());
            return ApiResponse::success($orden, 'Orden creada exitosamente', 201);
        } catch (\Exception $e) {
            return ApiResponse::error($e->getMessage());
        }

    }

    public function obtenerOrdenesPorSucursal(): JsonResponse
    {
        try {
            $ordenes = $this->ordenService->obtenerOrdenesPorSucursal($this->getCurrentUser()->getAuthIdentifier());
            return ApiResponse::success($ordenes, 'Órdenes recuperadas exitosamente');
        } catch (\Exception $e) {
            return ApiResponse::error($e->getMessage());
        }
    }

}
