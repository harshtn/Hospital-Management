-- ========================================================
-- Hospital Management System (HMS 2025) - MySQL Relational Schema
-- Database: hospital_db
-- ========================================================

CREATE DATABASE IF NOT EXISTS `hospital_db` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `hospital_db`;

-- 1. Clinical Departments
CREATE TABLE IF NOT EXISTS `core_department` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(120) NOT NULL UNIQUE,
    `code` VARCHAR(20) NOT NULL UNIQUE,
    `description` LONGTEXT NULL,
    `head_of_department` VARCHAR(150) NULL,
    `phone` VARCHAR(30) NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Hospital Rooms and Wards
CREATE TABLE IF NOT EXISTS `core_room` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `room_number` VARCHAR(30) NOT NULL UNIQUE,
    `room_type` VARCHAR(20) NOT NULL DEFAULT 'GENERAL',
    `capacity` INT UNSIGNED NOT NULL DEFAULT 1,
    `current_occupancy` INT UNSIGNED NOT NULL DEFAULT 0,
    `status` VARCHAR(20) NOT NULL DEFAULT 'AVAILABLE',
    `cost_per_day` DECIMAL(10, 2) NOT NULL DEFAULT 50.00,
    `department_id` BIGINT NULL,
    CONSTRAINT `fk_room_department` FOREIGN KEY (`department_id`) REFERENCES `core_department` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Doctors & Specialists
CREATE TABLE IF NOT EXISTS `doctors_doctor` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `doctor_id` VARCHAR(20) NOT NULL UNIQUE,
    `first_name` VARCHAR(80) NOT NULL,
    `last_name` VARCHAR(80) NOT NULL,
    `specialization` VARCHAR(120) NOT NULL,
    `qualification` VARCHAR(150) NOT NULL,
    `experience_years` INT UNSIGNED NOT NULL DEFAULT 1,
    `phone` VARCHAR(20) NOT NULL,
    `email` VARCHAR(254) NOT NULL UNIQUE,
    `room_number` VARCHAR(30) NULL,
    `consultation_fee` DECIMAL(10, 2) NOT NULL DEFAULT 100.00,
    `available_days` VARCHAR(150) NOT NULL,
    `time_slot_start` TIME NOT NULL DEFAULT '09:00:00',
    `time_slot_end` TIME NOT NULL DEFAULT '17:00:00',
    `is_active` TINYINT(1) NOT NULL DEFAULT 1,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `department_id` BIGINT NOT NULL,
    CONSTRAINT `fk_doctor_department` FOREIGN KEY (`department_id`) REFERENCES `core_department` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. Patients Registry
CREATE TABLE IF NOT EXISTS `patients_patient` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `patient_id` VARCHAR(20) NOT NULL UNIQUE,
    `first_name` VARCHAR(80) NOT NULL,
    `last_name` VARCHAR(80) NOT NULL,
    `gender` VARCHAR(2) NOT NULL,
    `date_of_birth` DATE NOT NULL,
    `blood_group` VARCHAR(10) NOT NULL DEFAULT 'UNKNOWN',
    `phone` VARCHAR(20) NOT NULL,
    `email` VARCHAR(254) NULL,
    `address` LONGTEXT NOT NULL,
    `emergency_contact_name` VARCHAR(120) NOT NULL,
    `emergency_contact_phone` VARCHAR(20) NOT NULL,
    `emergency_contact_relation` VARCHAR(50) NOT NULL DEFAULT 'Guardian',
    `allergies` LONGTEXT NULL,
    `chronic_conditions` LONGTEXT NULL,
    `medical_history` LONGTEXT NULL,
    `insurance_provider` VARCHAR(120) NULL,
    `insurance_policy_number` VARCHAR(60) NULL,
    `status` VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. Appointments & Scheduling
