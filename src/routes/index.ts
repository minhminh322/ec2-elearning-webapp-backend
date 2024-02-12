import express from "express";
import submissions from "./submissions";
import practiceProblems from "./code-playground";

const router = express.Router();

export default (): express.Router => {
  submissions(router);
  practiceProblems(router);
  return router;
};
