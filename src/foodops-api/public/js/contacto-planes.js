class ContactoPlanes {
    constructor() {
        this.form = document.getElementById('contactForm');
        this.planSelect = document.getElementById('plan');
        this.planPreview = document.getElementById('planPreview');
        this.submitButton = this.form.querySelector('button[type="submit"]');
        this.currentStep = 1;
        this.totalSteps = 3;
        this.formSections = [
            document.getElementById('step1'),
            document.getElementById('step2'),
            document.getElementById('step3')
        ];

        this.initializeEventListeners();
        this.initializeStepper();
        this.showCurrentStep();
    }

    initializeEventListeners() {
        // Validación del formulario
        this.form.addEventListener('submit', this.handleSubmit.bind(this));

        // Manejo de la previsualización del plan
        this.planSelect.addEventListener('change', this.handlePlanChange.bind(this));

        // Validaciones en tiempo real
        this.initializeValidations();

        // Guardado automático
        this.initializeAutoSave();

        // Botones de navegación
        document.querySelectorAll('.step-nav-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const action = e.target.dataset.action;
                if (action === 'next' && this.validateCurrentStep()) {
                    this.nextStep();
                } else if (action === 'prev') {
                    this.prevStep();
                }
            });
        });
    }

    initializeValidations() {
        // Validación de nombre completo
        const nombreInput = document.getElementById('nombre');
        nombreInput.addEventListener('input', () => this.validateField(nombreInput, {
            required: true,
            minLength: 2,
            maxLength: 100,
            message: 'El nombre completo debe tener entre 2 y 100 caracteres'
        }));

        // Validación de email
        const emailInput = document.getElementById('email');
        emailInput.addEventListener('input', () => this.validateField(emailInput, {
            required: true,
            pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
            message: 'El formato del correo electrónico no es válido'
        }));

        // Validación de teléfono
        const telefonoInput = document.getElementById('telefono');
        telefonoInput.addEventListener('input', () => this.validateField(telefonoInput, {
            required: true,
            pattern: /^[+]?[0-9\s\-\(\)]{7,20}$/,
            message: 'El formato del teléfono no es válido (ej: +34 91 123 45 67)'
        }));

        // Validación de empresa
        const empresaInput = document.getElementById('empresa');
        empresaInput.addEventListener('input', () => this.validateField(empresaInput, {
            required: true,
            minLength: 2,
            maxLength: 100,
            message: 'El nombre de la empresa debe tener entre 2 y 100 caracteres'
        }));

        // Validación de plan
        const planSelect = document.getElementById('plan');
        planSelect.addEventListener('change', () => this.validateField(planSelect, {
            required: true,
            message: 'Debe seleccionar un plan'
        }));

        // Validación de mensaje
        const mensajeInput = document.getElementById('mensaje');
        mensajeInput.addEventListener('input', () => this.validateField(mensajeInput, {
            required: false,
            maxLength: 1000,
            message: 'El mensaje no puede exceder los 1000 caracteres'
        }));
    }

    validateField(field, rules) {
        const value = field.value.trim();
        let isValid = true;
        let errorMessage = '';

        // Validación de campo requerido
        if (rules.required && !value) {
            isValid = false;
            errorMessage = 'Este campo es obligatorio';
        }

        // Validación de longitud mínima
        if (isValid && rules.minLength && value.length < rules.minLength) {
            isValid = false;
            errorMessage = rules.message;
        }

        // Validación de longitud máxima
        if (isValid && rules.maxLength && value.length > rules.maxLength) {
            isValid = false;
            errorMessage = rules.message;
        }

        // Validación de patrón
        if (isValid && rules.pattern && !rules.pattern.test(value)) {
            isValid = false;
            errorMessage = rules.message;
        }

        // Mostrar/ocultar error
        this.showFieldError(field, isValid, errorMessage);
        return isValid;
    }

    showFieldError(field, isValid, message) {
        const errorElement = field.parentNode.querySelector('.invalid-feedback');
        
        if (!isValid) {
            field.classList.add('is-invalid');
            if (errorElement) {
                errorElement.textContent = message;
            }
        } else {
            field.classList.remove('is-invalid');
            field.classList.add('is-valid');
            if (errorElement) {
                errorElement.textContent = '';
            }
        }
    }

    initializeStepper() {
        const stepper = document.createElement('div');
        stepper.className = 'stepper';
        stepper.innerHTML = `
            <div class="step active" data-step="1">
                <span class="step-number">1</span>
                <span class="step-label">Información Personal</span>
            </div>
            <div class="step" data-step="2">
                <span class="step-number">2</span>
                <span class="step-label">Selección de Plan</span>
            </div>
            <div class="step" data-step="3">
                <span class="step-number">3</span>
                <span class="step-label">Mensaje</span>
            </div>
        `;
        this.form.insertBefore(stepper, this.form.firstChild);
    }

    showCurrentStep() {
        this.formSections.forEach((section, index) => {
            if (index + 1 === this.currentStep) {
                section.style.display = 'block';
            } else {
                section.style.display = 'none';
            }
        });

        // Actualizar estado del stepper
        document.querySelectorAll('.step').forEach((step, index) => {
            if (index + 1 < this.currentStep) {
                step.classList.add('completed');
                step.classList.remove('active');
            } else if (index + 1 === this.currentStep) {
                step.classList.add('active');
                step.classList.remove('completed');
            } else {
                step.classList.remove('active', 'completed');
            }
        });
    }

    nextStep() {
        if (this.currentStep < this.totalSteps) {
            this.currentStep++;
            this.showCurrentStep();
        }
    }

    prevStep() {
        if (this.currentStep > 1) {
            this.currentStep--;
            this.showCurrentStep();
        }
    }

    validateCurrentStep() {
        const currentSection = this.formSections[this.currentStep - 1];
        const inputs = currentSection.querySelectorAll('input, select, textarea');
        let isValid = true;

        inputs.forEach(input => {
            // Aplicar validaciones específicas según el campo
            if (input.id === 'nombre') {
                isValid = this.validateField(input, {
                    required: true,
                    minLength: 2,
                    maxLength: 100,
                    message: 'El nombre completo debe tener entre 2 y 100 caracteres'
                }) && isValid;
            } else if (input.id === 'email') {
                isValid = this.validateField(input, {
                    required: true,
                    pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                    message: 'El formato del correo electrónico no es válido'
                }) && isValid;
            } else if (input.id === 'telefono') {
                isValid = this.validateField(input, {
                    required: true,
                    pattern: /^[+]?[0-9\s\-\(\)]{7,20}$/,
                    message: 'El formato del teléfono no es válido (ej: +34 91 123 45 67)'
                }) && isValid;
            } else if (input.id === 'empresa') {
                isValid = this.validateField(input, {
                    required: true,
                    minLength: 2,
                    maxLength: 100,
                    message: 'El nombre de la empresa debe tener entre 2 y 100 caracteres'
                }) && isValid;
            } else if (input.id === 'plan') {
                isValid = this.validateField(input, {
                    required: true,
                    message: 'Debe seleccionar un plan'
                }) && isValid;
            } else if (input.id === 'mensaje') {
                isValid = this.validateField(input, {
                    required: false,
                    maxLength: 1000,
                    message: 'El mensaje no puede exceder los 1000 caracteres'
                }) && isValid;
            } else {
                // Validación genérica para otros campos
                if (input.hasAttribute('required') && !input.value.trim()) {
                    input.classList.add('is-invalid');
                    isValid = false;
                } else {
                    input.classList.remove('is-invalid');
                }
            }
        });

        return isValid;
    }

    handleSubmit(event) {
        event.preventDefault();
        
        if (!this.form.checkValidity()) {
            event.stopPropagation();
            this.form.classList.add('was-validated');
            return;
        }

        this.submitButton.classList.add('btn-loading');
        this.submitButton.disabled = true;
        
        // Obtener datos del formulario
        const formData = new FormData(this.form);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        // Obtener información del plan seleccionado
        const selectedOption = this.planSelect.options[this.planSelect.selectedIndex];
        if (selectedOption.value) {
            data.plan_id = selectedOption.value;
            data.plan_nombre = selectedOption.dataset.nombre;
        }

        // Enviar al endpoint de Laravel
        this.enviarFormulario(data);
    }

    async enviarFormulario(data) {
        try {
            const response = await fetch('/api/v1/contacto/enviar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                this.mostrarExito(result.message);
                this.form.reset();
                localStorage.removeItem('contactFormData');
                this.currentStep = 1;
                this.showCurrentStep();
            } else {
                this.mostrarError(result.message || 'Error al enviar el formulario');
            }
        } catch (error) {
            console.error('Error:', error);
            this.mostrarError('Error de conexión. Por favor, intente nuevamente.');
        } finally {
            this.submitButton.classList.remove('btn-loading');
            this.submitButton.disabled = false;
        }
    }

    mostrarExito(mensaje) {
        // Crear notificación de éxito
        const alert = document.createElement('div');
        alert.className = 'alert alert-success alert-dismissible fade show';
        alert.innerHTML = `
            <i class="bi bi-check-circle-fill me-2"></i>
            ${mensaje}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        this.form.insertBefore(alert, this.form.firstChild);
        
        // Auto-ocultar después de 5 segundos
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    }

    mostrarError(mensaje) {
        // Crear notificación de error
        const alert = document.createElement('div');
        alert.className = 'alert alert-danger alert-dismissible fade show';
        alert.innerHTML = `
            <i class="bi bi-exclamation-triangle-fill me-2"></i>
            ${mensaje}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        this.form.insertBefore(alert, this.form.firstChild);
        
        // Auto-ocultar después de 5 segundos
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    }

    handlePlanChange() {
        const selectedOption = this.planSelect.options[this.planSelect.selectedIndex];
        if (selectedOption.value) {
            const planData = {
                nombre: selectedOption.dataset.nombre,
                precio: selectedOption.dataset.precio,
                intervalo: selectedOption.dataset.intervalo,
                caracteristicas: JSON.parse(selectedOption.dataset.caracteristicas)
            };

            this.updatePlanPreview(planData);
        } else {
            this.planPreview.classList.remove('active');
        }
    }

    updatePlanPreview(planData) {
        const planPreview = this.planPreview;
        planPreview.querySelector('.plan-nombre').textContent = planData.nombre;
        planPreview.querySelector('.plan-price').textContent = `S/. ${planData.precio}/${planData.intervalo}`;

        const caracteristicasContainer = planPreview.querySelector('.plan-caracteristicas');
        caracteristicasContainer.innerHTML = '';

        // Agregar límites
        if (planData.caracteristicas.limites) {
            const limites = planData.caracteristicas.limites;
            Object.entries(limites).forEach(([key, value]) => {
                const feature = document.createElement('div');
                feature.className = 'feature-item';
                feature.innerHTML = `
                    <i class="bi bi-check-circle-fill"></i>
                    <span>${key.charAt(0).toUpperCase() + key.slice(1)}: ${value}</span>
                `;
                caracteristicasContainer.appendChild(feature);
            });
        }

        // Agregar características adicionales
        if (planData.caracteristicas.adicionales) {
            planData.caracteristicas.adicionales.forEach(caracteristica => {
                const feature = document.createElement('div');
                feature.className = 'feature-item';
                feature.innerHTML = `
                    <i class="bi bi-check-circle-fill"></i>
                    <span>${caracteristica}</span>
                `;
                caracteristicasContainer.appendChild(feature);
            });
        }

        planPreview.classList.add('active', 'fade-in');
    }



    initializeAutoSave() {
        const formData = localStorage.getItem('contactFormData');
        if (formData) {
            const data = JSON.parse(formData);
            Object.keys(data).forEach(key => {
                const input = this.form.querySelector(`[name="${key}"]`);
                if (input) {
                    input.value = data[key];
                }
            });
        }

        this.form.addEventListener('input', () => {
            const formData = new FormData(this.form);
            const data = {};
            formData.forEach((value, key) => {
                data[key] = value;
            });
            localStorage.setItem('contactFormData', JSON.stringify(data));
        });
    }

    saveFormData() {
        const formData = new FormData(this.form);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });
        localStorage.setItem('contactFormData', JSON.stringify(data));
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    new ContactoPlanes();
}); 