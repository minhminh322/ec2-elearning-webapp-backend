require("dotenv").config();

const mysql = require("mysql");

const db = mysql.createConnection({
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_DATABASE,
  ssl: true,
});

// connect.
db.connect((err: any) => {
  if (err) {
    console.error("Error connecting to MySQL RDS: " + err.stack);
    return;
  }
  console.log("Connected to MySQL RDS as ID " + db.threadId);
});

export default db;
