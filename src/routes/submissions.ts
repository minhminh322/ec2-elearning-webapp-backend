import { createSubmissions } from "../controllers/submissions";
import express from "express";

export default (router: express.Router) => {
  // router.get("/submissions/batch", getSubmissions);
  router.post("/submissions", createSubmissions);
};
