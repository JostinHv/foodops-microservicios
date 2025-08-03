package com.foodops.emailmicroservice.application.service;

import com.foodops.emailmicroservice.domain.model.ContactForm;
import com.foodops.emailmicroservice.domain.model.EmailRequest;
import com.foodops.emailmicroservice.domain.model.EmailResponse;
import com.foodops.emailmicroservice.domain.port.ContactFormService;
import com.foodops.emailmicroservice.domain.port.EmailService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * Implementación del servicio de formulario de contacto
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class ContactFormServiceImpl implements ContactFormService {
    
    private final EmailService emailService;
    
    @Value("${app.email.owner:admin@foodops.com}")
    private String ownerEmail;
    
    @Value("${app.email.from:noreply@foodops.com}")
    private String fromEmail;
    
    @Override
    public EmailResponse processContactForm(ContactForm contactForm) {
        log.info("Procesando formulario de contacto para: {}", contactForm.getEmail());
        
        try {
            EmailRequest emailRequest = buildContactNotificationEmail(contactForm);
            EmailResponse response = emailService.sendEmail(emailRequest);
            
            log.info("Email de contacto enviado exitosamente. MessageId: {}", response.getMessageId());
            return response;
            
        } catch (Exception e) {
            log.error("Error al procesar formulario de contacto: {}", e.getMessage(), e);
            return EmailResponse.builder()
                    .success(false)
                    .errorMessage("Error interno del servidor: " + e.getMessage())
                    .provider(emailService.getProviderName())
                    .build();
        }
    }
    
    private EmailRequest buildContactNotificationEmail(ContactForm contactForm) {
        String subject = "Nuevo formulario de contacto - Plan: " + contactForm.getInterestedPlan();
        
        String htmlContent = buildHtmlContent(contactForm);
        String textContent = buildTextContent(contactForm);
        
        return EmailRequest.builder()
                .from(fromEmail)
                .to(List.of(ownerEmail))
                .subject(subject)
                .htmlContent(htmlContent)
                .textContent(textContent)
                .replyTo(contactForm.getEmail())
                .build();
    }
    
    private String buildHtmlContent(ContactForm contactForm) {
        return """
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <title>Nuevo formulario de contacto</title>
                    <style>
                        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                        .header { background-color: #f8f9fa; padding: 20px; border-radius: 5px; }
                        .content { padding: 20px; }
                        .field { margin-bottom: 15px; }
                        .label { font-weight: bold; color: #555; }
                        .value { margin-top: 5px; }
                        .message { background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 20px; }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h2>📧 Nuevo formulario de contacto</h2>
                            <p>Se ha recibido una nueva solicitud de contacto desde tu aplicación multitenant.</p>
                        </div>
                        
                        <div class="content">
                            <div class="field">
                                <div class="label">👤 Nombre completo:</div>
                                <div class="value">%s</div>
                            </div>
                            
                            <div class="field">
                                <div class="label">📧 Correo electrónico:</div>
                                <div class="value"><a href="mailto:%s">%s</a></div>
                            </div>
                            
                            <div class="field">
                                <div class="label">📞 Teléfono:</div>
                                <div class="value">%s</div>
                            </div>
                            
                            <div class="field">
                                <div class="label">🏢 Empresa:</div>
                                <div class="value">%s</div>
                            </div>
                            
                            <div class="field">
                                <div class="label">📋 Plan de interés:</div>
                                <div class="value"><strong>%s</strong></div>
                            </div>
                            
                            %s
                        </div>
                    </div>
                </body>
                </html>
                """.formatted(
                        contactForm.getFullName(),
                        contactForm.getEmail(),
                        contactForm.getEmail(),
                        contactForm.getPhone(),
                        contactForm.getCompanyName(),
                        contactForm.getInterestedPlan(),
                        contactForm.getMessage() != null && !contactForm.getMessage().trim().isEmpty() 
                            ? """
                                <div class="message">
                                    <div class="label">💬 Mensaje:</div>
                                    <div class="value">%s</div>
                                </div>
                                """.formatted(contactForm.getMessage())
                            : ""
                );
    }
    
    private String buildTextContent(ContactForm contactForm) {
        StringBuilder content = new StringBuilder();
        content.append("NUEVO FORMULARIO DE CONTACTO\n");
        content.append("=============================\n\n");
        content.append("Se ha recibido una nueva solicitud de contacto desde tu aplicación multitenant.\n\n");
        content.append("INFORMACIÓN DEL CONTACTO:\n");
        content.append("------------------------\n");
        content.append("Nombre completo: ").append(contactForm.getFullName()).append("\n");
        content.append("Correo electrónico: ").append(contactForm.getEmail()).append("\n");
        content.append("Teléfono: ").append(contactForm.getPhone()).append("\n");
        content.append("Empresa: ").append(contactForm.getCompanyName()).append("\n");
        content.append("Plan de interés: ").append(contactForm.getInterestedPlan()).append("\n");
        
        if (contactForm.getMessage() != null && !contactForm.getMessage().trim().isEmpty()) {
            content.append("\nMENSAJE:\n");
            content.append("--------\n");
            content.append(contactForm.getMessage()).append("\n");
        }
        
        return content.toString();
    }
} 