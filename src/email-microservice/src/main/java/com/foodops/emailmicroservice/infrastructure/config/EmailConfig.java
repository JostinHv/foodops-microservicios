package com.foodops.emailmicroservice.infrastructure.config;

import com.foodops.emailmicroservice.domain.port.EmailService;
import com.foodops.emailmicroservice.infrastructure.adapter.SmtpEmailAdapter;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.mail.javamail.JavaMailSender;

/**
 * Configuración para el servicio de email
 */
@Slf4j
@Configuration
public class EmailConfig {
    
    @Value("${spring.mail.password:}")
    private String smtpPassword;
    
    @Value("${app.email.provider:smtp}")
    private String emailProvider;
    
    @Autowired
    private JavaMailSender javaMailSender;
    
    /**
     * Configura el servicio de email principal
     * Por defecto usa SMTP, pero puede ser configurado para otros proveedores
     */
    @Bean
    @Primary
    public EmailService emailService() {
        log.info("Configurando proveedor de email: {}", emailProvider);
        
        switch (emailProvider.toLowerCase()) {
            case "smtp":
                if (smtpPassword.isEmpty() || smtpPassword.equals("tu-token-smtp-aqui")) {
                    log.warn("Token SMTP de Mailtrap no configurado. Usando token por defecto.");
                }
                return new SmtpEmailAdapter(javaMailSender);
            
            // Aquí se pueden agregar más proveedores en el futuro
            // case "gmail":
            //     return new GmailEmailAdapter(gmailConfig);
            // case "sendgrid":
            //     return new SendGridEmailAdapter(sendGridConfig);
            
            default:
                log.warn("Proveedor de email '{}' no reconocido. Usando SMTP por defecto.", emailProvider);
                return new SmtpEmailAdapter(javaMailSender);
        }
    }
} 