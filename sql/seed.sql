
INSERT INTO customers(customer_id,full_name,email,phone,license_number,joined_on) VALUES
(1,'Aarav Sharma','aarav.sharma@example.in','+91 98765 43210','DL-0420110012345','2025-02-12'),
(2,'Priya Mehta','priya.mehta@example.in','+91 98201 56789','MH-0320130098765','2025-04-03'),
(3,'Rohan Kapoor','rohan.kapoor@example.in','+91 98450 12345','KA-0520140011223','2025-05-18'),
(4,'Ananya Iyer','ananya.iyer@example.in','+91 98401 23456','TN-0920150044556','2025-07-21'),
(5,'Arjun Nair','arjun.nair@example.in','+91 98950 67890','KL-0720160077889','2025-09-08'),
(6,'Kavya Reddy','kavya.reddy@example.in','+91 98490 24680','TS-1020170033445','2025-10-11'),
(7,'Ishaan Gupta','ishaan.gupta@example.in','+91 98100 13579','UP-1620180066778','2025-11-02'),
(8,'Diya Shah','diya.shah@example.in','+91 98250 86420','GJ-0120190099001','2025-11-14')
ON CONFLICT (customer_id) DO NOTHING;

INSERT INTO vehicles(vehicle_id,make,model,year,license_plate,category,daily_rate,mileage,status,image_color) VALUES
(1,'Tata','Nexon EV',2024,'DL 8C AQ 2481','Electric',4200,20000,'Rented','#dcebe7'),
(2,'Maruti Suzuki','Ciaz',2023,'MH 02 EB 9302','Sedan',2800,29500,'Available','#f4e6d7'),
(3,'Hyundai','Creta',2024,'KA 03 MN 5128','SUV',3800,15400,'Available','#e6edda'),
(4,'Mahindra','XUV700',2023,'TN 09 BX 7401','SUV',5200,35600,'Rented','#e9e1f3'),
(5,'Maruti Suzuki','Baleno',2022,'UP 16 CC 4088','Economy',2200,42000,'Available','#dfeaf2'),
(6,'Tata','Punch EV',2024,'GJ 01 AB 6591','Electric',3200,8100,'Maintenance','#efe5cc'),
(7,'Toyota','Innova Crysta',2023,'MH 14 DY 2630','Van',5600,26500,'Available','#e2e8ea'),
(8,'Honda','City',2024,'DL 01 CZ 8834','Sedan',3200,18000,'Available','#f1e0dc'),
(9,'Kia','Carens',2023,'KA 05 LS 6305','Van',4400,22800,'Available','#e2ecdf')
ON CONFLICT (vehicle_id) DO NOTHING;

INSERT INTO bookings(booking_id,customer_id,vehicle_id,pickup_date,return_date,status,estimated_total,created_at) VALUES
(1,3,3,'2026-11-18','2026-11-22','Confirmed',15200,'2026-11-11 09:20:00+00'),
(2,5,7,'2026-11-19','2026-11-23','Confirmed',22400,'2026-11-12 14:10:00+00'),
(3,7,2,'2026-11-20','2026-11-24','Pending',11200,'2026-11-13 11:30:00+00'),
(4,8,9,'2026-11-22','2026-11-25','Confirmed',13200,'2026-11-14 08:45:00+00')
ON CONFLICT (booking_id) DO NOTHING;

INSERT INTO rentals(rental_id,customer_id,vehicle_id,booking_id,start_date,end_date,actual_return_date,status,total_amount,created_at) VALUES
(1,1,1,NULL,'2026-11-12','2026-11-17',NULL,'Active',21000,'2026-11-12 10:15:00+00'),
(2,2,4,NULL,'2026-11-13','2026-11-18',NULL,'Active',31200,'2026-11-13 12:05:00+00'),
(3,6,5,NULL,'2026-11-08','2026-11-10','2026-11-10','Completed',6600,'2026-11-08 08:00:00+00'),
(4,4,8,NULL,'2026-11-05','2026-11-07','2026-11-07','Completed',9600,'2026-11-05 15:20:00+00')
ON CONFLICT (rental_id) DO NOTHING;

INSERT INTO payments(payment_id,rental_id,amount,payment_date,method,status,reference) VALUES
(1,1,21000,'2026-11-12','Card','Paid','AF-2026-001'),
(2,2,20000,'2026-11-13','UPI','Paid','AF-2026-002'),
(3,3,6600,'2026-11-10','Cash','Paid','AF-2026-003'),
(4,4,9600,'2026-11-07','UPI','Paid','AF-2026-004')
ON CONFLICT (payment_id) DO NOTHING;

INSERT INTO maintenance(maintenance_id,vehicle_id,service_type,description,service_date,cost,status) VALUES
(1,6,'Battery inspection','Routine EV battery health check','2026-11-16',18500,'In progress'),
(2,3,'Periodic service','Scheduled 15,000 km service','2026-11-20',6500,'Scheduled'),
(3,5,'Tyre rotation','Quarterly tyre rotation','2026-11-05',4800,'Completed')
ON CONFLICT (maintenance_id) DO NOTHING;

-- Advance identity sequences past the explicit demo IDs.
SELECT setval(pg_get_serial_sequence('customers','customer_id'), COALESCE((SELECT MAX(customer_id) FROM customers),1), true);
SELECT setval(pg_get_serial_sequence('vehicles','vehicle_id'), COALESCE((SELECT MAX(vehicle_id) FROM vehicles),1), true);
SELECT setval(pg_get_serial_sequence('bookings','booking_id'), COALESCE((SELECT MAX(booking_id) FROM bookings),1), true);
SELECT setval(pg_get_serial_sequence('rentals','rental_id'), COALESCE((SELECT MAX(rental_id) FROM rentals),1), true);
SELECT setval(pg_get_serial_sequence('payments','payment_id'), COALESCE((SELECT MAX(payment_id) FROM payments),1), true);
SELECT setval(pg_get_serial_sequence('maintenance','maintenance_id'), COALESCE((SELECT MAX(maintenance_id) FROM maintenance),1), true);
