import express from "express";
import submissions from "./submissions";

const router = express.Router();

export default (): express.Router => {
  submissions(router);
  return router;
};
