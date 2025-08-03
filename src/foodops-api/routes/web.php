<?php

use App\Http\Controllers\Web\AdminController;
use App\Http\Controllers\Web\AuthController;
use App\Http\Controllers\Web\CajeroController;
use App\Http\Controllers\Web\CajeroFacturaController;
use App\Http\Controllers\Web\CocineroOrdenController;
use App\Http\Controllers\Web\ContactoController;
use App\Http\Controllers\Web\GerenteMesaController;
use App\Http\Controllers\Web\GerentePersonalController;
use App\Http\Controllers\Web\GrupoRestauranteController;
use App\Http\Controllers\Web\HomeController;
use App\Http\Controllers\Web\IgvController;
use App\Http\Controllers\Web\MenuController;
use App\Http\Controllers\Web\MetodoPagoController;
use App\Http\Controllers\Web\MovimientoHistorialController;
use App\Http\Controllers\Web\OrdenController;
use App\Http\Controllers\Web\PerfilController;
use App\Http\Controllers\Web\PlanSuscripcionController;
use App\Http\Controllers\Web\RestauranteController;
use App\Http\Controllers\Web\SucursalController;
use App\Http\Controllers\Web\SugerenciaController;
use App\Http\Controllers\Web\TenantController;
use App\Http\Controllers\Web\UsuarioController;
use App\Http\Middleware\WebAuthenticate;
use App\Http\Middleware\WebCheckRole;
use Illuminate\Support\Facades\Route;

Route::get('/phpinfo', function () {
    phpinfo();
});

// Rutas de autenticación
Route::get('/login', [AuthController::class, 'showLoginForm'])->name('login');
Route::post('/login', [AuthController::class, 'login'])->name('login-submit');
Route::get('/register', [AuthController::class, 'showRegisterForm'])->name('register');
Route::post('/register', [AuthController::class, 'register'])->name('register-submit');
Route::post('/check-email', [AuthController::class, 'checkEmail'])->name('check.email');
Route::post('/logout', [AuthController::class, 'logout'])->name('logout');
Route::get('/', [HomeController::class, 'index'])->name('home');
Route::get('/planes', [HomeController::class, 'planes'])->name('detalles.planes');
Route::get('/contacto', [ContactoController::class, 'mostrarFormulario'])->name('contacto');
Route::get('/contacto-planes', [ContactoController::class, 'mostrarFormulario'])->name('contacto.planes');
Route::get('/terminos-condiciones', [HomeController::class, 'terminosCondiciones'])->name('terminos.condiciones');
Route::get('/politica-privacidad', [HomeController::class, 'politicaPrivacidad'])->name('politica.privacidad');

Route::prefix('mesero')->group(function () {
// Rutas protegidas por autenticación
    Route::middleware([WebAuthenticate::class, WebCheckRole::class . ':mesero'])->group(function () {

        Route::get('/check-auth', static function () {
            return response()->json([
                'authenticated' => auth()->check(),
                'user_id' => auth()->id(),
            ]);
        });

        Route::get('/', static function () {
            return view('mesero.dashboard');
        })->name('mesero.dashboard');

        Route::prefix('ordenes')->group(function () {
            Route::get('/', [OrdenController::class, 'index'])->name('mesero.orden.index');
            Route::get('/crear-orden', [OrdenController::class, 'create'])->name('mesero.orden.store');
            Route::post('/crear-orden', [OrdenController::class, 'store'])->name('mesero.orden.store.submit');
            Route::get('/{orden}', [OrdenController::class, 'show'])->name('mesero.orden.show');
            Route::post('/ordenar', [OrdenController::class, 'ordenar'])->name('orden.ordenar');
            Route::post('/{id}/cambiar-estado', [OrdenController::class, 'cambiarEstado'])
                ->name('orden.cambiar-estado');
            Route::post('/{id}/marcar-servida', [OrdenController::class, 'marcarServida'])->name('orden.marcar-servida');
        });

        Route::get('/perfil', [PerfilController::class, 'index'])->name('mesero.perfil');
    });


});

