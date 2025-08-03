<?php

namespace App\Repositories\Implementations;


use App\Models\CategoriaMenu;
use App\Repositories\Interfaces\ICategoriaMenuRepository;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Collection;

class CategoriaMenuRepository extends ActivoBoolRepository implements ICategoriaMenuRepository
{

    public function __construct(CategoriaMenu $modelo)
    {
        parent::__construct($modelo);
    }

    protected function aplicarFiltros(Builder $consulta, array $filtros): void
    {
        // TODO: Implement aplicarFiltros() method.
    }

    protected function aplicarBusqueda(Builder $consulta, ?string $searchTerm, ?string $searchColumn): void
    {
        // TODO: Implement aplicarBusqueda() method.
    }

    protected function aplicarOrdenamiento(Builder $consulta, ?string $sortField, ?string $sortOrder): void
    {
        // TODO: Implement aplicarOrdenamiento() method.
    }

    public function obtenerCategoriasPorSucursal(int $sucursalId): Collection
    {
        return $this->modelo->where('sucursal_id', $sucursalId)
            ->where('activo', true)
            ->get();
    }
}
