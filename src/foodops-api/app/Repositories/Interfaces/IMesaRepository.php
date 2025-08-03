<?php

namespace App\Repositories\Interfaces;

use Illuminate\Database\Eloquent\Collection;
use Illuminate\Database\Eloquent\Model;

interface IMesaRepository
{
    public function obtenerTodos(): Collection;

    public function obtenerPorId(int $id): ?Model;

    public function crear(array $datos): Model;

    public function actualizar(int $id, array $datos): bool;

    public function eliminar(int $id): bool;

    public function obtenerMesasDisponibles(): Collection;

    public function obtenerPorIdConRelaciones(int $id, array $relaciones = []): ?Model;

    public function obtenerMesasPorSucursal(int $sucursalId);

    public function cambiarEstadoMesa(int $id, int $estadoMesaId): bool;

    public function obtenerMesasDisponiblesPorSucursal(int $sucursalId): Collection;

}
