create database Library;
use Library;

/*Member*/
create table membership(
m_id varchar(4) not null,
m_type varchar(20)not null,
constraint m_pk primary key(m_id),
constraint mid_ck check(m_id LIKE '[m/M][0-9][0-9][0-9]')
);

/*customer*/
create table customer(
c_id varchar(6) not null,
f_name varchar(50),
l_name varchar(50),
dob date,
address varchar(300),
contact int not null,
nic int not null,
m_id varchar(4) not null,
constraint c_pk primary key(c_id),
constraint c_fk foreign key(m_id) references membership(m_id),
constraint cid_ck check(c_id LIKE '[c/C][0-9][0-9][0-9][0-9][0-9]'),
constraint cmid_ck check(m_id LIKE '[m/M][0-9][0-9][0-9]')
);

/*role*/
create table role(
r_id varchar(4) not null,
r_name varchar(30),
constraint r_pk primary key(r_id),
constraint rid_ck check(r_id LIKE '[r/R][0-9][0-9][0-9]')
);

/*staff*/
create table staff(
s_id varchar(6) not null,
f_name varchar(50),
l_name varchar(50),
dob date,
address varchar(300),
contact int not null,
nic int not null,
r_id varchar(4) not null,
constraint s_pk primary key(s_id),
constraint s_fk foreign key(r_id) references role(r_id) ,
constraint sid_ck check(s_id LIKE '[s/S][0-9][0-9][0-9][0-9][0-9]'),
constraint srid_ck check(r_id LIKE '[r/R][0-9][0-9][0-9]')
);

/*staff email*/
create table staff_email(
s_id varchar(6) not null,
email varchar(100) not null,
constraint se_fk foreign key(s_id) references staff(s_id),
constraint seid_ck check(s_id LIKE '[s/S][0-9][0-9][0-9][0-9][0-9]')
);

/*admin*/
create table admin(
a_id varchar(6) not null,
f_name varchar(50),
l_name varchar(50),
dob date,
address varchar(300),
contact int not null,
nic varchar(12) not null,
r_id varchar(4) not null,
constraint a_pk primary key(a_id),
constraint a_fk foreign key(r_id) references role(r_id),
constraint aid_ck check(a_id LIKE '[a/A][0-9][0-9][0-9][0-9][0-9]'),
constraint arid_ck check(r_id LIKE '[r/R][0-9][0-9][0-9]')
);

/*customer email*/
create table customer_email(
c_id varchar(6) not null,
email varchar(100) not null,
constraint ce_fk foreign key(c_id) references customer(c_id),
constraint ce_ck check(c_id LIKE'[c/C][0-9][0-9][0-9][0-9][]0-9]')
);
/*admin email*/
create table admin_email(
a_id varchar(6) not null,
email varchar(100) not null,
constraint ae_fk foreign key(a_id) references admin(a_id),
constraint aeid_ck check(a_id LIKE'[a/A][0-9][0-9][0-9][0-9][0-9]')
);

/*role permission*/
create table role_permission(
r_id varchar(4) not null,
permission varchar(100) not null,
constraint rp_fk foreign key(r_id) references role(r_id),
constraint rp_ck check(r_id LIKE'[r/R][0-9][0-9][0-9]')
);

/*notice*/
create table notice(
n_id varchar(6) not null,
notice varchar(200),
r_id varchar(4) not null,
constraint n_pk primary key(n_id),
constraint n_fk foreign key(r_id) references role(r_id),
constraint n_ck check(n_id LIKE'[n/N][0-9][0-9][0-9][0-9][0-9]'),
constraint r_ck check(r_id LIKE'[r/R][0-9][0-9][0-9]')
);

/*book*/
create table book(
b_id varchar(6) not null,
name varchar(50)not null,
isbn int not null,
category varchar(100)not null,
author varchar(100),
constraint b_pk primary key(b_id),
constraint b_ck check(b_id LIKE'[b/B][0-9][0-9][0-9][0-9][0-9]'),
);

/*inventory*/
create table inventory(
b_id varchar(6) not null,
quantity int,
constraint i_fk foreign key(b_id) references book(b_id),
constraint ib_ck check(b_id LIKE'[b/B][0-9][0-9][0-9][0-9][0-9]')
);

/*book_customer*/
create table book_customer(
c_id varchar(6) not null,
b_id varchar(6) not null,
issue_date date not null,
return_date date not null,
constraint bc_fk1 foreign key(c_id) references customer(c_id),
constraint bc_fk2 foreign key(b_id) references book(b_id),
constraint bccid_ck check(c_id LIKE'[c/C][0-9][0-9][0-9][0-9][0-9]'),
constraint bcbid_ck check(b_id LIKE'[b/B][0-9][0-9][0-9][0-9][0-9]')
);

