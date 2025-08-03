package com.foodops.emailmicroservice.infrastructure.adapter;

import com.foodops.emailmicroservice.domain.model.EmailRequest;
import com.foodops.emailmicroservice.domain.model.EmailResponse;
import com.foodops.emailmicroservice.domain.port.EmailService;
import jakarta.mail.MessagingException;
import jakarta.mail.internet.MimeMessage;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.stereotype.Component;

/**
 * Adaptador SMTP que implementa el servicio de email
 * Usa la configuración SMTP de Mailtrap
 */
@Slf4j
@Component
public class SmtpEmailAdapter implements EmailService {

    private final JavaMailSender mailSender;

    @Autowired
    public SmtpEmailAdapter(JavaMailSender mailSender) {
        this.mailSender = mailSender;
        log.info("SmtpEmailAdapter inicializado exitosamente");
    }

    public EmailResponse sendSimpleEmail(EmailRequest emailRequest) {
        SimpleMailMessage message = new SimpleMailMessage();
        message.setFrom(emailRequest.getFrom());
        message.setTo(emailRequest.getTo().toArray(new String[0]));
        message.setSubject(emailRequest.getSubject());
        message.setText(emailRequest.getTextContent());
        mailSender.send(message);

        return EmailResponse.builder()
                .success(true)
                .messageId("smtp-" + System.currentTimeMillis())
                .provider("SMTP (Mailtrap)")
                .build();
    }

    @Override
    public EmailResponse sendEmail(EmailRequest request) {
        try {
            log.info("Enviando email usando SMTP a: {}", request.getTo());
            log.debug("Detalles del email - From: {}, Subject: {}, Provider: {}",
                    request.getFrom(), request.getSubject(), getProviderName());

            // Determinar si enviar como HTML o texto plano
            boolean hasHtmlContent = request.getHtmlContent() != null && !request.getHtmlContent().trim().isEmpty();

            return sendSimpleEmail(request);

        } catch (Exception e) {
            log.error("Error al enviar email con SMTP: {}", e.getMessage(), e);

            String errorMessage = "Error de SMTP: " + e.getMessage();

            // Manejar errores específicos de autenticación
            if (e.getMessage() != null && e.getMessage().contains("Authentication failed")) {
                errorMessage = "Error de autenticación SMTP. Verifica las credenciales de Mailtrap.";
                log.error("Credenciales SMTP inválidas");
            } else if (e.getMessage() != null && e.getMessage().contains("Connection refused")) {
                errorMessage = "Error de conexión SMTP. Verifica la configuración del servidor.";
            } else if (e.getMessage() != null && e.getMessage().contains("Invalid Address")) {
                errorMessage = "Dirección de email inválida.";
            }

            return EmailResponse.builder()
                    .success(false)
                    .errorMessage(errorMessage)
                    .provider("SMTP (Mailtrap)")
                    .build();
        }
    }

    @Override
    public String getProviderName() {
        return "SMTP (Mailtrap)";
    }

    private EmailResponse sendHtmlEmail(EmailRequest request) throws MessagingException {
        MimeMessage message = mailSender.createMimeMessage();
        MimeMessageHelper helper = new MimeMessageHelper(message, true, "UTF-8");

        // Configurar destinatarios
        helper.setTo(request.getTo().toArray(new String[0]));
        helper.setFrom(request.getFrom());
        helper.setSubject(request.getSubject());

        // Configurar contenido HTML
        helper.setText(request.getHtmlContent(), true);

        // Configurar contenido de texto plano como fallback
        if (request.getTextContent() != null && !request.getTextContent().trim().isEmpty()) {
            helper.setText(request.getTextContent(), false);
        }

        // Configurar reply-to si está disponible
        if (request.getReplyTo() != null && !request.getReplyTo().trim().isEmpty()) {
            helper.setReplyTo(request.getReplyTo());
        }

        mailSender.send(message);

        log.info("Email HTML enviado exitosamente con SMTP");

        return EmailResponse.builder()
                .success(true)
                .messageId("smtp-" + System.currentTimeMillis())
                .provider("SMTP (Mailtrap)")
                .build();
    }

    private EmailResponse sendTextEmail(EmailRequest request) {
        SimpleMailMessage message = new SimpleMailMessage();

        // Configurar destinatarios
        message.setTo(request.getTo().toArray(new String[0]));
        message.setFrom(request.getFrom());
        message.setSubject(request.getSubject());
        message.setText(request.getTextContent());

        // Configurar reply-to si está disponible
        if (request.getReplyTo() != null && !request.getReplyTo().trim().isEmpty()) {
            message.setReplyTo(request.getReplyTo());
        }

        mailSender.send(message);

        log.info("Email de texto enviado exitosamente con SMTP");

        return EmailResponse.builder()
                .success(true)
                .messageId("smtp-" + System.currentTimeMillis())
                .provider("SMTP (Mailtrap)")
                .build();
    }
} 