package com.foodops.emailmicroservice.domain.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;

/**
 * Modelo de dominio para el formulario de contacto
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ContactForm {
    
    @NotBlank(message = "El nombre completo es obligatorio")
    @Size(min = 2, max = 100, message = "El nombre debe tener entre 2 y 100 caracteres")
    private String fullName;
    
    @NotBlank(message = "El correo electrónico es obligatorio")
    @Email(message = "El formato del correo electrónico no es válido")
    private String email;
    
    @NotBlank(message = "El teléfono es obligatorio")
    @Pattern(regexp = "^[+]?[0-9\\s\\-\\(\\)]{7,20}$", 
             message = "El formato del teléfono no es válido")
    private String phone;
    
    @NotBlank(message = "El nombre de la empresa es obligatorio")
    @Size(min = 2, max = 100, message = "El nombre de la empresa debe tener entre 2 y 100 caracteres")
    private String companyName;
    
    @NotBlank(message = "El plan de interés es obligatorio")
    @Size(min = 2, max = 50, message = "El plan de interés debe tener entre 2 y 50 caracteres")
    private String interestedPlan;
    
    @Size(max = 1000, message = "El mensaje no puede exceder los 1000 caracteres")
    private String message;
} 