/*recipt*/
create table reciept(
invoice_no varchar(6) not null,
r_amount int,
remarks varchar(50),
c_id varchar(6)not null,
constraint re_pk primary key(invoice_no),
constraint re_fk foreign key(c_id) references customer(c_id),
constraint rei_ck check(invoice_no LIKE'[i/I][0-9][0-9][0-9][0-9][0-9]'),
constraint recid_ck check(c_id LIKE'[c/C][0-9][0-9][0-9][0-9][0-9]')
);

/*fine*/
create table fine(
f_id varchar(6) not null,
b_id varchar(6) not null,
issue_date date not null,
return_date date not null,
returned_date date not null,
constraint f_pk primary key(f_id),
constraint f_fk foreign key(b_id) references book(b_id),
constraint fid_ck check(f_id LIKE'[f/F][0-9][0-9][0-9][0-9][0-9]'),
constraint fbid_ck check(b_id LIKE'[b/B][0-9][0-9][0-9][0-9][0-9]')
);

/*customer fine*/
create table customer_fine(
f_id varchar(6) not null,
c_id varchar(6) not null,
amount int not null,
constraint cf_fk1 foreign key(f_id) references fine(f_id),
constraint cf_fk2 foreign key(c_id) references customer(c_id),
constraint cffid_ck check(f_id LIKE'[f/F][0-9][0-9][0-9][0-9][0-9]'),
constraint cfcid_ck check(c_id LIKE'[c/C][0-9][0-9][0-9][0-9][0-9]')
);

/*admin manage*/
create table admin_manage(
a_id varchar(6) not null,
c_id varchar(6) not null,
s_id varchar(6) not null,
b_id varchar(6) not null,
m_id varchar(4) not null,
r_id varchar(4) not null,
constraint am_fk1 foreign key(a_id) references admin(a_id),
constraint am_fk2 foreign key(c_id) references customer(c_id),
constraint am_fk3 foreign key(s_id) references staff(s_id),
constraint am_fk4 foreign key(b_id) references book(b_id),
constraint am_fk5 foreign key(m_id) references membership(m_id),
constraint am_fk6 foreign key(r_id) references role(r_id),
constraint amid_ck check(a_id LIKE '[a/A][0-9][0-9][0-9][0-9][0-9]'),
constraint amcid_ck check(c_id LIKE '[c/C][0-9][0-9][0-9][0-9][0-9]'),
constraint amsid_ck check(s_id LIKE '[s/S][0-9][0-9][0-9][0-9][0-9]'),
constraint amb_ck check(b_id LIKE'[b/B][0-9][0-9][0-9][0-9][]0-9]'),
constraint ammid_ck check(m_id LIKE '[m/M][0-9][0-9][0-9]'),
constraint amrid_ck check(r_id LIKE'[r/R][0-9][0-9][0-9]')
);
/*staff manage*/
create table staff_manage(
s_id varchar(6) not null,
c_id varchar(6) not null,
b_id varchar(6) not null,
m_id varchar(4) not null,
constraint sm_fk1 foreign key(s_id) references staff(s_id),
constraint sm_fk2 foreign key(c_id) references customer(c_id),
constraint sm_fk3 foreign key(b_id) references book(b_id),
constraint sm_fk4 foreign key(m_id) references membership(m_id),
constraint smid_ck check(s_id LIKE '[a/A][0-9][0-9][0-9][0-9][0-9]'),
constraint smcid_ck check(c_id LIKE '[c/C][0-9][0-9][0-9][0-9][0-9]'),
constraint smbid_ck check(b_id LIKE'[b/B][0-9][0-9][0-9][0-9][]0-9]'),
constraint smmid_ck check(m_id LIKE '[m/M][0-9][0-9][0-9]'),
);


/*Insert value to membership*/
insert into membership values ('M001','basic');
insert into membership values ('M002','premium');



/*Insert value to customer*/

insert into customer values('C00001','Ashan','Vithanage','2002-04-01','No 03 Flower road,Malabe',
'0788410318','2002454568','M001');
insert into customer values('C00002','Dilshan','Mendis','2001-09-20','No 03 Temple road,Ragama',
'0752555338','2001478563','M002');

insert into customer values('C00003','Ravindu','Nanayakkara','2000-02-14','No 24 Hokandara south,Hokandara',
'0719960110','2000545331','M001');

