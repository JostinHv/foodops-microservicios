package com.foodops.emailmicroservice.domain.port;

import com.foodops.emailmicroservice.domain.model.EmailRequest;
import com.foodops.emailmicroservice.domain.model.EmailResponse;

/**
 * Puerto (interfaz) para el servicio de email
 * Sigue el principio de inversión de dependencias
 */
public interface EmailService {
    
    /**
     * Envía un email usando el proveedor configurado
     * 
     * @param request Solicitud de email
     * @return Respuesta del envío
     */
    EmailResponse sendEmail(EmailRequest request);
    
    /**
     * Obtiene el nombre del proveedor de email
     * 
     * @return Nombre del proveedor
     */
    String getProviderName();
} 