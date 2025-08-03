package com.foodops.emailmicroservice.domain.port;

import com.foodops.emailmicroservice.domain.model.ContactForm;
import com.foodops.emailmicroservice.domain.model.EmailResponse;

/**
 * Puerto para el servicio de formulario de contacto
 */
public interface ContactFormService {
    
    /**
     * Procesa un formulario de contacto y envía la notificación
     * 
     * @param contactForm Formulario de contacto
     * @return Respuesta del envío
     */
    EmailResponse processContactForm(ContactForm contactForm);
} 