CREATE TABLE IF NOT EXISTS `appointments_appointment` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `appointment_id` VARCHAR(20) NOT NULL UNIQUE,
    `appointment_date` DATE NOT NULL,
    `appointment_time` TIME NOT NULL,
    `status` VARCHAR(20) NOT NULL DEFAULT 'SCHEDULED',
    `reason_for_visit` VARCHAR(255) NOT NULL,
    `doctor_notes` LONGTEXT NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `doctor_id` BIGINT NOT NULL,
    `patient_id` BIGINT NOT NULL,
    CONSTRAINT `fk_appointment_doctor` FOREIGN KEY (`doctor_id`) REFERENCES `doctors_doctor` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_appointment_patient` FOREIGN KEY (`patient_id`) REFERENCES `patients_patient` (`id`) ON DELETE CASCADE,
    CONSTRAINT `unique_doctor_slot` UNIQUE (`doctor_id`, `appointment_date`, `appointment_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. Medical Records (EHR)
CREATE TABLE IF NOT EXISTS `medical_records_medicalrecord` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `record_id` VARCHAR(20) NOT NULL UNIQUE,
    `record_date` DATE NOT NULL,
    `symptoms` LONGTEXT NOT NULL,
    `diagnosis` VARCHAR(255) NOT NULL,
    `treatment_plan` LONGTEXT NOT NULL,
    `blood_pressure` VARCHAR(20) NULL,
    `heart_rate` INT UNSIGNED NULL,
    `temperature` DECIMAL(4, 1) NULL,
    `weight_kg` DECIMAL(5, 2) NULL,
    `notes` LONGTEXT NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `appointment_id` BIGINT NULL,
    `doctor_id` BIGINT NOT NULL,
    `patient_id` BIGINT NOT NULL,
    CONSTRAINT `fk_record_appointment` FOREIGN KEY (`appointment_id`) REFERENCES `appointments_appointment` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_record_doctor` FOREIGN KEY (`doctor_id`) REFERENCES `doctors_doctor` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_record_patient` FOREIGN KEY (`patient_id`) REFERENCES `patients_patient` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 7. Prescription Line Items
CREATE TABLE IF NOT EXISTS `medical_records_prescriptionitem` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `medication_name` VARCHAR(150) NOT NULL,
    `dosage` VARCHAR(80) NOT NULL,
    `frequency` VARCHAR(80) NOT NULL,
    `duration_days` INT UNSIGNED NOT NULL DEFAULT 7,
    `instructions` VARCHAR(255) NULL,
    `medical_record_id` BIGINT NOT NULL,
    CONSTRAINT `fk_prescription_record` FOREIGN KEY (`medical_record_id`) REFERENCES `medical_records_medicalrecord` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 8. Billing & Invoices
CREATE TABLE IF NOT EXISTS `billing_invoice` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `invoice_id` VARCHAR(20) NOT NULL UNIQUE,
    `issue_date` DATE NOT NULL,
    `due_date` DATE NULL,
    `subtotal` DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    `discount` DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    `tax` DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    `total_amount` DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    `paid_amount` DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    `payment_status` VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    `payment_method` VARCHAR(20) NOT NULL DEFAULT 'CASH',
    `notes` LONGTEXT NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `appointment_id` BIGINT NULL,
    `patient_id` BIGINT NOT NULL,
    CONSTRAINT `fk_invoice_appointment` FOREIGN KEY (`appointment_id`) REFERENCES `appointments_appointment` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_invoice_patient` FOREIGN KEY (`patient_id`) REFERENCES `patients_patient` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 9. Invoice Line Items
CREATE TABLE IF NOT EXISTS `billing_invoiceitem` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `description` VARCHAR(200) NOT NULL,
    `unit_price` DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    `quantity` INT UNSIGNED NOT NULL DEFAULT 1,
    `total` DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    `invoice_id` BIGINT NOT NULL,
    CONSTRAINT `fk_invoiceitem_invoice` FOREIGN KEY (`invoice_id`) REFERENCES `billing_invoice` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

