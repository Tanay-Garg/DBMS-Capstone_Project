INSERT INTO customers(customer_id,full_name,email,phone,license_number,joined_on) VALUES
(10,'Meera Joshi','meera.joshi@example.com','+91 90000 10010','MH-1420200010010','2025-12-02'),
(11,'Kabir Malhotra','kabir.malhotra@example.com','+91 90000 10011','DL-0320190010011','2025-12-16'),
(12,'Nisha Verma','nisha.verma@example.com','+91 90000 10012','UP-3220210010012','2026-01-09'),
(13,'Aditya Kulkarni','aditya.kulkarni@example.com','+91 90000 10013','KA-0320180010013','2026-01-24'),
(14,'Saanvi Bose','saanvi.bose@example.com','+91 90000 10014','WB-0620220010014','2026-02-11'),
(15,'Vihaan Desai','vihaan.desai@example.com','+91 90000 10015','GJ-0520200010015','2026-03-04'),
(16,'Tara Menon','tara.menon@example.com','+91 90000 10016','KL-0720190010016','2026-03-27'),
(17,'Devansh Bhat','devansh.bhat@example.com','+91 90000 10017','MH-1220230010017','2026-04-12');

INSERT INTO vehicles(vehicle_id,make,model,year,license_plate,category,daily_rate,mileage,status,image_color) VALUES
(11,'Tata','Altroz',2024,'DL 05 RT 4182','Economy',2600,18400,'Available','#f2e4d6'),
(12,'Maruti Suzuki','Fronx',2025,'MH 12 KV 7031','SUV',3300,9700,'Available','#e8e9d8'),
(13,'Hyundai','Venue',2024,'KA 51 MG 2864','SUV',3600,21600,'Available','#dce9e5'),
(14,'Kia','Sonet',2025,'TN 10 QP 9457','SUV',3400,12800,'Available','#e9e1f2'),
(15,'Mahindra','Thar',2023,'UP 32 YT 5610','SUV',6200,30200,'Available','#e4e8d9'),
(16,'MG','ZS EV',2024,'GJ 05 CF 8274','Electric',6500,15600,'Available','#dce7f1'),
(17,'Tata','Tiago EV',2024,'RJ 14 DH 3906','Electric',3800,22100,'Available','#f2e1df'),
(18,'Renault','Kiger',2023,'HR 26 ZN 7143','SUV',3000,34800,'Available','#e6e3f3'),
(19,'Skoda','Slavia',2024,'TS 08 LB 2059','Sedan',4800,17400,'Available','#e2ece3'),
(20,'Honda','Elevate',2025,'WB 06 AP 6381','SUV',4200,8900,'Available','#f1e8d7'),
(21,'Toyota','Rumion',2024,'KL 07 MN 4725','Van',5100,19300,'Available','#dfe9eb'),
(22,'Maruti Suzuki','Grand Vitara',2025,'PB 10 RK 1938','SUV',4600,11200,'Available','#ebe0ee');

INSERT INTO bookings(booking_id,customer_id,vehicle_id,pickup_date,return_date,status,estimated_total) VALUES
(5,10,11,'2026-12-01','2026-12-04','Confirmed',10400),
(6,11,12,'2026-12-02','2026-12-06','Pending',16500),
(7,12,13,'2026-12-05','2026-12-08','Confirmed',14400),
(8,13,14,'2026-12-06','2026-12-09','Confirmed',13600),
(9,14,15,'2026-12-12','2026-12-16','Confirmed',31000),
(10,15,16,'2026-12-13','2026-12-16','Confirmed',26000),
(11,16,17,'2026-12-18','2026-12-22','Pending',19000),
(12,17,18,'2026-12-20','2026-12-24','Confirmed',15000);

INSERT INTO rentals(rental_id,customer_id,vehicle_id,start_date,end_date,actual_return_date,status,total_amount) VALUES
(5,10,11,'2026-11-20','2026-11-28',NULL,'Active',20800),
(6,11,12,'2026-11-23','2026-11-30',NULL,'Active',26400),
(7,12,13,'2026-11-24','2026-12-01',NULL,'Active',28800),
(8,13,14,'2026-11-24','2026-11-29',NULL,'Active',20400),
(9,14,15,'2026-11-25','2026-12-02',NULL,'Active',49600),
(10,15,16,'2026-11-20','2026-11-27',NULL,'Active',52000),
(11,16,17,'2026-11-10','2026-11-13','2026-11-13','Completed',15200),
(12,17,18,'2026-11-15','2026-11-18','2026-11-18','Completed',12000);

INSERT INTO payments(payment_id,rental_id,amount,payment_date,method,status,reference) VALUES
(5,5,20800,'2026-11-20','UPI','Paid','AF-2026-005'),
(6,6,13000,'2026-11-23','Card','Paid','AF-2026-006'),
(7,7,12000,'2026-11-24','UPI','Pending','AF-2026-007'),
(8,8,20400,'2026-11-24','Bank transfer','Paid','AF-2026-008'),
(9,9,30000,'2026-11-25','UPI','Paid','AF-2026-009'),
(10,10,52000,'2026-11-20','Card','Paid','AF-2026-010'),
(11,11,15200,'2026-11-13','UPI','Paid','AF-2026-011'),
(12,12,12000,'2026-11-18','Cash','Paid','AF-2026-012');

INSERT INTO maintenance(maintenance_id,vehicle_id,service_type,description,service_date,cost,status) VALUES
(3,17,'Battery health check','Routine electric vehicle battery inspection','2026-11-12',9200,'Completed'),
(4,18,'Brake inspection','Brake pad and fluid inspection','2026-11-13',3600,'Completed'),
(5,19,'Periodic service','Scheduled 20,000 km service','2026-12-02',7800,'Scheduled'),
(6,20,'Tyre replacement','Replace two worn tyres','2026-11-25',5400,'In progress'),
(7,21,'AC service','Cabin filter and air-conditioning service','2026-12-01',6200,'Scheduled'),
(8,22,'Wheel alignment','Alignment and balancing completed','2026-11-18',4100,'Completed');

SELECT setval(pg_get_serial_sequence('customers','customer_id'), (SELECT MAX(customer_id) FROM customers), true);
SELECT setval(pg_get_serial_sequence('vehicles','vehicle_id'), (SELECT MAX(vehicle_id) FROM vehicles), true);
SELECT setval(pg_get_serial_sequence('bookings','booking_id'), (SELECT MAX(booking_id) FROM bookings), true);
SELECT setval(pg_get_serial_sequence('rentals','rental_id'), (SELECT MAX(rental_id) FROM rentals), true);
SELECT setval(pg_get_serial_sequence('payments','payment_id'), (SELECT MAX(payment_id) FROM payments), true);
SELECT setval(pg_get_serial_sequence('maintenance','maintenance_id'), (SELECT MAX(maintenance_id) FROM maintenance), true);