Route::prefix('tenant')->group(function () {
    Route::middleware([WebAuthenticate::class, WebCheckRole::class . ':administrador'])->group(function () {
        Route::get('/dashboard', [AdminController::class, 'dashboard'])
            ->name('tenant.dashboard');
        Route::prefix('grupos')->group(function () {
            Route::get('/', [GrupoRestauranteController::class, 'index'])
                ->name('tenant.grupo-restaurant');
            Route::get('/{grupo}', [GrupoRestauranteController::class, 'show'])
                ->name('tenant.grupo-restaurant.show');
            Route::post('/', [GrupoRestauranteController::class, 'store'])
                ->name('tenant.grupo-restaurant.store');
            Route::put('/{grupo}', [GrupoRestauranteController::class, 'update'])
                ->name('tenant.grupo-restaurant.update');
        });
        Route::prefix('restaurantes')->group(function () {
            Route::get('/', [RestauranteController::class, 'index'])
                ->name('tenant.restaurantes');
            Route::get('/{restaurante}', [RestauranteController::class, 'show'])
                ->name('tenant.restaurantes.show');
            Route::post('/', [RestauranteController::class, 'store'])
                ->name('tenant.restaurantes.store');
            Route::put('/{restaurante}', [RestauranteController::class, 'update'])
                ->name('tenant.restaurantes.update');
            Route::delete('/{restaurante}', [RestauranteController::class, 'destroy'])
                ->name('tenant.restaurantes.destroy');
            Route::put('/{restaurante}/toggle-activo', [RestauranteController::class, 'toggleActivo'])
                ->name('tenant.restaurantes.toggle-activo');
        });
        Route::prefix('sucursales')->group(function () {
            Route::get('/', [SucursalController::class, 'index'])
                ->name('tenant.sucursales');
            Route::get('/{sucursal}', [SucursalController::class, 'show'])
                ->name('tenant.sucursales.show');
            Route::post('/', [SucursalController::class, 'store'])
                ->name('tenant.sucursales.store');
            Route::post('/{sucursal}', [SucursalController::class, 'update'])
                ->name('tenant.sucursales.update');
            Route::post('/{sucursal}/toggle-activo', [SucursalController::class, 'toggleActivo'])
                ->name('tenant.sucursales.toggle-activo');
        });
        Route::prefix('usuarios')->group(function () {
            Route::get('/', [UsuarioController::class, 'index'])
                ->name('tenant.usuarios');
            Route::post('/', [UsuarioController::class, 'store'])
                ->name('tenant.usuarios.store');
            Route::get('/{usuario}', [UsuarioController::class, 'show'])
                ->name('tenant.usuarios.show');
            Route::post('/{usuario}', [UsuarioController::class, 'update'])
                ->name('tenant.usuarios.update');
            Route::post('/{usuario}/toggle-activo', [UsuarioController::class, 'toggleActivo'])
                ->name('tenant.usuarios.toggle-activo');
        });

        // Rutas de perfil
        Route::get('/perfil', [PerfilController::class, 'index'])->name('tenant.perfil');
    });
});

