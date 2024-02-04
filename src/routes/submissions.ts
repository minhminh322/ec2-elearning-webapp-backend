import { createSubmission } from "../controllers/submissions";
import express from "express";

export default (router: express.Router) => {
  router.post("/submissions", createSubmission);
};
