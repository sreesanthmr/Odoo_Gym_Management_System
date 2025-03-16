📌 Project Overview

The Gym Management System is an Odoo-based ERP solution designed to efficiently manage gym memberships, trainer assignments, attendance tracking, and financial transactions. The system provides automated workflows, access control, and reporting to streamline gym operations.

Features

🔹 Model Inheritance & Customization

Extended res.partner for Gym Members and hr.employee for Trainers.

Inherited product.template to manage membership packages.

Integrated project.project and project.task for training schedules.

Extended account.move for invoice generation and payments.

🔹 Security & Access Control

Defined custom user groups: Gym Member & Gym Trainer.

Implemented record rules to enforce access restrictions.

Used domain filtering for data visibility per user role.

🔹 Reports & Data Export

Developed QWeb reports for invoices, attendance records, and training schedules.

Implemented XLSX export functionality for bulk data analysis.

🔹 Automation & Notifications

Configured automated email notifications for membership renewals & trainer assignments using scheduler (cron job).

Used sequences for generating unique membership IDs.