//Rutas de gerente de sucursal
Route::prefix('gerente')->group(function () {
    Route::middleware([WebAuthenticate::class, WebCheckRole::class . ':gerente'])->group(function () {
        Route::get('/dashboard', static function () {
            return view('gerente-sucursal.dashboard');
        })->name('gerente.dashboard');

        // Rutas del menú
        Route::get('/menu', [MenuController::class, 'index'])->name('gerente.menu');
        Route::get('/menu/items/{id}', [MenuController::class, 'showItem'])->name('gerente.menu.items.show');
        Route::post('/menu/items', [MenuController::class, 'storeItem'])->name('gerente.menu.items.store');
        Route::post('/menu/items/{id}', [MenuController::class, 'updateItem'])->name('gerente.menu.items.update');
        Route::post('/menu/items/{id}/toggle-activo', [MenuController::class, 'toggleItemActivo'])->name('gerente.menu.items.toggle-activo');
        Route::post('/menu/items/{id}/toggle-disponible', [MenuController::class, 'toggleItemDisponible'])->name('gerente.menu.items.toggle-disponible');
        Route::post('/menu/upload-imagen', [MenuController::class, 'uploadImagen'])->name('gerente.menu.upload-imagen');

        // Rutas para categorías del menú
        Route::get('/menu/categorias/{id}', [MenuController::class, 'showCategoria'])->name('gerente.menu.categorias.show');
        Route::post('/menu/categorias', [MenuController::class, 'storeCategoria'])->name('gerente.menu.categorias.store');
        Route::post('/menu/categorias/{id}', [MenuController::class, 'updateCategoria'])->name('gerente.menu.categorias.update');
        Route::post('/menu/categorias/{id}/toggle-activo', [MenuController::class, 'toggleCategoriaActivo'])->name('gerente.menu.categorias.toggle-activo');

        Route::group(['prefix' => 'mesas'], function () {
            Route::get('/', [GerenteMesaController::class, 'index'])
                ->name('gerente.mesas');
            Route::post('/', [GerenteMesaController::class, 'store'])
                ->name('gerente.mesas.store');
            Route::get('/{id}', [GerenteMesaController::class, 'show'])
                ->name('gerente.mesas.show');
            Route::get('/{id}/edit', [GerenteMesaController::class, 'edit'])
                ->name('gerente.mesas.edit');
            Route::put('/{id}', [GerenteMesaController::class, 'update'])
                ->name('gerente.mesas.update');
            Route::delete('/{id}', [GerenteMesaController::class, 'destroy'])
                ->name('gerente.mesas.destroy');
            Route::post('/{id}/estado', [GerenteMesaController::class, 'cambiarEstado'])
                ->name('gerente.mesas.cambiar-estado');
        });
        Route::prefix('personal')->group(function () {
            Route::get('/', [GerentePersonalController::class, 'index'])->name('gerente.personal');
            Route::post('/', [GerentePersonalController::class, 'store'])->name('gerente.personal.store');
            Route::get('/{id}', [GerentePersonalController::class, 'show'])->name('gerente.personal.show');
            Route::put('/{id}', [GerentePersonalController::class, 'update'])->name('gerente.personal.update');
            Route::post('/{id}/toggle-activo', [GerentePersonalController::class, 'toggleActivo'])->name('gerente.personal.toggle-activo');
            Route::post('/check-email', [GerentePersonalController::class, 'checkEmail'])->name('gerente.personal.check-email');
        });
//        Route::prefix('facturacion')->group(function () {
//            Route::get('/', [GerenteFacturaController::class, 'index'])->name('gerente.facturacion');
//            Route::post('/', [GerenteFacturaController::class, 'store'])->name('gerente.facturacion.store');
//            Route::get('/{id}', [GerenteFacturaController::class, 'show'])->name('gerente.facturacion.show');
//            Route::put('/{id}', [GerenteFacturaController::class, 'update'])->name('gerente.facturacion.update');
//            Route::delete('/{id}', [GerenteFacturaController::class, 'destroy'])->name('gerente.facturacion.destroy');
//            Route::post('/calcular-totales', [GerenteFacturaController::class, 'calcularTotales'])->name('gerente.facturacion.calcular-totales');
//            Route::get('/{id}/pdf', [GerenteFacturaController::class, 'generarPDF'])->name('gerente.facturacion.pdf');
//            Route::get('/{id}/pdf-pos', [GerenteFacturaController::class, 'generarPDFPOS'])->name('gerente.facturacion.pdf-pos');
//        });

        // Rutas de perfil
        Route::get('/perfil', [PerfilController::class, 'index'])->name('gerente.perfil');
        Route::post('/perfil', [PerfilController::class, 'actualizar'])->name('gerente.perfil.actualizar');
        Route::post('/perfil/contrasenia', [PerfilController::class, 'actualizarContrasenia'])->name('gerente.perfil.contrasenia');
    });
});

