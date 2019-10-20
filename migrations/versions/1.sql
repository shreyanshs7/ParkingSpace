--Users table
create table app_user (
  id serial primary key,
  password varchar(255) not null ,
  full_name varchar(255) not null ,
  number varchar(255) not null
);

--Location table
create table location(
  id serial primary key ,
  latitude float not null ,
  longitude float not null
);

--Vehicle table
create table vehicle(
  id serial primary key ,
  type varchar(255),
  charge float not null,
  quantity integer not null ,
  status varchar(255),
  user_id integer references app_user(id)
);

--Booking Space Table
create table booking_space(
    id serial primary key,
    name varchar(255) not null,
    from_time timestamp not null,
    to_time timestamp not null ,
    location_id integer references location(id),
    image varchar(255) not null ,
    user_id integer references app_user(id),
    additional_information varchar(255),
    status varchar(255),
    vehicle_id integer references vehicle(id)
);

--Booking Order table
create table booking_order(
  id serial primary key ,
  type varchar(255),
  booking_space_id integer references booking_space(id),
  booked_by integer references app_user(id),
  from_time timestamp,
  to_time timestamp,
  quantity integer
);

--Rating table
create table rating(
    id serial primary key ,
    booking_space_id integer references booking_space(id),
    by_user integer references app_user(id),
    rating integer not null
);