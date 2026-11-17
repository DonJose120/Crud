CREATE DATABASE IF NOT EXISTS gestor_contrasena; 
CREATE TABLE `baul` 
( `id_baul` int NOT NULL AUTO_INCREMENT, 
`Plataforma` varchar(80) NOT NULL, 
`usuario` varchar(80) NOT NULL, 
`clave` varchar(80) NOT NULL, 
PRIMARY KEY (`id_baul`), 
UNIQUE KEY `Plataforma` (`Plataforma`,`usuario`) ); 