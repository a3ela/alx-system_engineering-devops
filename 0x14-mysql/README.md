# Project: 0x14. MySQL

## Resources

#### Read or watch:

* [What is a primary-replica cluster](https://intranet.alxswe.com/rltoken/eojqG9FZbA6QVWN5P9cLzA)
* [MySQL primary replica setup](https://intranet.alxswe.com/rltoken/z2KVk2UKLMc0RvHMdJmYLg)
* [Build a robust database backup strategy](https://intranet.alxswe.com/rltoken/BharnxaLb-BDDYFywzME2Q)
## Learning Objectives

### General

* What is the main role of a database
* What is a database replica
* What is the purpose of a database replica
* Why database backups need to be stored in different physical locations
* What operation should you regularly perform to make sure that your database backup strategy actually works
## Tasks

| Task | File |
| ---- | ---- |
| 0. Install MySQL | [SOON](./) |
| 1. Let us in! | [SOON](./) |
| 2. If only you could see what I've seen with your eyes | [SOON](./) |
| 3. Quite an experience to live in fear, isn't it? | [SOON](./) |
| 4. Setup a Primary-Replica infrastructure using MySQL | [4-mysql_configuration_primary](./4-mysql_configuration_primary), [4-mysql_configuration_replica](./4-mysql_configuration_replica) |
| 5. MySQL backup | [5-mysql_backup](./5-mysql_backup) |

# MySQL Replication

![MySQL_Replication](https://raw.githubusercontent.com/kiminzajnr/Python_Projects/master/LW_Minis/MySQL_Replication/img/Repl.png)

## MySQL 5.7.* Installation
## [How To Install Guide](https://intranet.alxswe.com/concepts/100002) - (credits: [nuuX](https://github.com/nuuxcode) - C13)
- Check version:
```
mysql --version
```

## Create a database on the primary server
```
CREATE DATABASE tyrell_corp;
```

## Create a table
```
USE tyrell_corp;
CREATE TABLE nexus6 (id int auto_increment primary key, name varchar(50));

```

## Add atleast one entry to the table
```
INSERT INTO nexus6(name) VALUES ("Erick");
```

## Create a new user for the replica 
```
CREATE USER 'replica_user'@'%' IDENTIFIED BY 'password';
```

## Grant replication permission
```
GRANT REPLICATION SLAVE ON *.* TO 'replica_user'@'%';
```

# Setting up the replication

# Configure master

- Add:
```
server-id        = 1
log_bin          = /var/log/mysql/mysql-bin.log # binary log - record changes made to the db in binary formart
binlog_do_db     = tyrell_corp
```
- To:
```
/etc/mysql/mysql.conf.d/mysqld.cnf
```

- Restart MySQL
```
sudo systemctl restart mysql
```

- Get Binary log coordinates from master

```
FLUSH TABLES WITH READ LOCK;
SHOW MASTER STATUS;
```

## Migrate existing data to slave
- Create a snapshot using mysqldump utility
```
sudo mysqldump tyrell_corp > tyrell_corp.sql
```

- Use scp to copy the snapshot to slave
```
scp -i ~/.ssh/priv.key tyrell_corp.sql ubuntu@slave_ip:/tmp/
```

- create `tyrell_corp` database in slave
```
CREATE DATABASE tyrell_corp;
```

- import the snapshot
```
sudo mysql tyrell_corp < /tmp/tyrell_corp.sql
```

- Unlock tables in master
```
UNLOCK TABLES;
```

# Configure slave
- Add:
```
server-id               = 2
log_bin                 = /var/log/mysql/mysql-bin.log
binlog_do_db            = tyrell_corp
relay-log               = /var/log/mysql/mysql-relay-bin.log 
# Contain everything read from master bin log
# Store events that need to be applied to slave db locally
# Events are read from relay log and applied to slave
```

- To:
```
/etc/mysql/mysql.conf.d/mysqld.cnf
```

- restart MySQL
```
sudo systemctl restart mysql
```

# Testing Replication

- On slave, configure replication settings by running:

```
CHANGE MASTER TO
MASTER_HOST='master_ip',
MASTER_USER='replica_user',
MASTER_PASSWORD='password',
MASTER_LOG_FILE='mysql-bin.000001',
MASTER_LOG_POS=154;
```

- Activate slave
```
START SLAVE;
```

- Show slave state
```
SHOW SLAVE STATUS\G;
```

- Creating an entry in master should now reflect in slave