insert into customer values('C00004','Kavindu','Avishanka','2001-04-14','No 06/10 Hospital road,Angoda',
'0767532191','2001863313','M001');

insert into customer values('C00005','Chandimal','Weerasinghe','1973-12-25','No 03 Flower road,Malabe',
'0788410318','2002454684','M002');



/*Insert value to role*/
insert into role values('R001','Admin');
insert into role values('R002','Librarian');
insert into role values('R003','Assistant librarian');


 /*Insert value to staff*/



insert into staff values('S00001','Kamal','Hathurusinghe','1987-04-10','No 07 Church road,Jaela','075110485','874564142','R001');
insert into staff values('S00002','Samal','Gamage','1987-01-10','No 07 Mosque road,Kadavatha','075110489','874564131','R002');
insert into staff values('S00003','Ramal','Rajapaksha','1987-07-10','No 07 Temple road,Kiribathgoda','075110484','874564129','R003');

/*Insert value to staff email*/



insert into staff_email values('S00001','KamalHathuru2@gmail.com');
insert into staff_email values('S00001','HathuruKamal@gmail.com');
insert into staff_email values('S00002','samalgamage87@gmail.com');

/*Insert value to admin*/



insert into admin values('A00001','Mahinda','Rajapaksha','1936-04-01','No 12, Mirihana road, Thalavathugoda','0719204567','36456718','R001');

/*Insert value to email*/
insert into admin_email values('A00001','mahindarox@gmail.com');
insert into admin_email values('A00001','tsunami2004@gmail.com');



/*Insert value to permission*/

insert into role_permission values('R001','manage members');
insert into role_permission values('R001','manage inventory');
insert into role_permission values('R001','manage library');
insert into role_permission values('R001','manage users');
insert into role_permission values('R001','manage roles');
insert into role_permission values('R001','manage homepage');
insert into role_permission values('R001','manage inquiries');
insert into role_permission values('R001','manage notices');
insert into role_permission values('R002','manage members');
insert into role_permission values('R002','manage inventory');
insert into role_permission values('R002','manage library');
insert into role_permission values('R003','manage library');


/*Insert value to notice*/



insert into notice values('N00001','Hello world','R001');
insert into notice values('N00002','Visit Sri Lanka','R002');

/*Insert value to book*/

select * from book

insert into book values('B00001','rocket boys','0440257','history','Homer Hickam');
insert into book values('B00002','John Adams','5547894','biography','David Mccullough');
insert into book values('B00003','Harry Potter','4477896','fantacy','J.K.Rowling');
insert into book values('B00004','Hoobit','5557896','fantacy','Tolkien');
insert into book values('B00005','Madol duwa','7744256','biography','Martin Wickramasinghe');

/*Insert value to Linventory*/



insert into inventory values('B00001','10');
insert into inventory values('B00002','15');
insert into inventory values('B00003','25');
insert into inventory values('B00004','5');
insert into inventory values('B00005','12');

/*Insert value to book_customer*/



insert into book_customer values('C00001','B00001','2022-10-30','2022-11-30');
insert into book_customer values('C00002','B00002','2022-09-30','2022-10-30');
insert into book_customer values('C00003','B00003','2022-06-20','2022-07-20');
insert into book_customer values('C00004','B00004','2021-02-25','2021-03-25');
insert into book_customer values('C00005','B00005','2021-06-11','2021-07-11');



/*Insert value to recipt*/

insert into reciept values('I00001','300','Pay fine','C00001');
insert into reciept values('I00002','100','Pay fine','C00002');
insert into reciept values('I00003','500','Pay fine','C00003');
insert into reciept values('I00004','600','Pay fine','C00004');
insert into reciept values('I00005','700','Pay fine','C00005');



/*Insert value to customer fine*/

insert into customer_fine values('F00001', 'C00001', '500');
insert into customer_fine values('F00002', 'C00002', '200');
insert into customer_fine values('F00003', 'C00002', '100');
insert into customer_fine values('F00004', 'C00003', '500');
insert into customer_fine values('F00005', 'C00004', '500');


/*Insert value to fine*/
insert into fine values('F00001', 'B00001', '2022-09-28', '2022-10-28', '2022-10-30');
insert into fine values('F00002', 'B00002', '2022-09-28', '2022-10-28', '2022-10-30');
insert into fine values('F00003', 'B00002', '2022-08-28', '2022-09-28', '2022-09-30');
insert into fine values('F00004', 'B00003', '2022-07-28', '2022-08-28', '2022-08-30');
insert into fine values('F00005', 'B00004', '2022-09-28', '2022-10-28', '2022-10-30');

