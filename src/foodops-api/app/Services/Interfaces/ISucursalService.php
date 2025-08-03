<?php

namespace App\Services\Interfaces;

use Illuminate\Database\Eloquent\Collection;
use Illuminate\Database\Eloquent\Model;

interface ISucursalService extends IActivoBoolService
{
    public function obtenerTodos(): Collection;

    public function obtenerPorId(int $id): ?Model;

    public function crear(array $datos): Model;

    public function actualizar(int $id, array $datos): bool;

    public function eliminar(int $id): bool;

    public function cambiarEstadoAutomatico(int $id): bool;

    public function cambiarEstado(int $id, int $activo): bool;

    public function obtenerActivos(): Collection;

    public function obtenerUltimoActivo(): Collection;

    public function obtenerPorUsuarioId(int $usuarioId): Collection;

    public function gerenteTieneSucursal(int $usuarioId): bool;
}
