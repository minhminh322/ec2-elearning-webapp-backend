import express from "express";
import submissions from "./submissions";
import practiceProblems from "./code-playground";
import simpleTest from "./simpleTest";

const router = express.Router();

export default (): express.Router => {
  submissions(router);
  practiceProblems(router);
  simpleTest(router);
  return router;
};
