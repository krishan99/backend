PRAGMA foreign_keys = ON;

INSERT INTO businesses(uid, name, description, email) VALUES (
    '1abc',
    'Bobs Pizza',
    '1111 pizza street ann arbor michigan 48105',
    'pizza@gmail.com'
    ),(
    '2abc',
    'Ann Arbor Arts & Crafts',
    'We have paint and crayons',
    'craffs@gmail.com'
    ),(
    '3abc',
    'Starbucks',
    '1111 bob street ann arbor michigan 48105',
    'bob@starbucks'
    ),(
    '4abc',
    'Bobs Burgers',
    'burgers burger burgers',
    'burgers@hotmail.com'
);
/*
INSERT INTO businesses(name, email, password, address_street, address_city, address_state, zipcode) VALUES (
    'Bobs Pizza',
    'pizza@gmail.com',
    'pizza',
    '1111 pizza street',
    'ann arbor',
    'michigan',
    '48105'
    ),(
    'Ann Arbor Arts & Crafts',
    'craffs@gmail.com',
    'craffs',
    '1111 craffs street',
    'ann arbor',
    'michigan',
    '48105'
    ),(
    'Starbucks',
    'bob@starbucks',
    'bob',
    '1111 bob street',
    'ann arbor',
    'michigan',
    '48105'),(
    'Bobs Burgers',
    'burgers@hotmail.com',
    'burgers',
    '1111 burgers street',
    'ann arbor',
    'michigan',
    '48105'
);
*/
/*
INSERT INTO opening_hours(bid, weekday, open_time, end_time) VALUES (
    '1',
    '1',
    '2020-06-01 07:00:00',
    '2020-06-01 19:00:00'
    ),(
    '1',
    '2',
    '2020-06-01 07:00:00',
    '2020-06-01 19:00:00'
    ),(
    '1',
    '3',
    '2020-06-01 07:00:00',
    '2020-06-01 19:00:00'
    ),(
    '1',
    '4',
    '2020-06-01 07:00:00',
    '2020-06-01 19:00:00'
    ),(
    '1',
    '5',
    '2020-06-01 07:00:00',
    '2020-06-01 19:00:00'
    ),(
    '1',
    '6',
    '2020-06-01 12:00:00',
    '2020-06-01 18:00:00'
    ),(
    '1',
    '7',
    '2020-06-01 12:00:00',
    '2020-06-01 18:00:00'
);

INSERT INTO contact(bid, pid, phone_number) VALUES (
    '1',
    '1',
    '1001001000'
);*/

INSERT INTO queues(bid, qname, code, description) VALUES (
    '3',
    'Morning Brew',
    '3418',
    'Come get your coffee!!'
    ),(
    '2',
    'Outdoor Line',
    '1903',
    'We sell arts and crafts'
    ),(
    '1',
    'Outdoor Line',
    '0973',
    'Please wait your turn, no exceptions'
    ),(
    '1',
    'Pickups',
    '5361',
    'We will notify you as soon as your order is ready and you can come in'
);

INSERT INTO queue_qid3(name, phone, note) VALUES (
    'George Washington',
    '1-800-100-7843',
    ''
    ),(
    'John Cena',
    '8001234567',
    'Im the best'
    ),(
    'Tom Jerry',
    '124242',
    'Pick up order'
);
