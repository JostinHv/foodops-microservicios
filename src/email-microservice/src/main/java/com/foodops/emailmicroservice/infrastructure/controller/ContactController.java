package com.foodops.emailmicroservice.infrastructure.controller;

import com.foodops.emailmicroservice.domain.model.ContactForm;
import com.foodops.emailmicroservice.domain.model.EmailResponse;
import com.foodops.emailmicroservice.domain.port.ContactFormService;
import com.foodops.emailmicroservice.domain.port.EmailService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import jakarta.validation.Valid;
import java.util.HashMap;
import java.util.Map;

/**
 * Controlador REST para manejar formularios de contacto
 */
@Slf4j
@RestController
@RequestMapping("/api/v1/contact")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")
public class ContactController {
    
    private final ContactFormService contactFormService;
    private final EmailService emailService;
    
    @Value("${spring.mail.host:}")
    private String smtpHost;
    
    @Value("${spring.mail.port:}")
    private String smtpPort;
    
    @Value("${spring.mail.username:}")
    private String smtpUsername;
    
    @Value("${spring.mail.password:}")
    private String smtpPassword;
    
    /**
     * Endpoint para procesar formularios de contacto
     * 
     * @param contactForm Formulario de contacto validado
     * @return Respuesta del procesamiento
     */
    @PostMapping("/submit")
    public ResponseEntity<EmailResponse> submitContactForm(@Valid @RequestBody ContactForm contactForm) {
        log.info("Recibida solicitud de formulario de contacto para: {}", contactForm.getEmail());
        
        EmailResponse response = contactFormService.processContactForm(contactForm);
        
        if (response.isSuccess()) {
            log.info("Formulario de contacto procesado exitosamente");
            return ResponseEntity.ok(response);
        } else {
            log.error("Error al procesar formulario de contacto: {}", response.getErrorMessage());
            return ResponseEntity.internalServerError().body(response);
        }
    }
    
    /**
     * Endpoint de salud del servicio
     * 
     * @return Estado del servicio
     */
    @GetMapping("/health")
    public ResponseEntity<String> health() {
        return ResponseEntity.ok("Email Microservice is running!");
    }
    
    /**
     * Endpoint para verificar la configuración SMTP
     * 
     * @return Información de configuración
     */
    @GetMapping("/config")
    public ResponseEntity<Map<String, Object>> getConfig() {
        Map<String, Object> config = new HashMap<>();
        config.put("provider", emailService.getProviderName());
        config.put("smtpHost", smtpHost);
        config.put("smtpPort", smtpPort);
        config.put("smtpUsername", smtpUsername);
        config.put("smtpPasswordConfigured", smtpPassword != null && !smtpPassword.trim().isEmpty());
        config.put("smtpPasswordMasked", maskToken(smtpPassword));
        config.put("status", "configured");
        
        return ResponseEntity.ok(config);
    }
    
    /**
     * Endpoint para probar el envío de email
     * 
     * @return Resultado de la prueba
     */
    @PostMapping("/test")
    public ResponseEntity<EmailResponse> testEmail() {
        log.info("Iniciando prueba de envío de email");
        
        try {
            // Crear un formulario de prueba
            ContactForm testForm = ContactForm.builder()
                    .fullName("Usuario de Prueba")
                    .email("test@example.com")
                    .phone("+34 123 456 789")
                    .companyName("Empresa de Prueba")
                    .interestedPlan("Plan de Prueba")
                    .message("Este es un mensaje de prueba para verificar la configuración SMTP de Mailtrap.")
                    .build();
            
            EmailResponse response = contactFormService.processContactForm(testForm);
            
            if (response.isSuccess()) {
                log.info("Prueba de email exitosa");
                return ResponseEntity.ok(response);
            } else {
                log.error("Prueba de email fallida: {}", response.getErrorMessage());
                return ResponseEntity.internalServerError().body(response);
            }
            
        } catch (Exception e) {
            log.error("Error durante la prueba de email: {}", e.getMessage(), e);
            return ResponseEntity.internalServerError().body(
                EmailResponse.builder()
                    .success(false)
                    .errorMessage("Error durante la prueba: " + e.getMessage())
                    .provider(emailService.getProviderName())
                    .build()
            );
        }
    }
    
    private String maskToken(String token) {
        if (token == null || token.length() < 8) {
            return "***";
        }
        return token.substring(0, 4) + "..." + token.substring(token.length() - 4);
    }
} 