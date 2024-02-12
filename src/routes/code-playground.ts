import express from "express";
import { getPracticeProblems } from "../controllers/practiceProblems";

export default (router: express.Router) => {
  router.get("/code-playground", getPracticeProblems);
};