// Rutas de super administrador
Route::prefix('superadmin')->group(function () {
    Route::middleware([WebAuthenticate::class, WebCheckRole::class . ':superadmin'])->group(function () {
        Route::get('/dashboard', static function () {
            return view('super-admin.dashboard');
        })->name('superadmin.dashboard');

        // Ruta de perfil
        Route::get('/perfil', [PerfilController::class, 'index'])->name('perfil');

        Route::prefix('tenant')->group(function () {
            Route::get('/', [TenantController::class, 'index'])->name('superadmin.tenant');
            Route::post('/', [TenantController::class, 'store'])->name('superadmin.tenant.store');
            Route::get('/{id}', [TenantController::class, 'show'])->name('superadmin.tenant.show');
            Route::get('/detalles/{id}', [TenantController::class, 'obtenerDetalles'])->name('superadmin.tenant.detalles');
            Route::put('/{id}', [TenantController::class, 'update'])->name('superadmin.tenant.update');
            Route::delete('/{id}', [TenantController::class, 'destroy'])->name('superadmin.tenant.destroy');
            Route::put('/{id}/toggle-activo', [TenantController::class, 'toggleActivo'])->name('superadmin.tenant.toggle-activo');
            Route::post('/check-domain', [TenantController::class, 'checkDomain'])->name('superadmin.tenant.check-domain');
            // Rutas para gestión de usuarios del tenant
            Route::post('/{id}/usuarios', [TenantController::class, 'agregarUsuario'])
                ->name('superadmin.tenant.usuarios.store');
            Route::put('/{tenantId}/usuarios/{usuarioId}/toggle-estado', [TenantController::class, 'toggleEstadoUsuario'])
                ->name('superadmin.tenant.usuarios.toggle-estado');
            Route::put('/{tenantId}/usuarios/{usuarioId}/rol', [TenantController::class, 'cambiarRolUsuario'])
                ->name('superadmin.tenant.usuarios.cambiar-rol');
        });

        Route::prefix('planes')->group(function () {
            Route::get('/', [PlanSuscripcionController::class, 'index'])->name('planes');
            Route::post('/', [PlanSuscripcionController::class, 'store'])->name('superadmin.planes.store');
            Route::get('/{plan}', [PlanSuscripcionController::class, 'show'])
                ->name('superadmin.planes.show');
            Route::post('/{plan}', [PlanSuscripcionController::class, 'update'])->name('planes.update');
            Route::post('/{plan}/toggle-activo', [PlanSuscripcionController::class, 'toggleActivo'])->name('superadmin.planes.toggle-activo');
        });
        Route::prefix('pago')->group(function () {
            Route::get('/', [MetodoPagoController::class, 'index'])->name('superadmin.pago');
            Route::post('/', [MetodoPagoController::class, 'store'])->name('superadmin.pago.store');
            Route::put('/{id}', [MetodoPagoController::class, 'update'])->name('superadmin.pago.update');
            Route::post('/{id}/toggle-activo', [MetodoPagoController::class, 'toggleActivo'])->name('superadmin.pago.toggle-activo');
        });
        Route::prefix('igv')->group(function () {
            Route::get('/', [IgvController::class, 'index'])->name('superadmin.igv');
            Route::post('/', [IgvController::class, 'store'])->name('superadmin.igv.store');
            Route::put('/{id}', [IgvController::class, 'update'])->name('superadmin.igv.update');
            Route::post('/{id}/toggle-activo', [IgvController::class, 'toggleActivo'])->name('superadmin.igv.toggle-activo');
        });

        // Rutas de auditoría
        Route::get('/movimientos', [MovimientoHistorialController::class, 'index'])->name('superadmin.movimientos');
        Route::get('/movimientos/usuario/{id}', [MovimientoHistorialController::class, 'getUserDetail'])->name('superadmin.movimientos.user-detail');
    });
});

// Rutas para sugerencias (superadmin)
Route::prefix('superadmin')->middleware([WebAuthenticate::class, WebCheckRole::class . ':superadmin'])->group(function () {
    Route::get('/sugerencias', [SugerenciaController::class, 'index'])->name('superadmin.sugerencias.index');
    Route::get('/sugerencias/{id}', [SugerenciaController::class, 'show'])->name('superadmin.sugerencias.show');
    Route::put('/sugerencias/{id}', [SugerenciaController::class, 'update'])->name('superadmin.sugerencias.update');
    Route::delete('/sugerencias/{id}', [SugerenciaController::class, 'destroy'])->name('superadmin.sugerencias.destroy');
});

// Ruta para crear sugerencias (cualquier autenticado)
Route::middleware([WebAuthenticate::class])->group(function () {
    Route::get('/sugerencias/crear', [SugerenciaController::class, 'create'])->name('sugerencias.create');
    Route::post('/sugerencias', [SugerenciaController::class, 'store'])->name('sugerencias.store');
    Route::get('/sugerencias/historial', [SugerenciaController::class, 'historial'])->name('sugerencias.historial');
});

