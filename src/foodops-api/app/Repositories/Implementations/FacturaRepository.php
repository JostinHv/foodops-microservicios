<?php

namespace App\Repositories\Implementations;

use App\Models\Factura;
use App\Repositories\Interfaces\IFacturaRepository;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Database\Eloquent\Model;

class FacturaRepository extends BaseRepository implements IFacturaRepository
{

    public function __construct(Factura $modelo)
    {
        parent::__construct($modelo);
    }

    public function obtenerTodos(): Collection
    {
        return $this->modelo->with(['orden', 'metodoPago', 'igv'])->get();
    }

    public function obtenerPorId(int $id): ?Model
    {
        return $this->modelo->with(['orden', 'metodoPago', 'igv'])->find($id);
    }

    public function crear(array $datos): Model
    {
        return $this->modelo->create($datos);
    }

    public function actualizar(int $id, array $datos): bool
    {
        $factura = $this->modelo->find($id);
        if (!$factura) {
            return false;
        }
        return $factura->update($datos);
    }

    public function eliminar(int $id): bool
    {
        $factura = $this->modelo->find($id);
        if (!$factura) {
            return false;
        }
        return $factura->delete();
    }

    public function obtenerPorSucursales(array $sucursalIds): Collection
    {
        return $this->modelo->with(['orden', 'metodoPago', 'igv'])
            ->whereHas('orden', function ($query) use ($sucursalIds) {
                $query->whereIn('sucursal_id', $sucursalIds);
            })
            ->get();
    }

    public function obtenerPorOrden(int $ordenId): ?Model
    {
        return $this->modelo->with(['orden', 'metodoPago', 'igv'])
            ->where('orden_id', $ordenId)
            ->first();
    }

    public function obtenerUltimaFactura(): ?Model
    {
        return $this->modelo->orderBy('id', 'desc')->first();
    }

    protected function aplicarFiltros(Builder $consulta, array $filtros): void
    {

    }

    protected function aplicarBusqueda(Builder $consulta, ?string $searchTerm, ?string $searchColumn): void
    {
        if ($searchTerm) {
            if ($searchColumn) {
                $consulta->where($searchColumn, 'like', '%' . $searchTerm . '%');
            }
        }
    }

    protected function aplicarOrdenamiento(Builder $consulta, ?string $sortField, ?string $sortOrder): void
    {
        if ($sortField && $sortOrder) {
            $consulta->orderBy($sortField, $sortOrder);
        }
    }
}
