<?php

namespace App\Services\Implementations;

use App\Repositories\Interfaces\IMetodoPagoRepository;
use App\Services\Interfaces\IMetodoPagoService;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Database\Eloquent\Model;

readonly class MetodoPagoService implements IMetodoPagoService
{

    public function __construct(
        private IMetodoPagoRepository $repository
    )
    {
    }

    public function obtenerTodos(): Collection
    {
        return $this->repository->obtenerTodos();
    }

    public function obtenerPorId(int $id): ?Model
    {
        return $this->repository->obtenerPorId($id);
    }

    public function crear(array $datos): Model
    {
        return $this->repository->crear($datos);
    }

    public function actualizar(int $id, array $datos): bool
    {
        return $this->repository->actualizar($id, $datos);
    }

    public function eliminar(int $id): bool
    {
        return $this->repository->eliminar($id);
    }

    public function cambiarEstadoAutomatico(int $id): bool
    {
        return $this->repository->cambiarEstadoAutomatico($id);
    }

    public function cambiarEstado(int $id, int $activo): bool
    {
        return $this->repository->cambiarEstado($id, $activo);
    }

    public function obtenerActivos(): Collection
    {
        return $this->repository->obtenerActivos();
    }

    public function obtenerUltimoActivo(): Collection
    {
        return $this->repository->obtenerUltimoActivo();
    }
}
