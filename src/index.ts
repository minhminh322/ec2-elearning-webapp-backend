import express from "express";
import http from "http";
const dotenv = require("dotenv");
import bodyParser from "body-parser";
import cookieParser from "cookie-parser";
import compression from "compression";
import cors from "cors";
import router from "./routes";
dotenv.config();

const app = express();
const port = process.env.PORT || 8000;

app.use(cors({ credentials: true }));

app.use(bodyParser.json());
app.use(cookieParser());
app.use(compression());

const server = http.createServer(app);

server.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

app.use("/", router());
