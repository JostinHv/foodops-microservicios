package com.foodops.emailmicroservice.domain.model;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;

import jakarta.validation.ConstraintViolation;
import jakarta.validation.Validation;
import jakarta.validation.Validator;
import jakarta.validation.ValidatorFactory;

import java.util.Set;

import static org.junit.jupiter.api.Assertions.*;

@DisplayName("ContactForm Model Tests")
class ContactFormTest {
    
    private final ValidatorFactory factory = Validation.buildDefaultValidatorFactory();
    private final Validator validator = factory.getValidator();
    
    @Test
    @DisplayName("Should create valid ContactForm")
    void shouldCreateValidContactForm() {
        ContactForm contactForm = ContactForm.builder()
                .fullName("Juan Pérez")
                .email("juan.perez@empresa.com")
                .phone("+34 123 456 789")
                .companyName("Restaurante El Bueno")
                .interestedPlan("Plan Premium")
                .message("Me interesa conocer más sobre el plan")
                .build();
        
        Set<ConstraintViolation<ContactForm>> violations = validator.validate(contactForm);
        
        assertTrue(violations.isEmpty(), "No debería haber violaciones de validación");
    }
    
    @Test
    @DisplayName("Should fail validation with empty fullName")
    void shouldFailValidationWithEmptyFullName() {
        ContactForm contactForm = ContactForm.builder()
                .fullName("")
                .email("juan.perez@empresa.com")
                .phone("+34 123 456 789")
                .companyName("Restaurante El Bueno")
                .interestedPlan("Plan Premium")
                .build();
        
        Set<ConstraintViolation<ContactForm>> violations = validator.validate(contactForm);
        
        assertFalse(violations.isEmpty(), "Debería haber violaciones de validación");
        assertTrue(violations.stream().anyMatch(v -> v.getPropertyPath().toString().equals("fullName")));
    }
    
    @Test
    @DisplayName("Should fail validation with invalid email")
    void shouldFailValidationWithInvalidEmail() {
        ContactForm contactForm = ContactForm.builder()
                .fullName("Juan Pérez")
                .email("invalid-email")
                .phone("+34 123 456 789")
                .companyName("Restaurante El Bueno")
                .interestedPlan("Plan Premium")
                .build();
        
        Set<ConstraintViolation<ContactForm>> violations = validator.validate(contactForm);
        
        assertFalse(violations.isEmpty(), "Debería haber violaciones de validación");
        assertTrue(violations.stream().anyMatch(v -> v.getPropertyPath().toString().equals("email")));
    }
    
    @Test
    @DisplayName("Should fail validation with invalid phone")
    void shouldFailValidationWithInvalidPhone() {
        ContactForm contactForm = ContactForm.builder()
                .fullName("Juan Pérez")
                .email("juan.perez@empresa.com")
                .phone("invalid-phone")
                .companyName("Restaurante El Bueno")
                .interestedPlan("Plan Premium")
                .build();
        
        Set<ConstraintViolation<ContactForm>> violations = validator.validate(contactForm);
        
        assertFalse(violations.isEmpty(), "Debería haber violaciones de validación");
        assertTrue(violations.stream().anyMatch(v -> v.getPropertyPath().toString().equals("phone")));
    }
    
    @Test
    @DisplayName("Should pass validation with valid phone formats")
    void shouldPassValidationWithValidPhoneFormats() {
        String[] validPhones = {
            "+34 123 456 789",
            "123456789",
            "+1-555-123-4567",
            "(555) 123-4567"
        };
        
        for (String phone : validPhones) {
            ContactForm contactForm = ContactForm.builder()
                    .fullName("Juan Pérez")
                    .email("juan.perez@empresa.com")
                    .phone(phone)
                    .companyName("Restaurante El Bueno")
                    .interestedPlan("Plan Premium")
                    .build();
            
            Set<ConstraintViolation<ContactForm>> violations = validator.validate(contactForm);
            
            assertTrue(violations.isEmpty(), 
                "El teléfono " + phone + " debería ser válido");
        }
    }
    
    @Test
    @DisplayName("Should pass validation with optional message")
    void shouldPassValidationWithOptionalMessage() {
        ContactForm contactForm = ContactForm.builder()
                .fullName("Juan Pérez")
                .email("juan.perez@empresa.com")
                .phone("+34 123 456 789")
                .companyName("Restaurante El Bueno")
                .interestedPlan("Plan Premium")
                .message(null)
                .build();
        
        Set<ConstraintViolation<ContactForm>> violations = validator.validate(contactForm);
        
        assertTrue(violations.isEmpty(), "No debería haber violaciones de validación");
    }
} 