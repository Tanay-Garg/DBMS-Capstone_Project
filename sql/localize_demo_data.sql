-- One-time update of the initial demo rows for the Indian market.
BEGIN;

UPDATE customers SET full_name='Aarav Sharma', email='aarav.sharma@example.in', phone='+91 98765 43210', license_number='DL-0420110012345' WHERE customer_id=1;
UPDATE customers SET full_name='Priya Mehta', email='priya.mehta@example.in', phone='+91 98201 56789', license_number='MH-0320130098765' WHERE customer_id=2;
UPDATE customers SET full_name='Rohan Kapoor', email='rohan.kapoor@example.in', phone='+91 98450 12345', license_number='KA-0520140011223' WHERE customer_id=3;
UPDATE customers SET full_name='Ananya Iyer', email='ananya.iyer@example.in', phone='+91 98401 23456', license_number='TN-0920150044556' WHERE customer_id=4;
UPDATE customers SET full_name='Arjun Nair', email='arjun.nair@example.in', phone='+91 98950 67890', license_number='KL-0720160077889' WHERE customer_id=5;
UPDATE customers SET full_name='Kavya Reddy', email='kavya.reddy@example.in', phone='+91 98490 24680', license_number='TS-1020170033445' WHERE customer_id=6;
UPDATE customers SET full_name='Ishaan Gupta', email='ishaan.gupta@example.in', phone='+91 98100 13579', license_number='UP-1620180066778' WHERE customer_id=7;
UPDATE customers SET full_name='Diya Shah', email='diya.shah@example.in', phone='+91 98250 86420', license_number='GJ-0120190099001' WHERE customer_id=8;

UPDATE vehicles SET make='Tata', model='Nexon EV', license_plate='DL 8C AQ 2481', category='Electric', daily_rate=4200, mileage=20000, image_color='#dcebe7' WHERE vehicle_id=1;
UPDATE vehicles SET make='Maruti Suzuki', model='Ciaz', license_plate='MH 02 EB 9302', category='Sedan', daily_rate=2800, mileage=29500, image_color='#f4e6d7' WHERE vehicle_id=2;
UPDATE vehicles SET make='Hyundai', model='Creta', license_plate='KA 03 MN 5128', category='SUV', daily_rate=3800, mileage=15400, image_color='#e6edda' WHERE vehicle_id=3;
UPDATE vehicles SET make='Mahindra', model='XUV700', license_plate='TN 09 BX 7401', category='SUV', daily_rate=5200, mileage=35600, image_color='#e9e1f3' WHERE vehicle_id=4;
UPDATE vehicles SET make='Maruti Suzuki', model='Baleno', license_plate='UP 16 CC 4088', category='Economy', daily_rate=2200, mileage=42000, image_color='#dfeaf2' WHERE vehicle_id=5;
UPDATE vehicles SET make='Tata', model='Punch EV', license_plate='GJ 01 AB 6591', category='Electric', daily_rate=3200, mileage=8100, image_color='#efe5cc' WHERE vehicle_id=6;
UPDATE vehicles SET make='Toyota', model='Innova Crysta', license_plate='MH 14 DY 2630', category='Van', daily_rate=5600, mileage=26500, image_color='#e2e8ea' WHERE vehicle_id=7;
UPDATE vehicles SET make='Honda', model='City', license_plate='DL 01 CZ 8834', category='Sedan', daily_rate=3200, mileage=18000, image_color='#f1e0dc' WHERE vehicle_id=8;
UPDATE vehicles SET make='Kia', model='Carens', license_plate='KA 05 LS 6305', category='Van', daily_rate=4400, mileage=22800, image_color='#e2ecdf' WHERE vehicle_id=9;

UPDATE bookings SET estimated_total=15200 WHERE booking_id=1;
UPDATE bookings SET estimated_total=22400 WHERE booking_id=2;
UPDATE bookings SET estimated_total=11200 WHERE booking_id=3;
UPDATE bookings SET estimated_total=13200 WHERE booking_id=4;
UPDATE rentals SET total_amount=21000 WHERE rental_id=1;
UPDATE rentals SET total_amount=31200 WHERE rental_id=2;
UPDATE rentals SET total_amount=6600 WHERE rental_id=3;
UPDATE rentals SET total_amount=9600 WHERE rental_id=4;
UPDATE payments SET amount=21000, method='Card' WHERE payment_id=1;
UPDATE payments SET amount=20000, method='UPI' WHERE payment_id=2;
UPDATE payments SET amount=6600, method='Cash' WHERE payment_id=3;
UPDATE payments SET amount=9600, method='UPI' WHERE payment_id=4;
UPDATE maintenance SET service_type='Battery inspection', description='Routine EV battery health check', cost=18500 WHERE maintenance_id=1;
UPDATE maintenance SET service_type='Periodic service', description='Scheduled 15,000 km service', cost=6500 WHERE maintenance_id=2;
UPDATE maintenance SET service_type='Tyre rotation', description='Quarterly tyre rotation', cost=4800 WHERE maintenance_id=3;

COMMIT;
