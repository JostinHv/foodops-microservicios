package com.foodops.emailmicroservice.domain.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Modelo de dominio para las respuestas de email
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class EmailResponse {
    private boolean success;
    private String messageId;
    private String errorMessage;
    private String provider;
} 