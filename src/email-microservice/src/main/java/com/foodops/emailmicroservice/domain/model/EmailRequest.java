package com.foodops.emailmicroservice.domain.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

/**
 * Modelo de dominio para las solicitudes de email
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class EmailRequest {
    private String from;
    private List<String> to;
    private String subject;
    private String textContent;
    private String htmlContent;
    private String replyTo;
} 