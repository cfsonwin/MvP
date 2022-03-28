INSERT INTO DB_NAME.administrator
(admin_id, Email, u_name, u_password, pw_salt, u_status, addtime, modifytime)
VALUES(1, 'fashu_cheng@outlook.com', 'Fashu/Cheng', '8d19a3ce094e0d58c1d3714333ca5c9a', 869068, 0, '2022-02-27 15:12:00', '2022-02-27 15:12:00');

INSERT INTO DB_NAME.`constructor`
(u_id, Email, u_name, u_password, pw_salt, u_status, addtime, modifytime, addr)
VALUES(1, 'Fashu_cheng@outlook.com', 'Fashu/Cheng', '6987cc38664f6169ee45b6ed029a0e43', 932264, 0, '2022-02-27 15:14:36', '2022-02-27 15:14:36', 'pallaswiesenstrasse 57_64293_Darmstadt_Germany');
INSERT INTO DB_NAME.`constructor`
(u_id, Email, u_name, u_password, pw_salt, u_status, addtime, modifytime, addr)
VALUES(2, 'Lukas_Hoffmann@example.de', 'Lukas/Hoffmann', '727491d84cb33a1053dbbe3b6cd5ef4e', 832400, 0, '2022-02-27 15:19:58', '2022-02-27 15:41:44', 'Mathildenstraße 15_64625_Bensheim_Germany');
INSERT INTO DB_NAME.`constructor`
(u_id, Email, u_name, u_password, pw_salt, u_status, addtime, modifytime, addr)
VALUES(3, 'Anna_Friedrich@example.de', 'Anna/Friedrich', '4d58b84bd76eb9c1460c8729da9c8ec0', 372164, 1, '2022-02-27 15:23:37', '2022-02-27 15:42:05', 'Jahnstraße 120_70597 _Stuttgart_Germany');
INSERT INTO DB_NAME.`constructor`
(u_id, Email, u_name, u_password, pw_salt, u_status, addtime, modifytime, addr)
VALUES(4, 'Clemencia_Martin@example.de', 'Clemencia/Martin', 'c53df1357857b9d67265a37369448cd2', 613249, 0, '2022-02-27 15:27:48', '2022-02-27 15:27:48', 'Place d''Armes_78000 _Versailles_France');
INSERT INTO DB_NAME.`constructor`
(u_id, Email, u_name, u_password, pw_salt, u_status, addtime, modifytime, addr)
VALUES(5, 'Alexander_Keller@example.com', 'Alexander/Keller', '0ca297a7c7f941499898820eac176204', 615300, 0, '2022-02-27 15:38:09', '2022-02-27 15:38:09', 'Sechseläutenpl. 1_8008_Zürich_Switzerland');

INSERT INTO DB_NAME.cpmapping
(id, c_id, c_email, p_id)
VALUES(1, 1, 'Fashu_cheng@outlook.com', 1);
INSERT INTO DB_NAME.cpmapping
(id, c_id, c_email, p_id)
VALUES(2, 1, 'Fashu_cheng@outlook.com', 2);
INSERT INTO DB_NAME.cpmapping
(id, c_id, c_email, p_id)
VALUES(3, 2, 'Lukas_Hoffmann@example.de', 1);
INSERT INTO DB_NAME.cpmapping
(id, c_id, c_email, p_id)
VALUES(4, 4, 'Clemencia_Martin@example.de', 3);
INSERT INTO DB_NAME.cpmapping
(id, c_id, c_email, p_id)
VALUES(5, 5, 'Alexander_Keller@example.com', 3);

