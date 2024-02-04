import express from "express";
import http from "http";
import bodyParser from "body-parser";
import cookieParser from "cookie-parser";
import compression from "compression";
import cors from "cors";
import router from "./routes";

const app = express();

app.use(cors({ credentials: true }));

app.use(bodyParser.json());
app.use(cookieParser());
app.use(compression());

const server = http.createServer(app);

server.listen(8080, () => {
  console.log("Server is running on port 8080");
});

app.use("/", router());
