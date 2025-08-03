document.addEventListener('DOMContentLoaded', function () {
    try {
        console.log('Inicializando nuevaorden.js...');

        // Elementos del DOM
        const ordenForm = document.getElementById('ordenForm');
    const tabla = document.getElementById('detalle-tabla').getElementsByTagName('tbody')[0];
        const totalProductosBadge = document.getElementById('total-productos');
        const totalOrdenElement = document.getElementById('total-orden');
        const buscarProductoInput = document.getElementById('buscarProducto');
        const mesaInput = document.getElementById('mesa_id');

        if (!ordenForm || !tabla || !totalProductosBadge || !totalOrdenElement) {
            throw new Error('No se pudieron encontrar todos los elementos necesarios en el DOM');
        }

        console.log('Elementos del DOM encontrados correctamente');

        // Inicializar el servicio de orden
        window.ordenService = new OrdenService(tabla);
        console.log('OrdenService inicializado');

        // Función para actualizar totales
        function actualizarTotales() {
            const productos = ordenService.orden.getProductos();
            const total = productos.reduce((sum, producto) => sum + parseFloat(producto.precioTotal), 0);

            totalProductosBadge.textContent = `${productos.length} productos`;
            totalOrdenElement.textContent = `S/. ${total.toFixed(2)}`;

            console.log('Totales actualizados:', {
                cantidadProductos: productos.length,
                total: total
            });
        }

        // Función para actualizar cantidad de producto
        function actualizarCantidadProducto(card, cantidad) {
            try {
                const productoId = parseInt(card.dataset.id);
                if (isNaN(productoId)) {
                    throw new Error('ID de producto inválido');
                }

                console.log('Actualizando cantidad de producto:', {
                    id: productoId,
                    cantidad: cantidad
                });

                const nombreProducto = card.dataset.nombre;
                const precio = parseFloat(card.dataset.precio);

                if (cantidad > 0) {
                    const producto = new Producto(productoId, nombreProducto, precio, cantidad);
                    ordenService.agregarProducto(producto);
        } else {
                    ordenService.eliminarProducto(productoId);
                }

                actualizarTotales();
                console.log('Cantidad actualizada exitosamente');
            } catch (error) {
                console.error('Error al actualizar cantidad:', error);
                alert('Error al actualizar la cantidad: ' + error.message);
            }
        }

        // Evento para buscar productos
        buscarProductoInput.addEventListener('input', function(e) {
            const busqueda = e.target.value.toLowerCase();
            document.querySelectorAll('.producto-item').forEach(item => {
                const nombre = item.dataset.nombre;
                item.style.display = nombre.includes(busqueda) ? '' : 'none';
            });
        });

        // Eventos para los botones de cantidad
        document.querySelectorAll('.producto-card').forEach(card => {
            const input = card.querySelector('.cantidad-input');
            const btnMenos = card.querySelector('.btn-cantidad-menos');
            const btnMas = card.querySelector('.btn-cantidad-mas');

            btnMenos.addEventListener('click', () => {
                const nuevaCantidad = Math.max(0, parseInt(input.value) - 1);
                input.value = nuevaCantidad;
                actualizarCantidadProducto(card, nuevaCantidad);
            });

            btnMas.addEventListener('click', () => {
                const nuevaCantidad = parseInt(input.value) + 1;
                input.value = nuevaCantidad;
                actualizarCantidadProducto(card, nuevaCantidad);
            });

            input.addEventListener('change', () => {
                const nuevaCantidad = Math.max(0, parseInt(input.value) || 0);
                input.value = nuevaCantidad;
                actualizarCantidadProducto(card, nuevaCantidad);
            });
        });

        // Evento para eliminar producto
        tabla.addEventListener('click', function(e) {
            const btnEliminar = e.target.closest('.eliminar-producto');
            if (btnEliminar) {
                try {
                    const productoId = parseInt(btnEliminar.getAttribute('data-producto-id'));
                    console.log('Intentando eliminar producto con ID:', productoId);

                    if (isNaN(productoId)) {
                        throw new Error('ID de producto inválido');
                    }

                    // Encontrar y resetear la tarjeta correspondiente
                    const card = document.querySelector(`.producto-card[data-id="${productoId}"]`);
                    if (card) {
                        const input = card.querySelector('.cantidad-input');
                        input.value = 0;
                    }

                    // Eliminar el producto
                    ordenService.eliminarProducto(productoId);
                    actualizarTotales();
                    console.log('Producto eliminado exitosamente');
                } catch (error) {
                    console.error('Error al eliminar producto:', error);
                    alert('Error al eliminar el producto: ' + error.message);
                }
            }
        });

        // Manejo de selección de mesas
        document.querySelectorAll('.mesa-card').forEach(card => {
            card.addEventListener('click', function() {
                // Remover selección previa
                document.querySelectorAll('.mesa-card').forEach(c => {
                    c.classList.remove('selected');
            });

                // Agregar selección a la mesa actual
                this.classList.add('selected');

                // Actualizar el input oculto con el ID de la mesa
                const mesaId = this.dataset.id;
                mesaInput.value = mesaId;

                console.log('Mesa seleccionada:', mesaId);
    });
        });

        // Evento para enviar formulario
        ordenForm.addEventListener('submit', function (e) {
            try {
                console.log('Iniciando envío del formulario...');
        e.preventDefault();

                // Validar que se haya seleccionado una mesa
                if (!mesaInput.value) {
                    alert('Por favor, seleccione una mesa');
            return;
        }

                // Preparar el formulario con los productos
                if (ordenService.prepararFormulario(this)) {
                    const datosFormulario = {
                        cliente: this.querySelector('[name="cliente"]').value,
                        mesa_id: mesaInput.value,
                        productos: ordenService.orden.toRequestFormat().productos
                    };

                    console.log('Datos a enviar:', datosFormulario);
                    console.log('Formulario preparado correctamente, enviando...');

                    // Verificar que los productos se hayan agregado correctamente al formulario
                    const productosInputs = this.querySelectorAll('input[name^="productos"]');
                    console.log('Campos de productos en el formulario:', productosInputs.length);
                    productosInputs.forEach(input => {
                        console.log('Campo:', input.name, 'Valor:', input.value);
        });

        this.submit();
                }
            } catch (error) {
                console.error('Error al enviar el formulario:', error);
                alert('Error al enviar el formulario: ' + error.message);
            }
        });

        console.log('Inicialización completada exitosamente');

        // ===== FUNCIONALIDAD RENIEC =====
        
        // Elementos del DOM para RENIEC
        const clienteInput = document.getElementById('cliente');
        const dniInput = document.getElementById('dni');
        const dniContainer = document.getElementById('dni-container');
        const btnBuscarDni = document.getElementById('btn-buscar-dni');
        const reniecStatus = document.getElementById('reniec-status');
        const reniecStatusText = document.getElementById('reniec-status-text');

        // Verificar estado del servicio RENIEC al cargar la página
        async function verificarEstadoReniec() {
            try {
                reniecStatus.style.display = 'block';
                reniecStatusText.textContent = 'Verificando servicio RENIEC...';

                const response = await fetch('/api/v1/reniec/estado', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
                    }
                });

                const result = await response.json();

                if (result.success) {
                    // Servicio disponible - mostrar campo DNI
                    dniContainer.style.display = 'block';
                    clienteInput.placeholder = 'Ingrese DNI para buscar automáticamente el nombre';
                    reniecStatusText.textContent = 'Servicio RENIEC disponible';
                    reniecStatus.className = 'mt-2 text-success';
                    
                    console.log('Servicio RENIEC disponible');
                } else {
                    // Servicio no disponible - ocultar campo DNI
                    dniContainer.style.display = 'none';
                    clienteInput.placeholder = 'Nombre del cliente';
                    clienteInput.readOnly = false;
                    reniecStatusText.textContent = 'Servicio RENIEC no disponible';
                    reniecStatus.className = 'mt-2 text-warning';
                    
                    console.log('Servicio RENIEC no disponible');
                }
            } catch (error) {
                console.error('Error al verificar estado de RENIEC:', error);
                dniContainer.style.display = 'none';
                clienteInput.placeholder = 'Nombre del cliente';
                clienteInput.readOnly = false;
                reniecStatusText.textContent = 'Error al verificar servicio RENIEC';
                reniecStatus.className = 'mt-2 text-danger';
            }
        }

        // Función para consultar persona por DNI
        async function consultarPersona(dni) {
            try {
                // Mostrar loading
                btnBuscarDni.innerHTML = '<i class="bi bi-arrow-clockwise spin"></i>';
                btnBuscarDni.disabled = true;
                dniInput.disabled = true;

                const response = await fetch('/api/v1/reniec/consultar', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
                    },
                    body: JSON.stringify({ dni: dni })
                });

                const result = await response.json();

                if (result.success) {
                    // Persona encontrada
                    clienteInput.value = result.data.nombres_completos;
                    clienteInput.classList.add('is-valid');
                    clienteInput.classList.remove('is-invalid');
                    
                    // Mostrar mensaje de éxito
                    mostrarMensaje('Persona encontrada: ' + result.data.nombres_completos, 'success');
                    
                    console.log('Persona encontrada:', result.data);
                } else {
                    // Persona no encontrada
                    clienteInput.value = '';
                    clienteInput.classList.add('is-invalid');
                    clienteInput.classList.remove('is-valid');
                    
                    mostrarMensaje(result.message || 'Persona no encontrada', 'danger');
                    
                    console.log('Persona no encontrada');
                }
            } catch (error) {
                console.error('Error al consultar RENIEC:', error);
                mostrarMensaje('Error de conexión con RENIEC', 'danger');
            } finally {
                // Restaurar botón
                btnBuscarDni.innerHTML = '<i class="bi bi-search"></i>';
                btnBuscarDni.disabled = false;
                dniInput.disabled = false;
            }
        }

        // Función para mostrar mensajes
        function mostrarMensaje(mensaje, tipo) {
            // Crear alerta temporal
            const alert = document.createElement('div');
            alert.className = `alert alert-${tipo} alert-dismissible fade show position-fixed`;
            alert.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
            alert.innerHTML = `
                <i class="bi bi-${tipo === 'success' ? 'check-circle' : 'exclamation-triangle'}-fill me-2"></i>
                ${mensaje}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            
            document.body.appendChild(alert);
            
            // Auto-ocultar después de 5 segundos
            setTimeout(() => {
                if (alert.parentNode) {
                    alert.remove();
                }
            }, 5000);
        }

        // Evento para buscar por DNI
        btnBuscarDni.addEventListener('click', function() {
            const dni = dniInput.value.trim();
            
            if (!dni) {
                mostrarMensaje('Por favor, ingrese un DNI', 'warning');
                return;
            }
            
            if (!/^[0-9]{8}$/.test(dni)) {
                mostrarMensaje('El DNI debe tener exactamente 8 dígitos numéricos', 'warning');
                return;
            }
            
            consultarPersona(dni);
        });

        // Evento para buscar al presionar Enter en el campo DNI
        dniInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                btnBuscarDni.click();
            }
        });

        // Evento para limpiar cliente cuando se cambia el DNI
        dniInput.addEventListener('input', function() {
            if (clienteInput.value) {
                clienteInput.value = '';
                clienteInput.classList.remove('is-valid', 'is-invalid');
            }
        });

        // Verificar estado de RENIEC al cargar la página
        verificarEstadoReniec();

        console.log('Funcionalidad RENIEC inicializada');
    } catch (error) {
        console.error('Error en la inicialización:', error);
        alert('Error al inicializar la página: ' + error.message);
    }
});