INSERT INTO DB_NAME.manufacturer
(m_id, contact, addr, loc, m_status, addtime, modifytime, description, m_name)
VALUES(1, 'manu1@example.com', 'Otto-Berndt-Straße 2_64287_Darmstadt_Germany', '49.861252,8.682602', 0, '2022-02-27 15:14:36', '2022-02-27 15:14:36', '''''''first time add''''''', 'TU Darmstadt');
INSERT INTO DB_NAME.manufacturer
(m_id, contact, addr, loc, m_status, addtime, modifytime, description, m_name)
VALUES(2, 'manu2@example.com', 'Keplerstraße 7_70174_Stuttgart_Germany', '48.781197,9.173505', 0, '2022-02-27 15:14:36', '2022-02-27 15:14:36', '''''''first time add''''''', 'Universität Stuttgart');
INSERT INTO DB_NAME.manufacturer
(m_id, contact, addr, loc, m_status, addtime, modifytime, description, m_name)
VALUES(3, 'manu3@example.com', '3 Rue Joliot Curie_91190_Gif-sur-Yvette_France', '48.709340,2.166256', 0, '2022-02-27 15:14:36', '2022-02-27 15:14:36', '''''''first time add''''''', 'CentraleSupélec - Université Paris-Saclay');
INSERT INTO DB_NAME.manufacturer
(m_id, contact, addr, loc, m_status, addtime, modifytime, description, m_name)
VALUES(4, 'manu4@example.com', 'Edificio 1_20133_Milano MI_Italy', '45.478005,9.227311', 0, '2022-02-27 15:14:36', '2022-02-27 15:14:36', '''''''first time add''''''', 'Politecnico di Milano');
INSERT INTO DB_NAME.manufacturer
(m_id, contact, addr, loc, m_status, addtime, modifytime, description, m_name)
VALUES(5, 'manu5@example.com', 'Mekelweg 5_2628_CD Delft_Niederlande', '52.002073,4.372997', 0, '2022-02-27 15:14:36', '2022-02-27 15:14:36', '''''''first time add''''''', 'Technische Universiteit Delft');
INSERT INTO DB_NAME.manufacturer
(m_id, contact, addr, loc, m_status, addtime, modifytime, description, m_name)
VALUES(6, 'manu6@example.com', 'Boltzmannstraße 15_85748_Garching bei München_Germany', '48.265414,11.670284', 0, '2022-02-27 15:14:36', '2022-02-27 15:14:36', '''''''first time add''''''', 'Technische Universität München Garching');

INSERT INTO DB_NAME.pmmapping
(id, p_id, m_id, m_pnode, m_Tlevel)
VALUES(1, 1, 1, 0, '1');
INSERT INTO DB_NAME.pmmapping
(id, p_id, m_id, m_pnode, m_Tlevel)
VALUES(2, 1, 2, 1, '2');
INSERT INTO DB_NAME.pmmapping
(id, p_id, m_id, m_pnode, m_Tlevel)
VALUES(3, 1, 3, 1, '2');
INSERT INTO DB_NAME.pmmapping
(id, p_id, m_id, m_pnode, m_Tlevel)
VALUES(4, 1, 4, 3, '3');
INSERT INTO DB_NAME.pmmapping
(id, p_id, m_id, m_pnode, m_Tlevel)
VALUES(5, 2, 1, 0, '1');
INSERT INTO DB_NAME.pmmapping
(id, p_id, m_id, m_pnode, m_Tlevel)
VALUES(6, 2, 2, 0, '1');
INSERT INTO DB_NAME.pmmapping
(id, p_id, m_id, m_pnode, m_Tlevel)
VALUES(7, 2, 5, 2, '2');
INSERT INTO DB_NAME.pmmapping
(id, p_id, m_id, m_pnode, m_Tlevel)
VALUES(8, 2, 6, 2, '2');
INSERT INTO DB_NAME.pmmapping
(id, p_id, m_id, m_pnode, m_Tlevel)
VALUES(9, 3, 1, 0, '1');

INSERT INTO DB_NAME.product
(p_id, p_name, p_status, addtime, modifytime, avatar, description)
VALUES(1, 'vProduct_1', 0, '2022-02-27 15:14:36', '2022-02-27 15:14:36', NULL, 'description for vProduct 1');
INSERT INTO DB_NAME.product
(p_id, p_name, p_status, addtime, modifytime, avatar, description)
VALUES(2, 'vProduct_2', 0, '2022-02-27 15:14:40', '2022-02-27 15:14:40', NULL, 'description for vProduct 2');
INSERT INTO DB_NAME.product
(p_id, p_name, p_status, addtime, modifytime, avatar, description)
VALUES(3, 'vProduct_3', 0, '2022-02-27 15:14:56', '2022-02-27 15:14:56', NULL, 'description for vProduct 3');