//Rutas de cajero
Route::prefix('cajero')->group(function () {
    Route::middleware([WebAuthenticate::class, WebCheckRole::class . ':cajero'])->group(function () {
        Route::get('/dashboard', static function () {
            return view('cajero.dashboard');
        })->name('cajero.dashboard');

        Route::prefix('facturacion')->group(function () {
            Route::get('/', [CajeroFacturaController::class, 'index'])->name('cajero.facturacion');
            Route::post('/', [CajeroFacturaController::class, 'store'])->name('cajero.facturacion.store');
            Route::get('/{id}', [CajeroFacturaController::class, 'show'])->name('cajero.facturacion.show');
            Route::put('/{id}', [CajeroFacturaController::class, 'update'])->name('cajero.facturacion.update');
            Route::post('/calcular-totales', [CajeroFacturaController::class, 'calcularTotales'])->name('cajero.facturacion.calcular-totales');
            Route::post('/{ordenId}/cambiar-estado', [CajeroFacturaController::class, 'cambiarEstadoOrden'])->name('cajero.facturacion.cambiar-estado');
            Route::get('/{id}/pdf', [CajeroFacturaController::class, 'generarPDF'])->name('cajero.facturacion.pdf');
            Route::get('/{id}/pdf-pos', [CajeroFacturaController::class, 'generarPDFPOS'])->name('cajero.facturacion.pdf-pos');
            Route::get('/orden/{ordenId}', [CajeroFacturaController::class, 'showOrden'])->name('cajero.facturacion.orden.show');

            // Rutas específicas para actualizaciones AJAX
            Route::get('/api/ordenes', [CajeroFacturaController::class, 'getOrdenesActualizadas'])->name('cajero.facturacion.api.ordenes');
            Route::get('/api/facturas', [CajeroFacturaController::class, 'getFacturasActualizadas'])->name('cajero.facturacion.api.facturas');
        });

        Route::prefix('caja')->group(function () {
            Route::get('/', [CajeroController::class, 'caja'])->name('cajero.caja');
            Route::get('/apertura', [CajeroController::class, 'aperturaCaja'])->name('cajero.caja.apertura');
            Route::post('/apertura', [CajeroController::class, 'storeAperturaCaja'])->name('cajero.caja.apertura.store');
            Route::get('/cierre', [CajeroController::class, 'cierreCaja'])->name('cajero.caja.cierre');
            Route::post('/cierre', [CajeroController::class, 'storeCierreCaja'])->name('cajero.caja.cierre.store');
            Route::get('/movimientos', [CajeroController::class, 'movimientosCaja'])->name('cajero.caja.movimientos');
            // Endpoints AJAX para estado de caja, validaciones, etc. (opcional)
        });

        // Rutas de perfil
        Route::get('/perfil', [PerfilController::class, 'index'])->name('cajero.perfil');
        Route::post('/perfil', [PerfilController::class, 'actualizar'])->name('cajero.perfil.actualizar');
        Route::post('/perfil/contrasenia', [PerfilController::class, 'actualizarContrasenia'])->name('cajero.perfil.contrasenia');
    });
});

//Rutas de cocinero
Route::prefix('cocinero')->group(function () {
    Route::middleware([WebAuthenticate::class, WebCheckRole::class . ':cocinero'])->group(function () {
        Route::prefix('ordenes')->group(function () {
            Route::get('/', [CocineroOrdenController::class, 'index'])->name('cocinero.orden.index');
            Route::get('/{orden}', [CocineroOrdenController::class, 'show'])->name('cocinero.orden.show');
            Route::post('/ordenar', [CocineroOrdenController::class, 'ordenar'])->name('cocinero.orden.ordenar');
            Route::post('/{id}/cambiar-estado', [CocineroOrdenController::class, 'cambiarEstado'])
                ->name('cocinero.orden.cambiar-estado');
            Route::post('/{id}/marcar-servida', [CocineroOrdenController::class, 'marcarServida'])->name('cocinero.orden.marcar-servida');
        });
    });
});

//Rutas de cocinero

//Rutas provisionales
/*Route::get('/cajero', function () {
    return view('cajero.facturacion');
})->name('cajero.facturacion');*/
